import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from swim_log import app, db, bcrypt
from swim_log.forms import RegistrationForm, LoginForm, UpdateAccountForm, LogSwim
from swim_log.models import User, Session
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route("/history")
@login_required
def history():
    sessions = Session.query.all()
    return render_template('history.html', title='History', sessions=sessions)


@app.route("/swim/new", methods=['GET', 'POST'])
@login_required
def log_swim():
    form = LogSwim()
    if form.validate_on_submit():
        logged_swim = Session(session_date=form.session_date.data, swim_type=form.swim_type.data, swim_stroke=form.swim_stroke.data, swim_distance=form.swim_distance.data, swim_time=form.swim_time.data, swimmer=current_user)
        db.session.add(logged_swim)
        db.session.commit()
        flash('Your swim has been succesfully logged.', 'success')
        return redirect(url_for('history'))
    return render_template('log_swim.html', title='Log Swim', form=form, legend='Log Swim')


@app.route("/swim/<int:session_id>")
@login_required
def session(session_id):
    session = Session.query.get_or_404(session_id)
    return render_template('swim.html', title=session.session_date, session=session)


@app.route("/swim/<int:session_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('session', session_id=session.id))
    elif request.method == 'GET':
        form.session_date.data = session.session_date
        form.swim_type.data = session.swim_type
    form.swim_stroke.data = session.swim_stroke
    form.swim_distance.data = session.swim_distance
    form.swim_time.data = session.swim_time
    return render_template('log_swim.html', title='Update Swim', form=form, legend='Update Swim')


@app.route("/swim/<int:session_id>/delete", methods=['POST'])
@login_required
def delete_swim(session_id):
    session = Session.query.get_or_404(session_id)
    if session.swimmer != current_user:
        abort(403)
    db.session.delete(session)
    db.session.commit()
    flash('Your swim session has been deleted.', 'success')
    return redirect(url_for('history'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created - you may now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful, please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)
