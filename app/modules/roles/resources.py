"""
RESTful API Role resources
--------------------------
"""

import logging

from flask import request
from flask_restplus import Resource
from app.restplus import api_v1 as api
from .models import db, Role
from app.modules.serializers import page_of_roles, role
from app.modules.parsers import pagination_arguments

log = logging.getLogger(__name__)
ns = api.namespace('roles', description="Operations related to Roles")


@ns.route('/')
class Roles(Resource):
    """
    Manipulations with users.
    """

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_roles)
    def get(self):
        """
        List of roles.

        Returns a list of roles starting from ``page`` limited by ``per_page``
        parameter.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        role_query = Role.query
        roles_page = role_query.paginate(page, per_page, error_out=False)

        return roles_page

    @api.expect(role, validate=True)
    @api.response(204, 'Role successfully updated.')
    def post(self):
        """
        Registers a new role.
        """
        data = request.json

        name = data.get('name')
        description = data.get('description')
        role = Role(name=name,
                    description=description)
        db.session.add(role)
        db.session.commit()

        return None, 201