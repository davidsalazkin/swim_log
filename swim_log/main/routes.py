from flask import Blueprint
from flask import render_template, request
from swim_log.models import Session
from flask_login import login_required


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@main.route("/history")
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    sessions = Session.query.order_by(Session.session_date.desc()).paginate(page=page, per_page=5)
    return render_template('history.html', title='History', sessions=sessions)
