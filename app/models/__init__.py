from flask_sqlalchemy import SQLAlchemy

# Initialize the db here so we can use it around
db = SQLAlchemy()


def create_all():
    from .users import Users
    from .files import Files
    from .shares import Shares

    db.create_all()
