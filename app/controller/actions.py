import time

from dropbox import dropbox
from flask import Blueprint, request
from flask.ext.login import login_required
from werkzeug.utils import secure_filename

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
