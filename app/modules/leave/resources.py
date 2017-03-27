"""
RESTful API Leave resources
--------------------------
"""

import logging

from flask import request
from flask_restplus import Resource
from app.restplus import api_v1 as api
from .models import db, Leave
from app.modules.users.models import User
from app.modules.serializers import page_of_leave_applications, leave, leave_detail, leave_update_status
from app.modules.parsers import pagination_arguments
from datetime import datetime, date, timedelta

log = logging.getLogger(__name__)
ns = api.namespace('leave', description="Operations related to leave applications")


@ns.route('/')
class LeaveCollection(Resource):
    """
    Manipulations with leave.
    """

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_leave_applications)
    def get(self):
        """
        List of leave.

        Returns a list of leave applications starting from ``page`` limited by ``per_page``
        parameter.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        leave_query = Leave.query
        leave_page = leave_query.paginate(page, per_page, error_out=False)

        return leave_page

    @api.expect(leave, validate=True)
    @api.response(201, 'Leave application successfully created.')
    def post(self):
        """
        Registers a new leave application.
        """
        data = request.json

        user_id = data.get('user_id')
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


@ns.route('/<int:id>')
@api.response(404, 'Leave application not found.')
class LeaveById(Resource):

    @api.marshal_with(leave_detail)
    def get(self, id):
        """
        Returns a leave application by id.
        """
        return Leave.query.filter(Leave.id == id).one()

    @api.expect(leave_update_status, validate=True)
    @api.response(204, 'Leave application successfully updated.')
    def put(self, id):
        """
        Updates a leave application and updates the owning users remaining leave days accordingly
        """
        data = request.json
        leave = Leave.query.filter(Leave.id == id).one()
        status = data.get('status')

        if status == 'Approved' and leave.status == 'New':
            user = User.query.filter(User.id == leave.user_id).one()
            user.leave_remaining -= leave.days_of_leave
        elif status == 'Declined' and leave.status == 'Approved':
            user = User.query.filter(User.id == leave.user_id).one()
            user.leave_remaining += leave.days_of_leave

        leave.status = status

        db.session.add(leave)
        db.session.add(user)
        db.session.commit()
        return None, 204
