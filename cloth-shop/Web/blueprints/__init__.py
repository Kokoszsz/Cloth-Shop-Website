from flask import current_app

from database import SessionFactory


def db_Session() -> SessionFactory:
    return current_app.extensions['db_Session']
