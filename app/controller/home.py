from flask import Blueprint, render_template
from flask import request

from app.models.shares import Shares

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/')
def index():
    return render_template('home/index.html')


@home_blueprint.route('/data')
def data():
    return render_template('home/data.html')


@home_blueprint.route('/info')
def info():
    return render_template('home/info.html')


@home_blueprint.route('/fb')
def fb():
    return render_template('home/fb.html')


@home_blueprint.route('/home')
def home():
    return render_template('home/home.html')


@home_blueprint.route('/view_shared')
def view_shared():
    share = Shares.get_by_share_key(request.args['key'])

    if share is None or not share.is_active():
        return "Oh noes"

    return render_template("home/view_shared.html", type=share.type, share_key=request.args['key'])
