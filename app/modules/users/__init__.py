"""
Users module
============
"""

from app.restplus import api_v1


def init_app(app):
    # pylint: disable=unused-argument,unused-variable
    """
    Init users module.
    """
    # Touch underlying modules
    from . import resources

    api_v1.add_namespace(resources.ns)
