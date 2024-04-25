import os
from app import create_app, db
from app.models import *
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():                                                  #integrade db with python shell
    #return dict(app=app, db=db, User=User, Role=Role)
    return dict(app=app, db=db)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command('delete_shared')
def expired_links():
    import datetime
    """Check for expired shared links"""
    current_time = datetime.datetime.now()
    print(f'Current Time: {current_time}')
    last_day = current_time - datetime.timedelta(hours=24)
    print(f'Last day: {last_day}')
    #get links before last 24 hours.
    links = ShareLink.query.filter(ShareLink.created < last_day).all()
    print(len(links))
    for link in links:
        print(link.created)
        db.session.delete(link)
    db.session.commit()

