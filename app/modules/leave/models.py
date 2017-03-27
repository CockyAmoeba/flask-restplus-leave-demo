from app import db


class Leave(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'leave'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    days_of_leave = db.Column(db.Integer)
    status = db.Column(db.String(8), default='New')

    def __repr__(self):
        return '<Leave: UserId - {} StartDate - {}, EndDate - {}>'.format(self.user_id, self.start_date, self.end_date)