from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Creating DB instance
db = SQLAlchemy(app, session_options={'autocommit': True})


# USER class
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(100), nullable=False)
    initial_balance = db.Column(db.Integer,nullable=False)

    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.user_name


# BOOK Class
class Book(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable=False)
    author_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Book %r>' % self.title


# USERBOOK class
class UserBook(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def add(self):
        db.session.begin()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Book %r>' % self.user_id


class Wallet(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
