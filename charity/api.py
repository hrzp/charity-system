from charity.views import user
from charity.views import general
from charity.database import db
from sqlalchemy.orm import validates


def register_blueprint(app):
    # Regester App routes
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(general.bp, url_prefix='/general')


def register_restless(manager):
    manager.create_api(db.User, methods=['GET'], exclude_columns=[
                       'password', 'force_to_change_password',
                       'mail', 'mail_verified'])
    manager.create_api(db.Role, methods=['GET'], exclude_columns=[])
