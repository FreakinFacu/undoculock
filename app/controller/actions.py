import json
import time

from dropbox import dropbox
from flask import Blueprint, request
from flask import make_response
from flask import render_template
from flask import url_for
from flask.ext.login import current_user
from flask_login import login_required, login_user
from werkzeug.utils import secure_filename, redirect

from app.models.files import Files
from app.models.shares import Shares
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


@actions.route("/steptwo", methods=["GET"])
@login_required
def steptwo():
    return render_template("temp/file.html")


@actions.route('/uploadFile', methods=['POST'])
@login_required
def upload2():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filename = gen_file_name(current_user.id, filename)

    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    x = dbx.files_upload(file.stream.read(), filename)
    print(str(x))

    Files.create(current_user.id, x.path_display)
    # return responses.create_success_with_data({'url': image_url})
    return redirect(url_for("actions.stepthree"))


@actions.route("/stepthree")
@login_required
def stepthree():
    return render_template("temp/share.html")


@actions.route("/shareEmail", methods=["POST"])
@login_required
def shareEmail():
    share = Shares.create(current_user.id, Shares.TYPE_EMAIL, request.json['email'])
    return url_for("actions.shareTheLoad", key=share.share_key)


@actions.route("/shareLink")
def shareTheLoad():
    share = Shares.get_by_share_key(request.args['key'])

    if share is None or not share.is_active():
        return "Oh noes"

    return render_template("temp/load.html", type=share.type, share_key=request.args['key'])


@actions.route("/verifyEmail", methods=["POST"])
def verifyEmail():
    share = Shares.get_by_share_key(request.json['share_key'])

    if share is None or not share.is_active():
        return make_response(json.dumps({"error": "Unable to validate email"}), 400)

    if share.key != request.json['email']:
        return make_response(json.dumps({"error": "Unable to validate email"}), 400)

    files = share.user.files

    file_list = [{"filepath": f.filepath, "id": f.id} for f in files]
    return json.dumps({"results": file_list})
