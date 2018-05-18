# this file contains the setups for all the tables used
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))


	def __repr__(self):
		return self.username

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Budget(db.Model):
	__tablename__ = 'budgets'
	id = db.Column(db.Integer, primary_key=True)
	budget_name = db.Column(db.String(100))
	username = db.Column(db.String(64))
	shared_by = db.Column(db.String(64))
    
	def __repr__(self):
		return self.budget_name

class LineItem(db.Model):
	__tablename__= 'lineitems'
	id=db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(50))
	amount = db.Column(db.Float(precision=2))
	budget_name=db.Column(db.String(100))
	username = db.Column(db.String(64))

class Spending(db.Model):
	__tablename__='spending'
	id=db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64))
	category=db.Column(db.String(50))
	amount = db.Column(db.Float(precision=2))
	date=db.Column(db.Date)

class Threads(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64))
	thread_name = db.Column(db.String(100))

class Comments(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(64))
	comment=db.Column(db.String(1000))
	thread_name=db.Column(db.String(100))

@login.user_loader
def load_user(id):
	return User.query.get(int(id))