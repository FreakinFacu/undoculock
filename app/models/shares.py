import uuid
from datetime import datetime

from app.models import db


class Shares(db.Model):
    # Define Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    share_key = db.Column(db.String(255), index=True)
    state = db.Column(db.String(10))

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    user = db.relationship('Users', foreign_keys='Files.user_id')

    STATE_ACTIVE = "active"
    STATE_DELETED = "deleted"

    @staticmethod
    def create(user_id):
        share = Shares()
        share.user_id = user_id
        share.share_key = uuid.uuid4()
        share.state = Shares.STATE_ACTIVE

        # Save the user
        share.save()
        return share

    def save(self):
        db.session.add(self)
        db.session.commit()
