from flask_restplus import fields
from app.restplus import api_v1 as api

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='User email'),
    'username': fields.String(required=True, description='Username'),
    'first_name': fields.String(required=True, description='Users first name'),
    'last_name': fields.String(required=True, description='Users last name'),
    'password': fields.String(required=True, description='Users password')
})

user_with_details = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='User email'),
    'username': fields.String(required=True, description='Username'),
    'first_name': fields.String(required=True, description='Users first name'),
    'last_name': fields.String(required=True, description='Users last name'),
    'password_hash': fields.String(required=True, description='Users password'),
    'role_id': fields.Integer(attribute='role.id'),
    'role': fields.String(attribute='role.id'),
    'create_date': fields.DateTime
})

page_of_users = api.inherit('Page of users', pagination, {
    'items': fields.List(fields.Nested(user_with_details))
})

role = api.model('User role', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user role'),
    'name': fields.String(required=True, description='Role name'),
    'description': fields.String(required=True, description='Role description')
})

page_of_roles = api.inherit('Page of roles', pagination, {
    'items': fields.List(fields.Nested(role))
})

role_with_users = api.inherit('Role with users', role, {
    'users': fields.List(fields.Nested(user))
})

user_role = api.model('User role assignment', {
    'id': fields.Integer(required=True, description='Role id to be assigned to user')
})
