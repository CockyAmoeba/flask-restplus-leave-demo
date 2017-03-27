"""
RESTful API Role resources
--------------------------
"""

import logging

from flask import request
from flask_restplus import Resource
from app.restplus import api_v1 as api
from .models import db, Role
from app.modules.serializers import page_of_roles, role, role_with_users
from app.modules.parsers import pagination_arguments

log = logging.getLogger(__name__)
ns = api.namespace('roles', description="Operations related to Roles")


@ns.route('/')
class Roles(Resource):
    """
    Manipulations with roles.
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
    @api.response(201, 'Role successfully updated.')
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


@ns.route('/<int:id>')
@api.response(404, 'Role not found.')
class UserById(Resource):

    @api.marshal_with(role_with_users)
    def get(self, id):
        """
        Returns a user by id.
        """
        return Role.query.filter(Role.id == id).one()

    @api.expect(role, validate=True)
    @api.response(204, 'Role successfully updated.')
    def put(self, id):
        """
        Updates a user and assign a specific role by id.
        """
        data = request.json
        role = Role.query.filter(Role.id == id).one()
        if 'description' in data:
            role.description = data.get('description')
        if 'name' in data:
            role.name = data.get('name')
        db.session.add(role)
        db.session.commit()
        return None, 204