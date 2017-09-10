from datetime import datetime

from app.models import db


class Files(db.Model):
    # Define Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    filepath = db.Column(db.String(255), default='', nullable=False)
    type = db.Column(db.String(255), default='', nullable=False)
    state = db.Column(db.String(10))

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    # user = db.relationship('Users', foreign_keys='Files.user_id',  primaryjoin="Users.id == Files.user_id")

    STATE_ACTIVE = "active"
    STATE_DELETED = "deleted"

    @staticmethod
    def create(user_id, filepath, upload_type):
        file = Files()
        file.user_id = user_id
        file.filepath = filepath
        file.type = upload_type
        file.state = Files.STATE_ACTIVE

        # Save the user
        file.save()

        return file

    @staticmethod
    def get_by_id(file_id):
        return Files.query.filter_by(id=file_id).first()

    def delete(self):
        # TODO make file call to erase file
        self.state = Files.STATE_DELETED
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
