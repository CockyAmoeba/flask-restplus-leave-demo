from . import users


def init_app(app):
    """
    Application extensions initialization.
    """
    users.init_app(app)
