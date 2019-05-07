from flask import Flask


app = Flask(__name__)

try:
    import charity.serverbase
    from charity.api import register_blueprint
    register_blueprint(app)
except Exception as e:
    raise Exception(e)
