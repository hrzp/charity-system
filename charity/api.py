from flask import g
from charity.views import user
from charity.views import general
from charity.database import db
from sqlalchemy.orm import validates
from charity.serverbase import ErrorToClient


def register_blueprint(app):
    # Regester App routes
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(general.bp, url_prefix='/general')


msg = 'You are not allow to access this point'


def admin_required(*args, **kw):
    if 'admin' not in g.user_roles:
        raise ErrorToClient(msg)


def register_restless(manager):
    manager.create_api(db.User, methods=['GET'], exclude_columns=[
                       'password', 'force_to_change_password',
                       'mail', 'mail_verified'])
    manager.create_api(db.Role, methods=['GET'], exclude_columns=[])
    manager.create_api(db.BaseCategory,
                       methods=['GET',
                                'POST',
                                'DELETE',
                                'PUT'],
                       exclude_columns=[],
                       collection_name="base-category",
                       preprocessors={'GET_MANY': [admin_required],
                                      'GET_SINGLE': [admin_required],
                                      'POST': [admin_required],
                                      'PATCH_SINGLE': [admin_required],
                                      'PATCH_MANY': [admin_required],
                                      'DELETE_SINGLE': [admin_required],
                                      'DELETE_MANY': [admin_required]
                                      })
    manager.create_api(db.BaseItem, methods=[
                       'GET', 'POST', 'DELETE', 'PUT'], exclude_columns=[], collection_name="base-item")
