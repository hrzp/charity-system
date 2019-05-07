from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
)
from flask import Blueprint, jsonify, request, g, session
from charity.serverbase import ErrorToClient, acc
from charity.common.general import set_log
from charity.common.mail import send_mail
from captcha.image import ImageCaptcha
from charity.database import db as db
from random import randrange as rnd
import random
import string
import hashlib
import base64
import json


bp = Blueprint('general', __name__)


image = ImageCaptcha(fonts=['charity/ui/assets/font/cap.ttf'])
# image = ImageCaptcha()


class Captcha(object):
    def __init__(self):
        pass

    def generate(self):
        captcha_number = str(rnd(1, 999, 1) * 10)
        session['captcha_value'] = hashlib.sha256(
            captcha_number.encode('utf-8')).hexdigest()
        data = image.generate(captcha_number)
        return base64.b64encode(data.getvalue())


@bp.route('/new-captcha')
def new_captcha():
    captcha = Captcha()
    cap = captcha.generate()
    return jsonify({
        'status': True,
        'args': {
            'captcha': cap.decode('utf-8')
        }
    })
