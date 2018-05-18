from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm, RegisterForm, CreateBudget, Categories, ViewBudget, EditBudget, DeleteBudget, Expenses, ShareBudget
from app.models import User, Budget, LineItem, Spending, Threads, Comments
from flask_login import current_user, login_user
from flask_login import logout_user
import datetime
import html
from decimal import Decimal
import pygal


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
	#instantiates all the forms
	createform = CreateBudget()
	viewform = ViewBudget()
	editform = EditBudget()
	deleteform = DeleteBudget()
	expenseform = Expenses()
	shareform = ShareBudget()
	share=0
	#puts all the budgets for a user in a list to display in html
	budgets = Budget.query.filter_by(username=current_user.username)
	budgets2 = []
	#a list of all the usernames that have shared a budget with this user
	shared = []
	for b in budgets:
		budgets2+=[str(b.budget_name)]
		shared+=[b.shared_by]
	#counts the number of budgets that a user has
	count = Budget.query.filter_by(username=current_user.username).count()
	
	differences = {}
	
	#if the createform is validated, the budget is added to the Budgets table and the user is redirected to a file that will allow the user to specify the details of the budget
	if createform.validate_on_submit():
		name = createform.budget_name.data
		buds = Budget.query.filter_by(username=current_user.username)
		for a in buds:
			if a.budget_name==name:
				flash('A budget with this name already exists')
				return redirect('/index')
		b=Budget(budget_name=createform.budget_name.data, username=current_user.username)
		db.session.add(b)
		db.session.commit()
		bud = Budget.query.filter_by(username=current_user.username, budget_name=name)
		for a in bud:
			id =str(a.id)
		return redirect('/createbudget/'+id)

	#creates a graph that compares all the budgets in a stacked bar graph
	if "comparebudgets" in request.form:
		rent_dict = {}
		utilities_dict = {}
		groceries_dict = {}
		car_dict = {}
		travel_dict = {}
		clothing_dict = {}
		eatingout_dict = {}
		education_dict = {}
		other_dict = {}

		line_chart = pygal.StackedBar()
		line_chart.title = 'Comparison of All Budgets'
		line_chart.x_labels=budgets2

		for b in budgets2:
			rent_dict[b]=0
			utilities_dict[b]=0
			groceries_dict[b]=0
			car_dict[b]=0
			travel_dict[b]=0
			clothing_dict[b]=0
			eatingout_dict[b]=0
			education_dict[b]=0
			other_dict[b]=0

			lines = LineItem.query.filter_by(username=current_user.username, budget_name=b)
			for l in lines:
				if l.category == 'Rent':
					rent_dict[b] += l.amount
				if l.category == 'Utilities':
					utilities_dict[b] += l.amount
				if l.category == 'Groceries':
					groceries_dict[b] += l.amount
				if l.category == 'Car':
					car_dict[b] += l.amount
				if l.category == 'Travel':
					travel_dict[b] += l.amount
				if l.category == 'Clothing':
					clothing_dict[b] += l.amount
				if l.category == 'Eating Out':
					eatingout_dict[b] += l.amount
				if l.category == 'Education':
					education_dict[b] += l.amount
				if l.category == 'Other':
					other_dict[b] += l.amount
		line_chart.add('Rent', rent_dict.values())
		line_chart.add('Utilities', utilities_dict.values())
		line_chart.add('Groceries', groceries_dict.values())
		line_chart.add('Car', car_dict.values())
		line_chart.add('Travel', travel_dict.values())
		line_chart.add('Clothing', clothing_dict.values())
		line_chart.add('Eating Out', eatingout_dict.values())
		line_chart.add('Education', education_dict.values())
		line_chart.add('Other', other_dict.values())
		return render_template('budgetcompare.html', line_chart=line_chart)
	
	
	#when a user tracks an expense, this function records the expense in the Spending table
	if 'expensesubmit' in request.form:
		date = request.form['date']
		year = int(date[0:4])
		month = int(date[5:7])
		day = int(date[8:10])
		date = datetime.date(year,month,day)
		amount=request.form['amount']
		try:
			amount=round(Decimal(request.form['amount']),2)
			ex = Spending(username=current_user.username, category = request.form['category'], amount = amount, date = date)
			db.session.add(ex)
			db.session.commit()
			flash('Your expense was recorded')
			return redirect('/index')
		except:
			flash('Please only enter numbers in the amount column')
			return redirect('/index')
	
	expenses_for_the_month=[]
	#deletes a recorded expense
	if 'deleteexpense' in request.form:
		expenseid=request.form['expenseid']
		ex = Spending.query.filter_by(id=int(expenseid))
		for e in ex:
			month=str(e.date)
			month=int(month[5:7])
			year= int(str(e.date)[0:4])
			e=e
		db.session.delete(e)
		db.session.commit()
		flash('Your expense record was delete')
		all=Spending.query.filter_by(username=current_user.username)
		for a in all:
			if(a.date.month==month and a.date.year==year):
				expenses_for_the_month+=[(a.category, round(Decimal(a.amount),2), a.id)]
		return render_template('index.html', title= 'Home', createform = createform, viewform=viewform, editform=editform, deleteform=deleteform, expenseform=expenseform, shareform=shareform, budgets=budgets2, count = count, expenses_for_the_month=expenses_for_the_month, shared=shared, length=len(expenses_for_the_month), differences=differences, dict_length=len(differences), share=share, budget_size=len(budgets2))
		
	#redirects the user to a different page that allows them to edit a recorded expense
	if 'editexpense' in request.form:
		expenseid=request.form['expenseid']
		return render_template('edit.html', expenseid=expenseid, expenseform=expenseform)
	
	#saves the edits to a recorded expense
	if 'editexpensesubmit' in request.form:
		expenseid=request.form['expenseid']
		category=request.form['category']
		amount=request.form['amount']
		date=request.form['date']
		year = int(date[0:4])
		month = int(date[5:7])
		day = int(date[8:10])
		date = datetime.date(year,month,day)
		ex=Spending.query.filter_by(id=int(expenseid))
		for e in ex:
			month=str(e.date)
			month=int(month[5:7])
			year=int(str(e.date)[0:4])
			e.category=category
			e.amount=amount
			e.date=date
		try:
			db.session.commit()
			flash('Your expense record was updated')
			all=Spending.query.filter_by(username=current_user.username)
			for a in all:
				if(a.date.month==month and a.date.year==year):
					expenses_for_the_month+=[(a.category, round(Decimal(a.amount),2), a.id)]
			return render_template('index.html', title= 'Home', createform = createform, viewform=viewform, editform=editform, deleteform=deleteform, expenseform=expenseform, shareform=shareform, budgets=budgets2, count = count, expenses_for_the_month=expenses_for_the_month, shared=shared, length=len(expenses_for_the_month), differences=differences, dict_length=len(differences), share=share, budget_size=len(budgets2))

		except:
			flash('Please only enter numbers for the amount')
			return render_template('edit.html', expenseid=expenseid, expenseform=expenseform)

	#displays in a list all the expenses of the specified month
	if 'viewexpenses' in request.form:
		viewmonth=request.form['month']
		viewmonth=int(str(viewmonth)[5:7])
		year= int(str(request.form['month'])[0:4])
		all=Spending.query.filter_by(username=current_user.username)
		for a in all:
			if(a.date.month==viewmonth and a.date.year==year):
				expenses_for_the_month+=[(a.category, round(Decimal(a.amount),2), a.id)]
		return render_template('index.html', title= 'Home', createform = createform, viewform=viewform, editform=editform, deleteform=deleteform, expenseform=expenseform, shareform=shareform, budgets=budgets2, count = count, expenses_for_the_month=expenses_for_the_month, shared=shared, length=len(expenses_for_the_month), differences=differences, dict_length=len(differences), share=share, budget_size=len(budgets2))
	
	#displays in a graph all the expenses of the specified month
	if 'analyzeexpenses' in request.form:
		month = request.form['month']
		month=int(month[5:7])
		year = int(request.form['month'][0:4])
		all=Spending.query.filter_by(username=current_user.username)
		for a in all:
			if(a.date.month==month and a.date.year==year):
				expenses_for_the_month+=[(a.category, round(Decimal(a.amount),2))]

		rent_dict = {}
		utilities_dict = {}
		groceries_dict = {}
		car_dict = {}
		travel_dict = {}
		clothing_dict = {}
		eatingout_dict = {}
		education_dict = {}
		other_dict = {}

		line_chart = pygal.StackedBar()
		line_chart.title = 'Expenses for '+datetime.date(2000,month,1).strftime('%b')

		b='expense'

		rent_dict[b]=0
		utilities_dict[b]=0
		groceries_dict[b]=0
		car_dict[b]=0
		travel_dict[b]=0
		clothing_dict[b]=0
		eatingout_dict[b]=0
		education_dict[b]=0
		other_dict[b]=0

		for e in expenses_for_the_month:
			if e[0] == 'Rent':
				rent_dict[b] += e[1]
			if e[0] == 'Utilities':
				utilities_dict[b] += e[1]
			if e[0] == 'Groceries':
				groceries_dict[b] += e[1]
			if e[0] == 'Car':
				car_dict[b] += e[1]
			if e[0] == 'Travel':
				travel_dict[b] += e[1]
			if e[0] == 'Clothing':
				clothing_dict[b] += e[1]
			if e[0] == 'Eating Out':
				eatingout_dict[b] += e[1]
			if e[0] == 'Education':
				education_dict[b] += e[1]
			if e[0] == 'Other':
				other_dict[b] += e[1]
		line_chart.add('Rent', rent_dict.values())
		line_chart.add('Utilities', utilities_dict.values())
		line_chart.add('Groceries', groceries_dict.values())
		line_chart.add('Car', car_dict.values())
		line_chart.add('Travel', travel_dict.values())
		line_chart.add('Clothing', clothing_dict.values())
		line_chart.add('Eating Out', eatingout_dict.values())
		line_chart.add('Education', education_dict.values())
		line_chart.add('Other', other_dict.values())
		return render_template('analyze.html', line_chart=line_chart)

	#creates a graph that compares a users budget and actual spending
	if 'comparesubmit' in request.form:
		budget_name = request.form['select']
		month = request.form['month']
		month=int(month[5:7])
		budget_spending=[]
		actual_spending=[]
		lines = LineItem.query.filter_by(username=current_user.username, budget_name=budget_name)
		for l in lines:
			budget_spending+=[(l.category, round(Decimal(l.amount),2))]
		expenses = Spending.query.filter_by(username=current_user.username)
		for ex in expenses:
			if(ex.date.month==month):
				actual_spending+=[(ex.category, round(Decimal(ex.amount),2))]
		for b in budget_spending:
			differences[b[0]]=b[1]
		for a in actual_spending:
			if a[0] not in differences:
				differences[a[0]]=-1*a[1]
			else:
				differences[a[0]]-=a[1]
		keys = list(differences.keys())
		values = list(differences.values())
		bar_chart=pygal.Bar()
		bar_chart.x_labels = keys
		bar_chart.add('Differences', values)
		return render_template('graph.html', bar_chart=bar_chart)

	return render_template('index.html', title= 'Home', createform = createform, viewform=viewform, editform=editform, deleteform=deleteform, expenseform=expenseform, shareform=shareform, budgets=budgets2, count = count, expenses_for_the_month=expenses_for_the_month, shared = shared, length=len(expenses_for_the_month), differences=differences, dict_length=len(differences),share=share, budget_size=len(budgets2))

