"""
Leave Application module
============
"""

from app.restplus import api_v1


def init_app(app):
    """
    Init users module.
    """
    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.ns)
