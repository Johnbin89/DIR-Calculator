import os
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():                                                  #integrade db with python shell
    #return dict(app=app, db=db, User=User, Role=Role)
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))   #integrade db with python shell
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def expired_links():
    import datetime
    """Check for expired shared links"""
    links = ShareLink.query.all()
    for link in links:
        if datetime.datetime.now() - link.created > datetime.timedelta(minutes=2):
            db.session.delete(link)
        db.session.commit()


if __name__ == "__main__":
    manager.run()