#this function deciphers if a user wants to view, edit, delete or share their budget and redirects them to the appropriate file
@app.route('/choose', methods = ['GET', 'POST'])
def choose():
	
	#redirects to a different page so a user can view the details of a budget
	if 'viewsubmit' in request.form:
		name = request.form['radio']
		bud = Budget.query.filter_by(username=current_user.username, budget_name=name)
		for b in bud:
			bud_id = str(b.id)
		return redirect('/viewbudget/'+bud_id)
	#redirects to a different page so a user can edit the details of a budget
	if 'editsubmit' in request.form:
		name = request.form['radio']
		bud = Budget.query.filter_by(username=current_user.username, budget_name=name)
		for b in bud:
			bud_id = str(b.id)
		return redirect('/editbudget/'+bud_id)
	#redirects to a page where the budget will be deleted
	if 'deletesubmit' in request.form:
		name = request.form['radio']
		bud = Budget.query.filter_by(username=current_user.username, budget_name=name)
		for b in bud:
			bud_id = str(b.id)
		return redirect('/deletebudget/'+bud_id)
	#when a user tries to share a budget with another user, this function saves the budget under the other username
	if 'sharesubmit' in request.form:
		name=request.form['radio']
		user = request.form['shareuser']
		user_list =[]
		all_users = User.query.all()
		for u in all_users:
			user_list += [u.username]
		if user in user_list:
			b=Budget(username=user, budget_name=name, shared_by=current_user.username)
			db.session.add(b)
			db.session.commit()
			lines = LineItem.query.filter_by(username=current_user.username, budget_name=name)
			for l in lines:
				new = LineItem(category=l.category, amount =l.amount, budget_name=name, username=user)
				db.session.add(new)
				db.session.commit()
			flash('Your budget was shared with '+user)
			return redirect('/index')
		else:
			flash('You did not enter a registered user')
			return redirect('/index')

