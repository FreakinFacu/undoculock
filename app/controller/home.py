from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/data')
def data():
    return render_template('home/data.html')


@home.route('/info')
def info():
    return render_template('home/info.html')


@home.route('/fb')
def fb():
    return render_template('home/fb.html')


@home.route('/home')
def home():
    return render_template('home/home.html')
