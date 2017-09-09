from flask import Flask
from flask.ext.login import LoginManager

from app.controller.actions import actions
from app.controller.home import home
from app.models import db, create_all
from app.models.users import Users

app = Flask(__name__)
app.debug = True

# Register Blueprints
app.register_blueprint(home)
app.register_blueprint(actions)

# Secret Key
app.secret_key = "Some secret key that will actually be secret at some point"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///temp/test.db"
db.init_app(app)

# login things
login_manager = LoginManager()
login_manager.login_view = "home.index"
login_manager.init_app(app)
app.config['REMEMBER_COOKIE_HTTPONLY'] = True


@login_manager.user_loader
def load_user(user_id):
    user = Users.get_from_unicode(user_id)
    return user


if __name__ == '__main__':
    with app.app_context():
        create_all()

    app.debug = True
    app.run(host='127.0.0.1')
