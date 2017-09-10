import json
import time

from dropbox import dropbox
from flask import Blueprint, request
from flask import render_template
from flask import url_for
from flask_login import login_required, login_user
from werkzeug.utils import secure_filename

from app.models.users import Users

actions = Blueprint('actions', __name__, url_prefix='/actions')


@actions.route('/upload')
def file_upload():
    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    with open("readme.md", 'rb') as stream:
        dbx.files_upload(stream.read(), "/readme.md")

    return str(dbx.users_get_current_account())

    # return "Hello Facu"
    # return render_template('home/file_upload.html')


def gen_file_name(user_id, filename):
    new_name = "/%d/%d.%s" % (user_id, int(time.time()), filename)
    return new_name


@actions.route('/view')
def view():
    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    link = dbx.files_get_temporary_link("/readme.md")
    return link.link


@actions.route('/imageUpload', methods=['POST'])
@login_required
def upload():
    file = request.files['files']

    filename = secure_filename(file.filename)
    filename = gen_file_name(filename)

    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    dbx.files_upload(file.stream.read(), filename)
    # return responses.create_success_with_data({'url': image_url})
    return "YAY"


@actions.route("/")
def index():
    return render_template('temp/index.html')


@actions.route("/login", methods=["POST"])
def login():
    user = Users.create(request.json['name'], request.json['id'])
    login_user(user, True)
    return json.dumps({"redirectUrl": url_for("actions.steptwo")})


@actions.route("/steptwo")
@login_required
def steptwo():
    return "YOU'RE LOGGED IN"