#displays all the line items in a given budget
@app.route('/viewbudget/<id>' , methods = ['GET', 'POST'])
def viewbudget(id):
	bud=Budget.query.filter_by(id=int(id))
	for b in bud:
		budget_name=b.budget_name
	line_items = LineItem.query.filter_by(username=current_user.username, budget_name=budget_name)
	categories = []
	amounts = []
	for l in line_items:
		categories+=[l.category]
		amounts += [round(Decimal(l.amount),2)]
	return render_template('viewbudget.html', categories = categories, amounts = amounts, length = len(categories))

#saves all the edits made to an updated budget
@app.route('/editbudget/<id>' , methods = ['GET', 'POST'])
def editbudget(id):
	form = Categories()
	bud=Budget.query.filter_by(id=int(id))
	for b in bud:
		name=b.budget_name
	if "submit" in request.form:
		lines = LineItem.query.filter_by(username=current_user.username, budget_name =name)
		for l in lines:
			db.session.delete(l)
		db.session.commit()
		if form.line_item1.data != 'blank':
			try:
				amount=round(Decimal(form.amount1.data),2)
				l = LineItem(category = form.line_item1.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item2.data != 'blank':
			try:
				amount=round(Decimal(form.amount2.data),2)
				l = LineItem(category = form.line_item2.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item3.data != 'blank':
			try:
				amount=round(Decimal(form.amount3.data),2)
				l = LineItem(category = form.line_item3.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item4.data != 'blank':
			try:
				amount=round(Decimal(form.amount4.data),2)
				l = LineItem(category = form.line_item4.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item5.data != 'blank':
			try:
				amount=round(Decimal(form.amount5.data),2)
				l = LineItem(category = form.line_item5.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item6.data != 'blank':
			try:
				amount=round(Decimal(form.amount6.data),2)
				l = LineItem(category = form.line_item6.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item7.data != 'blank':
			try:
				amount=round(Decimal(form.amount7.data),2)
				l = LineItem(category = form.line_item7.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item8.data != 'blank':
			try:
				amount=round(Decimal(form.amount8.data),2)
				l = LineItem(category = form.line_item8.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item9.data != 'blank':
			try:
				amount=round(Decimal(form.amount9.data),2)
				l = LineItem(category = form.line_item9.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item10.data != 'blank':
			try:
				amount=round(Decimal(form.amount10.data),2)
				l = LineItem(category = form.line_item10.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		flash('Your budget was updated!')
		return redirect('/viewbudget/'+id)
	return render_template('editbudget.html', form=form)

#deletes a budget from the table
@app.route('/deletebudget/<id>' , methods = ['GET', 'POST'])
def deletebudget(id):
	bud=Budget.query.filter_by(id=int(id))
	for b in bud:
		name=b.budget_name
	lines = LineItem.query.filter_by(username=current_user.username, budget_name =name)
	for l in lines:
		db.session.delete(l)
	db.session.commit()
	budget=Budget.query.filter_by(username=current_user.username, budget_name=name)
	for b in budget:
		db.session.delete(b)
	db.session.commit()
	flash('Budget was deleted!')
	return redirect('/index')

#adds all the line items to the LineItem table when a new budget is created
@app.route('/createbudget/<id>', methods = ['GET', 'POST'])
def createbudget(id):
	bud=Budget.query.filter_by(id=int(id))
	for b in bud:
		name=b.budget_name
	form = Categories()
	if "submit" in request.form:
		if form.line_item1.data != 'blank':
			try:
				amount=round(Decimal(form.amount1.data),2)
				l = LineItem(category = form.line_item1.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item2.data != 'blank':
			try:
				amount=round(Decimal(form.amount2.data),2)
				l = LineItem(category = form.line_item2.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item3.data != 'blank':
			try:
				amount=round(Decimal(form.amount3.data),2)
				l = LineItem(category = form.line_item3.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item4.data != 'blank':
			try:
				amount=round(Decimal(form.amount4.data),2)
				l = LineItem(category = form.line_item4.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item5.data != 'blank':
			try:
				amount=round(Decimal(form.amount5.data),2)
				l = LineItem(category = form.line_item5.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item6.data != 'blank':
			try:
				amount=round(Decimal(form.amount6.data),2)
				l = LineItem(category = form.line_item6.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item7.data != 'blank':
			try:
				amount=round(Decimal(form.amount7.data),2)
				l = LineItem(category = form.line_item7.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item8.data != 'blank':
			try:
				amount=round(Decimal(form.amount8.data),2)
				l = LineItem(category = form.line_item8.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item9.data != 'blank':
			try:
				amount=round(Decimal(form.amount9.data),2)
				l = LineItem(category = form.line_item9.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		if form.line_item10.data != 'blank':
			try:
				amount=round(Decimal(form.amount10.data),2)
				l = LineItem(category = form.line_item10.data, amount = amount, budget_name=name, username=current_user.username)
				db.session.add(l)
				db.session.commit()
			except:
				flash('Please only enter numbers in the amount column')
				return redirect('/createbudget/'+str(id))
		flash('Your budget was created!')
		return redirect('/viewbudget/'+id)
	return render_template('create_budget.html', form=form)
	

#checks if a user is registered and entered the correct password and then logs them in
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/index')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Username or password was incorrect')
			return redirect('/login')
		login_user(user, remember=form.remember_me.data)
		return redirect('/index')
	return render_template('login.html', title='Login', form = form)


#logs a user out
@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')


#adds a new user to the User table when they register
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()
	user = User.query.filter_by(username=form.username.data).first()
	if user is not None:
		flash('Please use a different username.')
		return redirect('/register')
	if form.validate_on_submit():
		if form.password.data!=form.password2.data:
			flash('Passwords did not match')
			return redirect('/register')
		u = User(username=form.username.data)
		u.set_password(form.password.data)
		db.session.add(u)
		db.session.commit()
		flash('You are a new user! You may now login to your account')
		return redirect('/login')

	return render_template('register.html', title='Register', form = form)


#the comment page
@app.route('/comments', methods =['GET', 'POST'])
def comment():
	#adds the comment thread to the Thread table
	if 'thread_submit' in request.form:
		if request.form['thread_name']=='':
			flash("Please enter a name to create a new thread")
		else:
			t=Threads(username=current_user.username, thread_name=request.form['thread_name'])
			db.session.add(t)
			db.session.commit()
			flash('Your comment thread was created')
		return redirect('/comments')
	comm = []
	all_threads=[]
	count=0
	current_thread = ""
	#displays all the comments in a particular comment page
	if 'select_thread' in request.form:
		count=1
		thread_name = request.form['select_thread']
		comments = Comments.query.filter_by(thread_name=thread_name)
		for c in comments:
			comm+=[(c.comment, c.username)]
		return render_template('comments.html', all_threads=all_threads, comm=comm, count=count, current_thread=thread_name)
	
	#saves a comment when a new one is made
	if 'comment_submit' in request.form:
		count=1
		thread_name = request.form['current_thread']
		comment = request.form['new_comment']
		c=Comments(username=current_user.username, thread_name=thread_name, comment=comment)
		db.session.add(c)
		db.session.commit()
		comments = Comments.query.filter_by(thread_name=thread_name)
		for c in comments:
			comm+=[(c.comment, c.username)]
		return render_template('comments.html', all_threads=all_threads, comm=comm, count=count, current_thread=thread_name)

	threads=Threads.query.all()
	for t in threads:
		all_threads += [t.thread_name]
	return render_template('comments.html', all_threads=all_threads, comm=comm, count=count, current_thread=current_thread)
