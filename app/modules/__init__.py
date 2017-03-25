from . import users
from . import roles


def init_app(app):
    """
    Application modules initialization.
    """
    for module in (
            users,
            roles
    ):
        module.init_app(app)
