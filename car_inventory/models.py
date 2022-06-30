from distutils.archive_util import make_archive
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner, lazy = True')

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"Congratulations, {self.email} is now in the database"

class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.String(100))
    top_speed = db.Column(db.String(100))
    max_horsepower = db.Column(db.String(100))
    seats = db.Column(db.String(100))
    price = db.Column(db.Numeric(precision=12, scale=2))
    length = db.Column(db.String(100))
    country = db.Column(db.String(100), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, year, top_speed, max_horsepower, seats, price, length, country, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.top_speed = top_speed
        self.max_horsepower = max_horsepower
        self.seats = seats
        self.price = price
        self.length = length
        self.country = country
        self.user_token = user_token

    def __repr__(self):
        return f"The following car has been added: {self.make}{self.model}"

    def set_id(self):
        return(secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'top_speed', 'max_horsepower', 'seats', 'price', 'length', 'country']

car_schema=(CarSchema())
cars_schema=(CarSchema(many=True))