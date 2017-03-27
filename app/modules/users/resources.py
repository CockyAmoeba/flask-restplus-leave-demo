"""
RESTful API User resources
--------------------------
"""

import logging

from flask import request
from flask_restplus import Resource
from app.restplus import api_v1 as api
from .models import db, User
from app.modules.roles.models import Role
from app.modules.leave.models import Leave
from app.modules.serializers import page_of_users, user, user_with_details, role, user_role, \
    page_of_leave_applications, leave, user_with_password, leave_for_user
from app.modules.parsers import pagination_arguments
from datetime import datetime, timedelta

log = logging.getLogger(__name__)
ns = api.namespace('users', description="Operations related to Users")


@ns.route('/')
class Users(Resource):
    """
    Manipulations with users.
    """

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_users)
    def get(self):
        """
        List of users.

        Returns a list of users starting from ``page`` limited by ``per_page``
        parameter.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        users_query = User.query
        users_page = users_query.paginate(page, per_page, error_out=False)

        return users_page

    @api.expect(user_with_password, validate=True)
    @api.response(201, 'User successfully updated.')
    def post(self):
        """
        Registers a new user.
        """
        data = request.json

        email = data.get('email')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        user = User(email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password)
        db.session.add(user)
        db.session.commit()

        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'User not found.')
class UserById(Resource):
    @api.marshal_with(user_with_details)
    def get(self, id):
        """
        Returns a user by id.
        """
        return User.query.filter(User.id == id).one()


@ns.route('/<string:username>')
@api.response(404, 'User not found.')
class UserByUsername(Resource):
    @api.marshal_with(user_with_details)
    def get(self, username):
        """
        Returns a user by their username.
        """
        return User.query.filter(User.username == username).one()


@ns.route('/<string:email>')
@api.response(404, 'User not found.')
class UserByEmail(Resource):
    @api.marshal_with(user_with_details)
    def get(self, email):
        """
        Returns a user by email.
        """
        return User.query.filter(User.email == email).one()


@ns.route('/<int:id>/role')
@api.response(404, 'User not found.')
class UserRole(Resource):
    @api.marshal_with(role)
    def get(self, id):
        """
        Returns the role associated with a user by their id.
        """
        return User.query.filter(User.id == id).one().role

    @api.expect(user_role, validate=True)
    @api.response(204, 'User role successfully updated.')
    def put(self, id):
        """
        Updates a user and assign a specific role by id.
        """
        data = request.json
        user = User.query.filter(User.id == id).one()
        role = Role.query.filter(Role.id == data.get('role_id')).one()
        user.role = role
        db.session.add(user)
        db.session.commit()
        return None, 204


@ns.route('/<int:id>/leave')
class UserLeave(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_leave_applications)
    def get(self, id):
        """
        Returns a leave applications for a user by their id
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        leave_query = Leave.query
        leave_page = leave_query.filter(Leave.user_id == id).paginate(page, per_page, error_out=False)
        return leave_page

    @api.expect(leave_for_user, validate=True)
    @api.response(201, 'Leave application successfully created.')
    def post(self, id):
        """
        Registers a new leave application for the given user with id.
        """
        data = request.json

        user_id = id
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')

        if end_date < start_date:
            return {'message': 'End date cannot be prior to start date'}, 406

        daygenerator = (start_date + timedelta(x + 1) for x in range((end_date - start_date).days + 1))
        days_of_leave = sum(1 for day in daygenerator if day.weekday() < 5)

        leaveEntry = Leave(user_id=user_id,
                           start_date=start_date,
                           end_date=end_date,
                           days_of_leave=days_of_leave)

        db.session.add(leaveEntry)
        db.session.commit()

        return None, 201
