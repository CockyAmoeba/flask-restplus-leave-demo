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
    'last_name': fields.String(required=True, description='Users last name')
})

user_with_password = api.inherit('User with password', user,  {
    'password': fields.String(required=True, description='Users password')
})

user_with_details = api.inherit('User with details', user, {
    'password_hash': fields.String(required=True, description='Users password'),
    'role_id': fields.Integer(attribute='role.id'),
    'role': fields.String(attribute='role.id'),
    'create_date': fields.DateTime,
    'leave_remaining': fields.Integer(required=True)
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
    'role_id': fields.Integer(required=True, description='Role id to be assigned to user')
})

leave = api.model('Leave Application', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a leave application'),
    'user_id': fields.Integer(required=True, description='Users Id of applicant'),
    'start_date': fields.DateTime(required=True, description='Start date of leave application',
                                  pattern='^(20\d{2})-(\d{2})-(\d{2})+$'),
    'end_date': fields.DateTime(required=True, description='End date of leave application',
                                pattern='^(20\d{2})-(\d{2})-(\d{2})+$'),
    'status': fields.String(required=True, description='Leave type (New, Approved, Declined)', default='New')
})

leave_for_user = api.model('Leave Application by user', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a leave application'),
    'start_date': fields.DateTime(required=True, description='Start date of leave application',
                                  pattern='^(20\d{2})-(\d{2})-(\d{2})+$'),
    'end_date': fields.DateTime(required=True, description='End date of leave application',
                                pattern='^(20\d{2})-(\d{2})-(\d{2})+$'),
    'status': fields.String(required=True, description='Leave type (New, Approved, Declined)', default='New')
})

leave_update_status = api.model('Leave Application status update', {
    'status': fields.String(required=True, description='Leave type (New, Approved, Declined)', pattern='^(Approved|Declined)+$')
})

leave_detail = api.model('Leave Application detail', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a leave application'),
    'user_id': fields.Integer(attribute='user.id'),
    'user': fields.String(attribute='user.id'),
    'start_date': fields.DateTime(description='Start date of leave application'),
    'end_date': fields.DateTime(description='End date of leave application'),
    'days_of_leave': fields.Integer(description='Length of leave in days'),
    'status': fields.String(description='Leave type (New, Approved, Declined)')
})

page_of_leave_applications = api.inherit('Page of leave applications', pagination, {
    'items': fields.List(fields.Nested(leave_detail))
})
