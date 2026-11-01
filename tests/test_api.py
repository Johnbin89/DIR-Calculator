import unittest

from app import create_app, db, socketio
from app.minimum_gas.forms import DiveForm, TankForm
from app.minimum_gas.validation import GAS_SWITCHES, TANKS
from app.models import ShareLink


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_minimum_gas_plan(self):
        response = self.client.post('/api/minimum-gas', json={'depth': 45, 'solve': 1, 'gas': 21})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(
            data['plan'],
            [{'depth': 45, 'time': 1}, {'depth': 24, 'time': 4}, {'depth': 21, 'time': 5}, {'depth': 21, 'time': 6}],
        )
        self.assertEqual(data['time_to_fs'], 3)
        self.assertEqual(data['tank'], 24)

    def test_minimum_gas_warnings(self):
        response = self.client.post('/api/minimum-gas', json={'depth': 80, 'solve': 1, 'gas': 21})
        self.assertEqual(response.status_code, 422)
        self.assertIn('warning', response.get_json())
        response = self.client.post('/api/minimum-gas', json={'depth': 35, 'solve': 1, 'gas': 0})
        self.assertEqual(response.status_code, 422)

    def test_minimum_gas_validation(self):
        response = self.client.post('/api/minimum-gas', json={'depth': -1, 'solve': 0, 'gas': 5})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(set(response.get_json()['errors']), {'depth', 'solve', 'gas'})

    def test_gas_used(self):
        response = self.client.post('/api/gas-used', json={'litres': 1290, 'tank': 24})
        self.assertEqual(response.get_json(), {'bar': 60, 'selected_tank': 24})

    def test_share_roundtrip(self):
        response = self.client.post('/api/share', json={'depth': 45, 'solve': 1, 'gas': 21})
        hash = response.get_json()['hash']
        response = self.client.get(f'/api/share/{hash}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['depth'], 45)
        self.assertEqual(self.client.get('/api/share/zzzzzz').status_code, 404)

    def test_invalid_tank_rejected(self):
        for tank in (0, -24, 7):
            response = self.client.post('/api/minimum-gas', json={'depth': 45, 'solve': 1, 'gas': 21, 'tank': tank})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(set(response.get_json()['errors']), {'tank'})
            response = self.client.post('/api/gas-used', json={'litres': 1290, 'tank': tank})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(set(response.get_json()['errors']), {'tank'})

    def test_share_rejects_plan_with_warning(self):
        response = self.client.post('/api/share', json={'depth': 200, 'solve': 1, 'gas': 21})
        self.assertEqual(response.status_code, 422)
        self.assertIn('warning', response.get_json())
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(ShareLink)), 0)

    def test_legacy_routes_validate(self):
        response = self.client.post('/gas_used', data={'tank': '0', 'min_gas_L': '1290'})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/gas_used', data={'tank': '24', 'min_gas_L': '1290'})
        self.assertEqual(response.get_json(), {'bar': 60, 'selected_tank': 24})
        response = self.client.post('/share', data={'depth': '45', 'solve': '1', 'gas': '5'})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/share', data={'depth': '200', 'solve': '1', 'gas': '21'})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/share', data={'depth': '45', 'solve': '1', 'gas': '21'})
        self.assertEqual(response.status_code, 200)

    def test_forms_use_shared_choices(self):
        with self.app.test_request_context():
            self.assertEqual(
                [(int(choice.value), choice.label) for choice in DiveForm().gas.choices],
                list(GAS_SWITCHES.items()),
            )
            self.assertEqual(
                [(int(choice.value), choice.label) for choice in TankForm().tank.choices],
                list(TANKS.items()),
            )

    def test_legacy_page_renders_choices(self):
        html = self.client.get('/minimum-gas').get_data(as_text=True)
        self.assertIn('<option', html)
        self.assertIn('21m - 50%', html)


class SocketValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(ShareLink(depth=45, gas=21, solve=1, hash='abcdef'))
        db.session.commit()
        self.socket = socketio.test_client(self.app)
        self.socket.emit('join', {'room': 'abcdef'})
        self.socket.get_received()

    def tearDown(self):
        self.socket.disconnect()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def plan_change(self, **overrides):
        event = {'room': 'abcdef', 'new_depth': 30, 'new_gas': 6, 'new_solve_time': 2, 'selected_tank': 24}
        self.socket.emit('plan_change', {**event, **overrides})
        db.session.expire_all()
        return self.socket.get_received()

    def test_valid_plan_change(self):
        received = self.plan_change()
        self.assertEqual([event['name'] for event in received], ['plan_change'])
        self.assertEqual(db.session.scalars(db.select(ShareLink)).one().depth, 30)

    def test_invalid_plan_change_ignored(self):
        for overrides in ({'new_gas': 5}, {'selected_tank': 0}, {'new_depth': 200}, {'new_depth': 'x'}):
            self.assertEqual(self.plan_change(**overrides), [])
            sharedplan = db.session.scalars(db.select(ShareLink)).one()
            self.assertEqual((sharedplan.depth, sharedplan.gas, sharedplan.solve), (45, 21, 1))

    def test_tank_change(self):
        event = {'room': 'abcdef', 'min_gas_l': 1290}
        self.socket.emit('shared_tank_change', {**event, 'selected_tank': 0})
        self.assertEqual(self.socket.get_received(), [])
        self.socket.emit('shared_tank_change', {**event, 'selected_tank': 24})
        self.assertEqual([event['name'] for event in self.socket.get_received()], ['shared_tank_change'])
