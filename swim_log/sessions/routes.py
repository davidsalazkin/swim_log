from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from swim_log import db
from swim_log.sessions.forms import LogSwim
from swim_log.models import Session
from flask_login import current_user, login_required


sessions = Blueprint('sessions', __name__)


@sessions.route("/swim/new", methods=['GET', 'POST'])
@login_required
def log_swim():
    form = LogSwim()
    if form.validate_on_submit():
        logged_swim = Session(session_date=form.session_date.data, swim_type=form.swim_type.data, swim_stroke=form.swim_stroke.data, swim_distance=form.swim_distance.data, swim_time=form.swim_time.data, swimmer=current_user)
        db.session.add(logged_swim)
        db.session.commit()
        flash('Your swim has been succesfully logged.', 'success')
        return redirect(url_for('main.history'))
    return render_template('log_swim.html', title='Add Swim', form=form, legend='Add Swim')


@sessions.route("/swim/<int:session_id>")
@login_required
def session(session_id):
    session = Session.query.get_or_404(session_id)
    return render_template('swim.html', title=session.session_date, session=session)


@sessions.route("/swim/<int:session_id>/update", methods=['GET', 'POST'])
@login_required
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.swimmer != current_user:
        abort(403)
    form = LogSwim()
    if form.validate_on_submit():
        session.session_date = form.session_date.data
        session.swim_type = form.swim_type.data
        session.swim_stroke = form.swim_stroke.data
        session.swim_distance = form.swim_distance.data
        session.swim_time = form.swim_time.data
        db.session.commit()
        flash('Your swim session has been updated.', 'success')
        return redirect(url_for('sessions.session', session_id=session.id))
    elif request.method == 'GET':
        form.session_date.data = session.session_date
        form.swim_type.data = session.swim_type
    form.swim_stroke.data = session.swim_stroke
    form.swim_distance.data = session.swim_distance
    form.swim_time.data = session.swim_time
    return render_template('log_swim.html', title='Update Swim', form=form, legend='Update Swim')


@sessions.route("/swim/<int:session_id>/delete", methods=['POST'])
@login_required
def delete_swim(session_id):
    session = Session.query.get_or_404(session_id)
    if session.swimmer != current_user:
        abort(403)
    db.session.delete(session)
    db.session.commit()
    flash('Your swim session has been deleted.', 'success')
    return redirect(url_for('main.history'))
