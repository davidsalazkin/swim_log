from swim_log import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sessions = db.relationship('Session', backref='swimmer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.Date, unique=True, nullable=False)
    session_length = db.Column(db.Integer, nullable=False)
    session_distance = db.Column(db.Integer, nullable=False)
    swims = db.relationship('Swim', backref='swim_session', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Session('{self.session_date}', '{self.session_length}', '{self.session_distance}')"


class Swim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swim_distance = db.Column(db.Integer, nullable=False)
    swim_stroke = db.Column(db.String, nullable=False)
    swim_time = db.Column(db.Integer)
    swim_type = db.Column(db.String, default='Working')
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)

    def __repr__(self):
        return f"Swim('{self.swim_distance}', '{self.swim_stroke}', '{self.swim_time}', '{self.swim_type}')"
