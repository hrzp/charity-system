import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import time

engine = sa.create_engine('postgresql://reza:1234@localhost/charity',
                          convert_unicode=True, echo=False, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.bind = engine


def _get_timestamp():
    return time.time()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Unicode, unique=True, nullable=False)
    password = sa.Column(sa.Unicode, nullable=False)
    name = sa.Column(sa.Unicode, nullable=False)
    mail = sa.Column(sa.Unicode, nullable=False, unique=True)
    mail_verified = sa.Column(sa.Boolean, default=False)
    user_type = sa.Column(sa.Unicode, nullable=False)
    active = sa.Column(sa.Boolean, default=False)
    force_to_change_password = sa.Column(sa.Boolean, default=True)
    roles = relationship('Role', secondary='user_role',
                         backref=backref('user', lazy='dynamic'))
    c_date = sa.Column(sa.DateTime, default=datetime.now())


# Define the UserRoles data model
class UserRole(Base):
    __tablename__ = 'user_role'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    role_id = sa.Column(sa.Integer, sa.ForeignKey('role.id'))


# Define the Role data model
class Role(Base):
    __tablename__ = 'role'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode, unique=True)
    label = sa.Column(sa.Unicode, unique=True)
    is_systemic = sa.Column(sa.Boolean, default=False)

    def __init__(self, name=None, label=None, is_systemic=None):
        self.name = name
        self.label = label
        self.is_systemic = is_systemic

    def __repr__(self):
        return self.name


class Token(Base):
    __tablename__ = 'token'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = relationship('User')
    token = sa.Column(sa.String(512))
    c_time_stamp = sa.Column(sa.Float, default=_get_timestamp)
    _type = sa.Column(sa.String(32))
    used = sa.Column(sa.Boolean, default=False)
    c_date = sa.Column(sa.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Token %s>' % (self.token)


class LoginHistory(Base):

    """
        Save the user login info.
        `last_login` is a timestap format
    """
    __tablename__ = 'login_history'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = relationship('User')
    last_login_date = sa.Column(sa.DateTime, default=datetime.now())
    ip = sa.Column(sa.String(256))
    browser = sa.Column(sa.String(256))
    full_browser_info = sa.Column(sa.String(4096))
    c_date = sa.Column(sa.DateTime, default=datetime.now())


class Logger(Base):
    """
        Log all action in this table
    """
    __tablename__ = 'logger'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = relationship('User')
    msg = sa.Column(sa.String(1024))
    c_time_stamp = sa.Column(sa.FLOAT, default=_get_timestamp())
    c_date = sa.Column(sa.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Action %r>' % (self.msg)


class PasswordHistory(Base):
    __tablename__ = 'password_history'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    user = relationship('User')
    password = sa.Column(sa.String(255), nullable=False)
    c_date = sa.Column(sa.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % (self.user)


Base.metadata.create_all()
