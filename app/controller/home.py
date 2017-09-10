from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home/index.html')
<<<<<<< HEAD
def data():
    return render_template('home/data.html')
def info():
    return render_template('home/info.html')
=======


@home.route('/fb')
def fb():
    return render_template('home/fb.html')
>>>>>>> origin/master
