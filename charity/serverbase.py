from sqlalchemy.orm import scoped_session
from charity.config import server_config as config
from flask_jwt_extended import JWTManager
from flask import request, g, redirect, session
from charity.database import db
from pymongo import MongoClient
from datetime import timedelta
from datetime import timedelta
from io import BytesIO as IO
from functools import wraps
from charity import app
import flask_restless
import functools
import logging
import redis
import json
import gzip


app.secret_key = config.server.secret_key
app.static_url_path = config.server.static_url_path
app.static_folder = config.server.static_folder
logger = logging.getLogger()


class ErrorToClient(Exception):
    pass


def load_user_roles():
    g.user_roles = []
    if g.user_id is None:
        return
    user = g.db_session.query(db.User).filter_by(id=g.user_id).first()
    if user is None or user.roles is None:
        return
    for role in user.roles:
        g.user_roles.append(
            role.name
        )


def gzip_content(response):
    accept_encoding = request.headers.get('Accept-Encoding', '')
    if 'gzip' not in accept_encoding.lower():
        return response
    response.direct_passthrough = False
    if (response.status_code < 200 or
        response.status_code >= 300 or
            'Content-Encoding' in response.headers):
        return response
    gzip_buffer = IO()
    gzip_file = gzip.GzipFile(mode='wb',
                              fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)
    return response


@app.errorhandler(ErrorToClient)
def error_to_client(error):
    logger.debug('ErrorToClient: %s', error)
    return json.dumps({
        'msg': error.args[0], 'args': error.args[1:]
    }), 400


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    db_session = scoped_session(db.Session)
    g.db_session = db_session
    g.user_id = session.get('user_id', None)
    g.user_roles = list()
    load_user_roles()


@app.after_request
def after_request(response):
    return gzip_content(response)


@app.teardown_request
def teardown_request(exception):
    db_session = getattr(g, 'db_session', None)
    if db_session is not None:
        db_session.close()


@app.route('/')
def index():
    return redirect('/static/index.html')


# Setup the flask-jwt-extended extension.
ACCESS_EXPIRES = timedelta(minutes=30)
REFRESH_EXPIRES = timedelta(days=1)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

# Setup our redis connection for storing the blacklisted tokens
redis_server = redis.StrictRedis(host='localhost', port=6379, db=0,
                                 decode_responses=True,
                                 password=config.redis.password)


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_server.get(jti)
    if entry is None:
        return True
    return entry == 'true'


def acc(*a):
    def func_wrapper(f):
        @wraps(f)
        def returned_wrapper(*args, **kwargs):
            for arg in a:
                if arg not in g.user_roles:
                    raise ErrorToClient(
                        'You Have no Premission to Access This Url')
            return f(*args, **kwargs)
        return returned_wrapper
    return func_wrapper


# use try to prevent pep8 error
try:
    from charity.api import register_restless
    db_session = scoped_session(db.Session)
    restless_api = flask_restless.APIManager(app, session=db_session)
    register_restless(restless_api)
except Exception as e:
    print(e)
    pass
