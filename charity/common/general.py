from charity.database import db as db
from flask import g


def set_log(user, msg):
    log = db.Logger()
    log.user = user
    log.msg = msg
    g.db_session.add(log)
    g.db_session.commit()
