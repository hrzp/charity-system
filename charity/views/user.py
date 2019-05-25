from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jti,
    jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
)
from charity.serverbase import ACCESS_EXPIRES, REFRESH_EXPIRES, redis_server
from flask import Blueprint, jsonify, request, g, session, redirect
from charity.config import server_config as config
from charity.serverbase import ErrorToClient, acc
from charity.common.general import set_log
from charity.common.mail import send_mail
from charity.database import db as db
from datetime import datetime
from time import time as now
from sqlalchemy import or_
import hashlib
import string
import random
import json
import os

bp = Blueprint('user', __name__)


def new_role(name, label, is_systemic):
    role = g.db_session.query(db.Role).filter_by(name=name).first()
    if role is None:
        role = db.Role()
        role.name = name
        role.label = label
        role.is_systemic = is_systemic
        g.db_session.add(role)
        g.db_session.commit()
    return role


def add_password_history(user, password):
    p = db.PasswordHistory()
    p.user = user
    p.password = password
    g.db_session.add(p)
    g.db_session.commit()


def add_user(data):
    user_types = ('admin', 'employee')
    if data['user_type'] not in user_types:
        raise ErrorToClient('Not Valid User Type')
    username = data.get('username').lower()
    mail = data['mail']
    str = string.ascii_letters + string.digits
    password = ''.join(random.choices(str, k=8))
    res = g.db_session.query(db.User).filter(
        or_(db.User.username == username,
            db.User.mail == mail)).first()
    if res is not None:
        raise ErrorToClient('user already exists')
    hash_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    u = db.User()
    u.username = username
    u.password = hash_password
    u.user_type = data['user_type']
    u.roles.append(new_role(data['user_type'], data['user_type'], False))
    u.name = data['name']
    u.mail = mail
    u.active = data['active']
    u.force_to_change_password = False
    g.db_session.add(u)
    add_password_history(u, password)
    g.db_session.commit()
    html = """
        <hr><hr><hr><br>
        <p>Username: <strong>{}</strong></p>
        <p>Password: <strong>{}</strong></p>
        <br><hr><hr><hr>
    """.format(username, password)
    send_mail(data['mail'], 'Your Information', html)
    set_log(
        g.db_session.query(db.User).filter_by(id=g.user_id).first(),
        'Create New User, User:{} , User Id: {}'.format(u.name, u.id)
    )
    return u


def signin_log(user, _request):
    new_log = db.LoginHistory()
    new_log.user = user
    new_log.full_browser_info = str(_request.headers)
    new_log.browser = str(_request.headers.get('User-Agent'))
    new_log.ip = str(_request.remote_addr)
    g.db_session.add(new_log)
    g.db_session.commit()


