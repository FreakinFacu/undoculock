import uuid
from datetime import datetime

from flask import url_for
from twilio.rest import Client

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

    def send(self):
        if self.type == Shares.TYPE_SMS:
            self.send_sms()
        elif self.type == Shares.TYPE_EMAIL:
            self.get_link()
        elif self.type == Shares.TYPE_FACEBOOK:
            self.get_link()

    def send_sms(self):
        body = "UndocuLock shared from {name} {link}".format(
            name=self.user.name,
            link=self.get_link()
        )

        # Your Account SID from twilio.com/console
        account_sid = "AC3823d80d718fe7df303909472abc7ce1"
        # Your Auth Token from twilio.com/console
        auth_token = "772496176978bab257e321ad6cf13ccc"
        client = Client(account_sid, auth_token)
        client.messages.create(to=self.key, from_="12134938836", body=body)

    def save(self):
        db.session.add(self)
        db.session.commit()
