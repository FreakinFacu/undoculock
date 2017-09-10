import uuid
from datetime import datetime

from flask import url_for

from app.models import db


class Shares(db.Model):
    # Define Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    share_key = db.Column(db.String(255), index=True)
    type = db.Column(db.String(10))
    key = db.Column(db.String(255))
    state = db.Column(db.String(10))

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    TYPE_FACEBOOK = "facebook"
    TYPE_EMAIL = "email"
    TYPE_SMS = "sms"

    # user = db.relationship('Users', foreign_keys='Files.user_id',  primaryjoin="Users.id == Shares.user_id")

    STATE_ACTIVE = "active"
    STATE_DELETED = "deleted"

    @staticmethod
    def create(user_id, type, key):
        share = Shares()
        share.user_id = user_id
        share.type = type
        share.key = key
        share.share_key = str(uuid.uuid4())
        share.state = Shares.STATE_ACTIVE

        # Save the user
        share.save()
        return share

    @staticmethod
    def get_by_share_key(share_key):
        """

        :param share_key:
        :return: Shares
        :rtype Shares
        """
        return Shares.query.filter_by(share_key=share_key).first()

    def is_active(self):
        return self.state == Shares.STATE_ACTIVE

    def get_link(self):
        generated_link = url_for("home.view_shared", key=self.share_key, _external=True)
        print(generated_link)
        return generated_link

    def save(self):
        db.session.add(self)
        db.session.commit()
