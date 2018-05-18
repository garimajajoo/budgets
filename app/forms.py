# this file consists of all the forms used in the htmlfiles

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, FloatField, DateField
from wtforms.validators import DataRequired
from app.models import User, Budget, LineItem
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Register')

class CreateBudget(FlaskForm):
	budget_name = StringField('Budget Name', validators=[DataRequired()])
	submit = SubmitField('Create New Budget')

class ViewBudget(FlaskForm):
	viewsubmit = SubmitField('View')

class EditBudget(FlaskForm):
	editsubmit = SubmitField('Edit')

class DeleteBudget(FlaskForm):
	deletesubmit = SubmitField('Delete')

class ShareBudget(FlaskForm):
	shareuser=StringField('Enter a username to share budget')
	sharesubmit = SubmitField('Share')

class Categories(FlaskForm):
	line_item1 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount1 = FloatField()
	line_item2 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount2 = FloatField()
	line_item3 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount3 = FloatField()
	line_item4 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount4 = FloatField()
	line_item5 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount5 = FloatField()
	line_item6 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount6 = FloatField()
	line_item7 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount7 = FloatField()
	line_item8 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount8 = FloatField()
	line_item9 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount9 = FloatField()
	line_item10 = SelectField(choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount10 = FloatField()
	submit = SubmitField()

class Expenses(FlaskForm):
	category = SelectField('Category',choices = [('blank', ''), ('Rent','Rent'), ('Groceries','Groceries'), ('Utilities','Utilities'), ('Car','Car'), ('Travel','Travel'), ('Clothing','Clothing'), ('Eating Out','Eating Out'), ('Education','Education'), ('Other','Other')])
	amount = FloatField('Amount')
	expensesubmit = SubmitField('Submit')