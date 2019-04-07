from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from swim_log import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sessions = db.relationship('Session', backref='swimmer', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Session(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    session_date = db.Column(db.Date())
    swim_type = db.Column(db.String())
    swim_distance = db.Column(db.Integer())
    swim_stroke = db.Column(db.String())
    swim_time = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Session('{self.session_date}', '{self.swim_type}', {self.swim_distance}, '{self.swim_stroke}', {self.swim_time})"
