from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.helpers.filepath import get_display_filename_from_db, get_display_type
from app.models.shares import Shares

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/')
def index():
    return render_template('home/index.html')


@home_blueprint.route('/data')
def data():
    return render_template('home/data.html')


@home_blueprint.route('/complete')
def complete():
    return "You're done sharing"


@home_blueprint.route('/info')
@login_required
def info():
    file_list = [{
                     "name": get_display_filename_from_db(f),
                     "id": f.id,
                     "type": get_display_type(f)
                 } for f in current_user.files]

    return render_template('home/info.html', name=current_user.name, files=file_list)


@home_blueprint.route('/alerts')
@login_required
def alerts():
    alert_list = [{
                     "message": a.message,
                     "id": a.id,
                     "number": a.number,
                     "state": a.state
                 } for a in current_user.alerts]

    return render_template('home/alerts.html', alerts=alert_list)


@home_blueprint.route('/fb')
def fb():
    return render_template('home/fb.html')


@home_blueprint.route('/home')
def home():
    return render_template('home/home.html')


@home_blueprint.route('/view_shared')
def view_shared():
    if 'key' not in request.args:
        share_key = "magic"
        share_type = "email"
    else:
        share_key = request.args['key']
        share = Shares.get_by_share_key(share_key)

        if share is None or not share.is_active():
            return "Oh noes"

        share_type = share.type
    return render_template("home/view_shared.html", type=share_type, share_key=share_key)
