from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/fb')
def fb():
    return render_template('home/fb.html')
