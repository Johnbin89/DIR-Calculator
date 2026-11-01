GAS_SWITCHES = {21: '21m - 50%', 6: 'Oxygen', 0: 'Surface'}
TANKS = {14: 'D7', 17: 'D8.5', 20: 'D10', 24: 'D12', 30: 'D15'}


def plan_warning(depth, gas_switch):
    """Return a warning message when the plan should not be calculated."""
    if depth > 70:
        return 'That deep with available just a 50% is not wise'
    if gas_switch == 0 and depth > 30:
        return 'Better take a stage, if you want to go below 30 meters.'
    return None


def read_int(data, key, errors, default=None):
    value = data.get(key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        errors[key] = 'Enter only integer numbers'
        return None


def read_tank(data, key, errors, default=None):
    tank = read_int(data, key, errors, default)
    if tank is not None and tank not in TANKS:
        errors[key] = 'Not a valid choice'
    return tank


def validate_plan_input(data):
    errors = {}
    depth = read_int(data, 'depth', errors)
    solve = read_int(data, 'solve', errors, default=1)
    gas = read_int(data, 'gas', errors)
    tank = read_tank(data, 'tank', errors, default=24)
    if depth is not None and depth <= 0:
        errors['depth'] = 'Provide positive integer'
    if solve is not None and solve < 1:
        errors['solve'] = 'Less than a minute to handle Out-Of-Gas?'
    if gas is not None and gas not in GAS_SWITCHES:
        errors['gas'] = 'Not a valid choice'
    return depth, solve, gas, tank, errors
