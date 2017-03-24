"""
RESTful API User resources
--------------------------
"""

import logging

from flask import request
from flask_restplus import Resource
from app.restplus import api_v1
from .models import db, User

log = logging.getLogger(__name__)
ns = api_v1.namespace('users', description="Operations related to Users")


@ns.route('/')
class Users(Resource):
    """
    Manipulations with users.
    """

    def get(self):
        """
        List of users.

        Returns a list of users starting from ``offset`` limited by ``limit``
        parameter.
        """
        return User.query.all()
