from flask import render_template
from app import db
from app.errors import errors_bp

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    '''
    To make sure any failed database sessions do not interfere with any database accesses triggered by the template,issue a session rollback. 
    This resets the session to a clean state.
    '''
    db.session.rollback()
    return render_template('errors/500.html'), 500