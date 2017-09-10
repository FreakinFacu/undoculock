from datetime import datetime

from app.models import db


class Users(db.Model):
    # Define Columns
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), default='', nullable=False)

    facebook_id = db.Column(db.String(255), index=True)

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    # Define Relationships
    files = db.relationship('Files', backref='user', lazy='dynamic')
    shares = db.relationship('Shares', backref='user', lazy='dynamic')
    alerts = db.relationship('Alerts', backref='user', lazy='dynamic')

    @staticmethod
    def create(name, facebook_id):
        existing = Users.get_by_fb_id(facebook_id)

        if existing is not None:
            return existing

        user = Users()
        user.name = name
        user.facebook_id = facebook_id

        # Save the user
        user.save()

        return user

    #
    # Flask-Login Functions
    #
    def is_authenticated(self):
        return True

    def is_active(self):
        # We'll have to check that the user hasn't been blocked
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """
        :return: From flask-login: MUST be a unicode
        """
        return str(self.id).encode()

    @staticmethod
    def get_from_unicode(user_id):
        """
        Not required as part of the user object but required for the user_loader decorator
        :param user_id:
        :type user_id: bytearray
        :return:
        """
        if isinstance(user_id, bytes):
            int_id = user_id.decode("utf-8", "strict")
        else:
            int_id = user_id

        user = Users.query.filter_by(id=int_id).first()
        return user

    #
    # End Flask-Login Functions
    #

    @staticmethod
    def get_by_fb_id(fb_id):
        return Users.query.filter_by(facebook_id=fb_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
