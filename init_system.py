from sqlalchemy.orm import scoped_session
from charity.database import db as db
import sys
import hashlib

session = scoped_session(db.Session)

all_roles = [
    {
        'name': 'admin',
        'label': 'Admin',
        'is_systemic': False
    },
    {
        'name': 'employee',
        'label': 'Employee',
        'is_systemic': False
    },
    {
        'name': 'change_user_activation',
        'label': 'Allow To Change User Activation',
        'is_systemic': False
    },
    {
        'name': 'change_user_roles',
        'label': 'Allow To Change User Roles',
        'is_systemic': False
    },
    {
        'name': 'allow_create_user',
        'label': 'Allow To Create New User',
        'is_systemic': False
    },
    {
        'name': 'see_login_history',
        'label': 'Allow To See Users Login History',
        'is_systemic': False
    },
    {
        'name': 'allow_edit_data',
        'label': 'Allow To Edit All Data',
        'is_systemic': True
    },
    {
        'name': 'see_logs',
        'label': 'Allow To See And Search System Logs',
        'is_systemic': False
    },
    {
        'name': 'mail_verified',
        'label': 'Should verified Mail',
        'is_systemic': True
    }
]


def init_admin_user():
    pass


def create_roles(roles):
    _roles = list()
    for role in roles:
        rec = session.query(db.Role).filter_by(name=role['name']).first()
        if not rec:
            new_role = db.Role(
                name=role['name'],
                label=role['label'],
                is_systemic=role['is_systemic'])
            if role['is_systemic'] is False:
                _roles.append(new_role)
            session.add(new_role)
        else:
            if role['is_systemic'] is False:
                _roles.append(rec)
    session.commit()
    return _roles


def create_admin_user(args):
    mail = str(args[1])
    username = str(args[2])
    password = str(args[3])
    print(mail, username, password)

    user = session.query(db.User).filter_by(
        user_type='admin').first()

    if user:
        raise Exception('User Admin Exist')

    admin = db.User()
    admin.mail = mail
    admin.username = username
    admin.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    admin.roles = [*create_roles(all_roles)]
    admin.user_type = 'admin'
    admin.name = 'admin'
    admin.active = True

    session.add(admin)
    session.commit()
    print('Ok Done Successfuly')


if __name__ == "__main__":
    create_roles(all_roles)
    create_admin_user(sys.argv)
