from flask import Blueprint, render_template, request, abort
from swim_log.models import Session, User
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home', legend='home')


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@main.route("/history/<string:username>")
@login_required
def history(username):
    if username != current_user.username:
        abort(403)
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    sessions = Session.query.filter_by(swimmer=user).order_by(Session.session_date.desc()).paginate(page=page, per_page=10)
    return render_template('history.html', title='History', sessions=sessions, user=user)
