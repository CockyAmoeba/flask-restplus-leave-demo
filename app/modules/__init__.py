from . import users
from . import roles
from . import leave


def init_app(app):
    """
    Application modules initialization.
    """
    for module in (
            users,
            roles,
            leave
    ):
        module.init_app(app)
