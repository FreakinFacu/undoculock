import json

from dropbox import dropbox
from flask import Blueprint, make_response, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from werkzeug.utils import redirect, secure_filename

from app.helpers.filepath import gen_file_name, get_display_filename_from_db
from app.models.files import Files
from app.models.shares import Shares
from app.models.users import Users

actions = Blueprint('actions', __name__, url_prefix='/actions')


@actions.route('/view')
def view():
    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    dbx.files_delete_v2()
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
    return "YAY"


@actions.route("/login", methods=["POST"])
def login():
    user = Users.create(request.json['name'], request.json['id'])
    login_user(user, True)
    return json.dumps({"redirectUrl": url_for("home.info")})


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

    Files.create(current_user.id, x.path_display, "Photo")
    return redirect(url_for("actions.stepthree"))


@actions.route("/stepthree")
@login_required
def stepthree():
    return render_template("temp/share.html")


@actions.route("/shareEmail", methods=["POST"])
@login_required
def shareEmail():
    share = Shares.create(current_user.id, Shares.TYPE_EMAIL, request.json['email'])
    return url_for("home.view_share", key=share.share_key)


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

    file_list = [{"name": get_display_filename_from_db(f), "id": f.id} for f in files]
    return json.dumps({"results": file_list})


@actions.route("/downloadFile", methods=["POST"])
def download_file():
    share = Shares.get_by_share_key(request.json['share_key'])

    if share is None or not share.is_active():
        return make_response(json.dumps({"error": "Unable to validate email"}), 400)

    if share.key != request.json['email']:
        return make_response(json.dumps({"error": "Unable to validate email"}), 400)

    file = Files.get_by_id(request.json['file_id'])

    dbx = dropbox.Dropbox('NIP9ZHfsSXcAAAAAAAASgJrQdNyIiEYDVWGyau04Wy-fupfVft3UyWaHZ16iJZAy')
    # dbx.files_delete_v2()
    link = dbx.files_get_temporary_link(file.filepath)

    return json.dumps({"redirectUrl": link.link})


@actions.route("/dothething")
def twillio():
    from twilio.rest import Client
    # Your Account SID from twilio.com/console
    account_sid = "AC3823d80d718fe7df303909472abc7ce1"
    # Your Auth Token from twilio.com/console
    auth_token = "772496176978bab257e321ad6cf13ccc"
    client = Client(account_sid, auth_token)
    message = client.messages.create(to="+17146869405", from_="12134938836", body="Hello from Python!")
    print(message.sid)
    return ""
