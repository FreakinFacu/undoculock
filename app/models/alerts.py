from datetime import datetime

from twilio.rest import Client

from app.models import db
from app.models.shares import Shares


class Alerts(db.Model):
    # Define Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    number = db.Column(db.String(255), Nullable=False)
    message = db.Column(db.String(255), Nullable=False)
    send_time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    state = db.Column(db.String(10))

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    # user = db.relationship('Users', foreign_keys='Files.user_id',  primaryjoin="Users.id == Files.user_id")

    STATE_ACTIVE = "active"
    STATE_SENT = "sent"
    STATE_DELETED = "deleted"

    @staticmethod
    def create(user_id, number, message):
        alert = Alerts()
        alert.user_id = user_id
        alert.number = number
        alert.message = message
        alert.state = Alerts.STATE_ACTIVE

        # Save the user
        alert.save()

        # TODO check if we need to send it now or later
        alert.send_sms()

        return alert

    @staticmethod
    def get_by_id(file_id):
        return Alerts.query.filter_by(id=file_id).first()

    def create_link(self):
        share = Shares.create(self.user_id, Shares.TYPE_SMS, self.number)
        return share.get_link()

    def send_sms(self):
        self.state = Alerts.STATE_SENT
        self.save()

        body = "UndocuLock Alert from {name}: {message} {link}".format(
            name=self.user.name,
            message=self.message,
            link=self.create_link()
        )

        # Your Account SID from twilio.com/console
        account_sid = "AC3823d80d718fe7df303909472abc7ce1"
        # Your Auth Token from twilio.com/console
        auth_token = "772496176978bab257e321ad6cf13ccc"
        client = Client(account_sid, auth_token)
        client.messages.create(to=self.number, from_="12134938836", body=body)

    def delete(self):
        # TODO make file call to erase file
        self.state = Alerts.STATE_DELETED
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