# A blacklisted refresh tokens will not be able to access this endpoint
@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)
    redis_server.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    ret = {'access_token': access_token}
    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@bp.route('/access_revoke', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    redis_server.set(jti, 'true', ACCESS_EXPIRES * 1.2)
    return jsonify({"msg": "Access token revoked"}), 200


# Endpoint for revoking the current users refresh token
@bp.route('/refresh_revoke', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    redis_server.set(jti, 'true', REFRESH_EXPIRES * 1.2)
    return jsonify({"msg": "Refresh token revoked"}), 200


# *****************************
# *****************************
# **** USER GENRAL ROUTES *****
# *****************************
# *****************************


@bp.route('/new', methods=['POST'])
@jwt_required
@acc('admin', 'allow_create_user')
def new():
    data = json.loads(request.data)
    u = add_user(data)
    return jsonify({
        'msg': '{} Create Successfully'.format(u.username),
        'args': {'id': u.id}
    })


@bp.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    username = data['username'].lower()
    password = data['password']
    password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    user = g.db_session.query(db.User).filter_by(
        username=username, password=password).first()
    if user is None:
        session['user_id'] = None
        raise ErrorToClient('username or password not valid')

    signin_log(user, request)
    if not user.active:
        raise ErrorToClient(
            'You Account Disabeld.Please Call the System Admin')
    response = {
        'isLogin': True,
        'userType': user.user_type,
        'name': user.name,
        'roles': [item.name for item in user.roles],
    }

    response['mailVerified'] = True if user.mail_verified else False
    con = True if user.force_to_change_password else False
    response['ForceToChangePassword'] = con
    # if response['mailVerified'] is False:
    #     session['user_id'] = None
    #     raise ErrorToClient('Your Mail not Verified. Please \
    #                         Go to Your Mail(Also Check Your Spam)\
    #                         And Click Verification Link')
    session['user_id'] = user.id

    # Create JWTs
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    redis_server.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    redis_server.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)
    response['access_token'] = access_token
    response['refresh_token'] = refresh_token
    return jsonify(response)


@bp.route('/signout', methods=['GET', 'POST'])
@jwt_required
def _signout():
    session['user_id'] = None
    return jsonify({
        'userType': 'Guest',
        'name': 'Guest',
        'isLogin': False
    })


@bp.route('/is-signin', methods=['GET', 'POST'])
@jwt_required
def is_signin():
    if g.user_id is None:
        return jsonify({
            'userType': 'Guest',
            'name': 'Guest',
            'roles': [],
            'isLogin': False
        })
    user = g.db_session.query(db.User).filter_by(id=g.user_id).first()
    return jsonify({
        'userType': user.user_type,
        'name': user.name,
        'roles': [item.name for item in user.roles],
        'isLogin': True
    })


@bp.route('/info', methods=['GET'])
@jwt_required
def _info():
    user = g.db_session.query(db.User).filter_by(id=g.user_id).first()
    login_history = g.db_session.query(db.LoginHistory).filter_by(
        user=user).order_by(db.LoginHistory.id.desc()).first()
    data = {
        'history': {
            'ip': login_history.ip,
            'lastLoginDate': datetime.utcfromtimestamp(
                int(float(
                    login_history.last_login_date))).strftime(
                        '%Y-%m-%d %H:%M:%S'),
        },
        'username': user.username,
        'name': user.name,
        'roles': [role.name for role in user.roles]
    }
    return data


@bp.route('/list', methods=['GET'])
@acc('admin')
@jwt_required
def _list():
    users = g.db_session.query(db.User).all()
    user_list = list()
    for user in users:
        user_list.append({
            'id': user.id,
            'name': user.name,
            'userType': user.user_type
        })
    return jsonify({'args': user_list})


@bp.route('/login-report', methods=['POST'])
@acc('admin', 'see_login_history')
@jwt_required
def login_report():
    data = json.loads(request.data)
    from_date = int(data['from_date'])
    to_date = int(data['to_date'])
    from_date = datetime.utcfromtimestamp(
        from_date).strftime('%Y-%m-%d %H:%M:%S')
    to_date = datetime.utcfromtimestamp(to_date).strftime('%Y-%m-%d %H:%M:%S')
    user = g.db_session.query(db.User).filter_by(id=data['id']).first()
    reports = g.db_session.query(db.LoginHistory).filter(
        db.LoginHistory.last_login_date >= from_date,
        db.LoginHistory.last_login_date <= to_date,
        db.LoginHistory.user == user
    ).all()
    report_list = list()
    for report in reports:
        time = None
        if report.last_login_date:
            time = report.last_login_date.strftime('%Y-%m-%d %H:%M:%S')
        report_list.append({
            'time': time,
            'ip': report.ip,
            'browser': report.browser,
            'fullBrowserInfo': report.full_browser_info
        })
    return jsonify({'args': report_list})


@bp.route('/log-report', methods=['POST'])
@acc('admin', 'see_logs')
@jwt_required
def logs_report():
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    user = g.db_session.query(db.User).filter_by(id=data['id']).first()
    reports = g.db_session.query(db.Logger).filter(
        db.Logger.c_time_stamp >= str(from_date),
        db.Logger.c_time_stamp <= str(to_date),
        db.Logger.user == user
    ).all()
    report_list = list()
    for report in reports:
        report_list.append({
            'time': report.c_time_stamp,
            'msg': report.msg,
        })
    return jsonify({'args': report_list})


@bp.route('/sendmailverifaction', methods=['POST'])
@jwt_required
def send_mail_verifaction():
    data = json.loads(request.data)
    cap = hashlib.sha256(data['captcha_value'].encode('utf-8')).hexdigest()
    if cap != session['captcha_value']:
        raise ErrorToClient('Wrong Captcha Number')
    user = g.db_session.query(db.User).filter_by(id=g.user_id).first()
    token_key = ''.join(random.choices(
        string.ascii_letters + string.digits, k=125))
    token = db.Token()
    token.token = token_key
    token.user = user
    token._type = 'mail_verifaction'
    mail_html = """
        <hr><hr><hr>
        <a  style='background-color=rgb(66, 133, 244);color:white'
            href='http://127.0.0.1:5000/user/mail-verification/%s'>
            Click Here To Active Your Account</a>
        <hr><hr><hr>
    """ % token_key
    send_mail(
        user.mail,
        "Mail Verification(Rmonex)",
        mail_html,
    )
    g.db_session.add(token)
    g.db_session.commit()
    set_log(
        user,
        'Send Verification Mail'
    )
    return jsonify({'msg': 'Done', 'status': True})


@bp.route('/mail-verification/<token>', methods=['GET'])
def mail_verifaction(token):
    if not token:
        return redirect('/static/pages/404.html')
    token = g.db_session.query(db.Token).filter_by(
        token=token, _type='mail_verifaction').first()
    if not token:
        return redirect('/static/pages/404.html')
    if (now() - token.c_time_stamp) / 60 > 5:
        return redirect('static/pages/expiredTime.html')
    token.user.mail_verified = True
    g.db_session.delete(token)
    g.db_session.commit()
    set_log(
        token.user,
        'Mail Verification Done Successfuly'
    )
    return redirect('/static/pages/mailVerifiedSuccess.html')


@bp.route('/changepassword', methods=['POST'])
@jwt_required
def changepassword():
    data = json.loads(request.data)
    cap = hashlib.sha256(data['captcha_value'].encode('utf-8')).hexdigest()
    if cap != session['captcha_value']:
        raise ErrorToClient('Wrong Captcha Number')
    user = g.db_session.query(db.User).filter_by(id=g.user_id).first()
    token_key = ''.join(random.choices(
        string.ascii_letters + string.digits, k=125))
    token = db.Token()
    token.token = token_key
    token.user = user
    token._type = 'change_password'
    html = """
        <hr><hr><hr><br>
        <a href='{}'>Click This Link To Change Your Password</a>
        <br><hr><hr><hr>
    """.format(config.server.address+'/user/changepassword/'+token_key)
    send_mail(to=user.mail, subject='Change Password Request', html=html)

    g.db_session.add(token)
    g.db_session.commit()
    set_log(user, 'Ask For Change Password')
    return jsonify({'status': True, 'msg': 'Done'})


@bp.route('/changepassword/<token>', methods=['GET'])
def changepassword_token(token):
    # TODO: Check for expire time of token
    token_rec = g.db_session.query(db.Token).filter_by(
        token=token, _type='change_password', used=False).first()
    if not token_rec:
        return redirect('/static/pages/404.html')
    new_token_key = ''.join(random.choices(string.ascii_letters, k=12))
    token = db.Token()
    token.token = new_token_key
    token.user = token_rec.user
    token._type = 'change_password_post'
    token_rec.used = True
    g.db_session.add(token)
    g.db_session.commit()

    with open("charity/ui/pages/changePassword.html", "rt") as fin:
        with open("charity/ui/pages/temp/{}.html".format(new_token_key),
                  "wt") as fout:
            for line in fin:
                fout.write(line.replace('TOKEN_KEY', new_token_key))

    return redirect('/static/pages/temp/{}.html'.format(new_token_key))


@bp.route('/changepassword/<token>', methods=['POST'])
def _changepassword_post(token):
    # TODO: Check for expire time of token
    token_rec = g.db_session.query(db.Token).filter_by(
        token=token, _type='change_password_post', used=False).first()
    if not token_rec:
        return redirect('/static/pages/404.html')
    password = request.form['password']
    confrim_password = request.form['confrimPassword']
    if password != confrim_password:
        return 'Passwords Are Not Equal\
                <br><a href="javascript:history.back()">Go Back</a>'

    if len(password) < 8 or len(password) > 32:
        return 'Password Should Have More Than 8 Characters Or Less\
                Than 32 Characters<br><a href="javascript:history.\
                back()">Go Back</a>'

    hash_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    pass_history = g.db_session.query(db.PasswordHistory).filter_by(
        user=token_rec.user, password=hash_password).first()
    if pass_history:
        return 'You Cant Use Your Old Password Twice.\
                Please Pick Another Password<br>\
                <a href="javascript:history.back()">Go Back</a>'

    token_rec.user.password = hash_password
    token_rec.used = True
    token_rec.user.force_to_change_password = False
    add_password_history(token_rec.user, hash_password)
    g.db_session.commit()

    file_name = "charity/ui/pages/temp/{}.html".format(token_rec.token)
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        # TODO: Set log for this
        print("The file does not exist")

    set_log(
        token_rec.user,
        'Change Password Done Successfuly'
    )
    return redirect('/static/pages/changePasswordSuccess.html')


@bp.route('/change-role', methods=['POST'])
@jwt_required
@acc('admin', 'change_user_roles')
def change_role():
    data = json.loads(request.data)
    role = g.db_session.query(db.Role).filter_by(id=data['id']).first()
    if role.name == 'admin':
        raise ErrorToClient('Cant Change Admin User')
    user = g.db_session.query(db.User).filter_by(id=data['user_id']).first()
    user_role = g.db_session.query(db.UserRole).filter_by(
        user_id=user.id, role_id=role.id).first()
    _type = 'Delete'
    if user_role:
        g.db_session.delete(user_role)
    else:
        user.roles.append(role)
        _type = 'Assign'
    g.db_session.commit()
    set_log(
        g.db_session.query(db.User).filter_by(id=g.user_id).first(),
        'Change Role - User: {}, User id: {}, {} role: {}'.format(
            user.name, user.id, _type, role.label)
    )
    return jsonify({'msg': '{} {} Successfuly'.format(role.label, _type)})


@bp.route('/changeactivation', methods=['POST'])
@jwt_required
@acc('admin', 'change_user_activation')
def change_activation():
    data = json.loads(request.data)
    user = g.db_session.query(db.User).filter_by(
        id=data['user_id']).first()
    _type = 'Active'
    if user.active:
        _type = 'Deactive'
        user.active = False
    else:
        user.active = True
    g.db_session.commit()
    set_log(
        g.db_session.query(db.User).filter_by(id=g.user_id).first(),
        'Change User Activation - User: {}, User id: {}, Change To: {}'.format(
            user.name, user.id, _type)
    )
    return jsonify({'msg': '{} {} Successfuly'.format(user.name, _type)})
