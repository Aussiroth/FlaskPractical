from flask import *
from functools import wraps
import sqlite3
from flask.ext.mail import *
import datetime
import hashlib

app = Flask(__name__)

mail = Mail(app)

app.secret_key = ('GreatWhiteBlueRedBlackGreenDragonsAreSoMuchCoolerThanTheStupidHouseDrakon')

#DATABASE = '/home/Aussiroth/mysite/shop.db'
DATABASE = 'shop.db'

app.config.from_object(__name__)


app.config.update(
	DEBUG=True,
	#Email does not work, so settings removed for now.
	)
#send email function, not yet working, error 111.
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = "you@dgoogle.com", recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login to access the site.')
            return redirect(url_for('login'))
    return wrap 
	
#function to format order for cart, checkout, invoice history
def format_order(currorder, format_order, prices):
	if currorder[1]>0:
		format_order.append(['A4 Lecture Pad', currorder[1], "{0:<.2f}".format(prices[0]), "{0:<.2f}".format(int(currorder[1])*prices[0])])
	if currorder[2]>0:
		format_order.append(['7-colour sticky note with pen', currorder[2], "{0:<.2f}".format(prices[1]), "{0:<.2f}".format(int(currorder[2])*prices[1])])
	if currorder[3]>0:
		format_order.append(['A5 exercise book', currorder[3], "{0:<.2f}".format(prices[2]), "{0:<.2f}".format(int(currorder[3])*prices[2])])
	if currorder[4]>0:
		format_order.append(['A5 note book with zip bag', currorder[4], "{0:<.2f}".format(prices[3]), "{0:<.2f}".format(int(currorder[4])*prices[3])])
	if currorder[5]>0:
		format_order.append(['2B pencil', currorder[5], "{0:<.2f}".format(prices[4]), "{0:<.2f}".format(int(currorder[5])*prices[4])])
	if currorder[6]>0:
		format_order.append(['Stainless steel tumbler', currorder[6], "{0:<.2f}".format(prices[5]), "{0:<.2f}".format(int(currorder[6])*prices[5])])
	if currorder[7]>0:
		format_order.append(['A4 clear holder', currorder[7], "{0:<.2f}".format(prices[6]), "{0:<.2f}".format(int(currorder[7])*prices[8])])
	if currorder[8]>0:
		format_order.append(['A4 vanguard file', currorder[8], "{0:<.2f}".format(prices[7]), "{0:<.2f}".format(int(currorder[8])*prices[7])])
	if currorder[9]>0:
		format_order.append(['Name card holder', currorder[9], "{0:<.2f}".format(prices[8]), "{0:<.2f}".format(int(currorder[9])*prices[8])])
	if currorder[10]>0:
		format_order.append(['Umbrella', currorder[10], "{0:<.2f}".format(prices[9]), "{0:<.2f}".format(int(currorder[10])*prices[9])])
	if currorder[11]>0:
		format_order.append(['School badge (Junior High)', currorder[11], "{0:<.2f}".format(prices[10]), "{0:<.2f}".format(int(currorder[11])*prices[10])])
	if currorder[12]>0:
		format_order.append(['School badge (Senior High)', currorder[12], "{0:<.2f}".format(prices[11]), "{0:<.2f}".format(int(currorder[12])*prices[11])])
	if currorder[13]>0:
		format_order.append(['Dunman dolls (pair)', currorder[13], "{0:<.2f}".format(prices[12]), "{0:<.2f}".format(int(currorder[13])*prices[12])])
	totalcost = 0
	for row in format_order:
		try:
			totalcost += float(row[3])
		except:
			True
	realcost = totalcost
	totalcost = "{0:<.2f}".format(totalcost)
	return format_order, totalcost, realcost
	
#view functions
	
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		logged_user = session['username']
		number=[]
		number.append(int(request.form['item1']))
		number.append(int(request.form['item2']))
		number.append(int(request.form['item3']))
		number.append(int(request.form['item4']))
		number.append(int(request.form['item5']))
		number.append(int(request.form['item6']))
		number.append(int(request.form['item7']))
		number.append(int(request.form['item8']))
		number.append(int(request.form['item9']))
		number.append(int(request.form['item10']))
		number.append(int(request.form['item11']))
		number.append(int(request.form['item12']))
		number.append(int(request.form['item13']))
		timeszero = 0
		for each in number:
			#validate if negative is entered
			if each<0:
				error = "You should not have negative numbers selected!"
				return render_template('home.html', logged = True, error = error)
			#check number of 0s entered
			elif each == 0:
				timeszero +=1
		#validate if user enters all 0
		if timeszero==13:
			error = "You did not order any quantity of any item!"
			return render_template('home.html', logged = True, error = error)
		g.db = connect_db()
		cur = g.db.execute('select name from orders')
		names = [row[0] for row in cur.fetchall()]
		#check if there is current order in cart
		if logged_user in names:
			#if have, take existing values, add together
			cur = g.db.execute('select * from orders where name="'+logged_user+'"')
			currnumber = [[row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]] for row in cur.fetchall()]
			g.db.execute('delete from orders where name="'+logged_user+'"')
			for i in range(0, 13):
				number[i]+=int(currnumber[0][i])
		g.db.execute('insert into orders (name, lecture, stickynote, exercisebook, notebook, pencil, tumbler, clearholder, vanguard, cardholder, umbrella, jhbadge, shbadge, dolls) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [logged_user, number[0], number[1], number[2], number[3], number[4], number[5], number[6], number[7], number[8], number[9], number[10], number[11], number[12]])
		g.db.commit()
		flash("Successfully placed your order!")
		#directs to cart to see the current order
		return redirect(url_for('cart'))
	else:
		return render_template('home.html', logged = True)
	
@app.route('/welcome')
def welcome():
	return render_template('welcome.html', logged = True)

#login/logout/create user functions
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	debug = 0
	if request.method == 'POST':
		g.db = connect_db()
		cur = g.db.execute('select username, password from users')
		users = [[row[0], row[1]] for row in cur.fetchall()]
		found = False
		curruser = request.form['username']
		currpass = request.form['password']
		for user in users:
			if user[0]==curruser:
				found = True
				hash = hashlib.sha1()
				hash.update(currpass)
				if user[1]==hash.hexdigest():
					session['username'] = curruser
					return redirect(url_for('welcome'))
				else:
					error = "You entered the wrong password."
		if not found:
			error = "You entered a wrong username."
	if 'username' in session:
		return render_template('log.html', error=error, logged = True)
	else:
		return render_template('log.html', error=error, logged = False)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))
		
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	error = []
	if request.method == 'POST':
		curruser = request.form['username']
		password1 = request.form['password1']
		password2 = request.form['password2']
		curremail = request.form['email']
		correct = True
		# VALIDATE EMAIL
		search = curremail.find("@")
		# VALIDATE IF THERE IS EMAIL
		if curremail == "":
			error.append("You did not enter an email!")
			correct = False
		# VALIDATE IF @ IS PRESENT
		elif search<0:
			error.append("You did not enter your email correctly, there must be a @ symbol in the email address, e.g. lim@def.com")
			curremail = ""
			correct = False
		# VALIDATE IF THERE IS A PROPER ADDRESS (THERE IS BLABLA@BLA.COM, NOT @BLA.COM
		elif search==0:
			error.append("You did not enter your email correctly, there should be some text before the @ symbol, e.g. ah@def.com")
			curremail = ""
			correct = False
		# VALIDATE IF THERE IS A . AFTER THE @ FOR PROPER ADDRESS
		else:
			if "." not in curremail:
				error.append("You did not enter your email correctly, there should be a . after the @ symbol, e.g. seng@def.com")
				curremail = ""
				correct = False
		# VALIDATE IF THERE IS PASSWORD
		if password1 == "" or password2 == "":
			error.append("You did not fill in the password fields!")
			password1=""
			correct = False
		#VALIDATE IF BOTH PASSWORDS ENTERED MATCH
		elif password1 != password2:
			error.append("The passwords you entered are not the same! Please reenter.")
			password1 = ""
			correct = False
		
		#VALIDATE IF USERNAME IS EMPTY
		
		if curruser == "":
			error.append("You did not enter any username!")
			correct = False
		else:
		#VALIDATE IF USERNAME ALREADY USED
			g.db = connect_db()
			cur = g.db.execute('select username from users')
			users = [row[0] for row in cur.fetchall()]
			if curruser in users:
				error.append("The username is already taken. Please choose another one.")
				curruser = ""
				correct = False
		
		# IF ALL DATA CORRECT, ENTER INTO DATABASE, REDIRECT TO WELCOME
			
		if correct==True:
			session['username'] = curruser
			hash = hashlib.sha1()
			hash.update(password1)
			g.db.execute('insert into users (username, password, email) values (?, ?, ?)', [curruser, hash.hexdigest(), curremail])
			g.db.commit()
			flash('Thanks for signing up!')
			return redirect(url_for('welcome'))
		else:
			return render_template('signup.html', username = curruser, password = password1, email = curremail, error = error, logged = False)
	else:
		return render_template('signup.html', logged = False)
		
#cart/checkout side		

@app.route('/cart')
@login_required
def cart():
	logged_user = session['username']
	g.db = connect_db()
	cur = g.db.execute('select * from orders')
	orders = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]] for row in cur.fetchall()]
	#take prices
	cur = g.db.execute('select price from prices')
	prices = [row[0] for row in cur.fetchall()]
	#check for persons order
	gotorder = False
	for order in orders:
		if order[0] == logged_user:
			currorder = order
			gotorder = True
			break
	if gotorder:
		fullorder = []
		fullorder, totalcost, realcost = format_order(currorder, fullorder, prices)
		if realcost>=150.00:
			warning = "Warning: You have selected at least $150 of purchases, do check if your current order is what you want and there is no error."
		else:
			warning = ""
		return render_template('cart.html', currorder = fullorder, logged = True, order = True, totalcost = totalcost, warning = warning)
	else:
		flash("You have no items in your cart! Head to the homepage to buy some items!")
		return render_template('cart.html', logged = True, order = False)
	
@app.route('/delete')
@login_required
def delete():
	logged_user = session['username']
	g.db = connect_db()
	g.db.execute('delete from orders where name="'+logged_user+'"')
	g.db.commit()
	flash("Successfully deleted your current order.")
	return redirect(url_for('cart'))
	
@app.route('/checkout')
@login_required
def checkout():
	logged_user = session['username']
	g.db = connect_db()
	cur = g.db.execute('select * from orders')
	orders = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]] for row in cur.fetchall()]
	#take prices
	cur = g.db.execute('select price from prices')
	prices = [row[0] for row in cur.fetchall()]
	#get email
	cur = g.db.execute('select email from users where username ="'+logged_user+'"')
	email = [row[0] for row in cur.fetchall()]
	#check for persons order
	gotorder = False
	for order in orders:
		if order[0] == logged_user:
			currorder = order
			gotorder = True
			break
	if gotorder:
		fullorder = []
		fullorder, totalcost, temp = format_order(currorder, fullorder, prices)
		#delete from carts
		g.db.execute('delete from orders where name="'+logged_user+'"')
		g.db.commit()
		#get current date and time of invoice and date to collect.
		currdate = datetime.datetime.today()
		logged_date = currdate.strftime("%d %B %Y, %H:%M")
		collectdate = currdate + datetime.timedelta(days=5)
		collectdate = collectdate.strftime("%d %B %Y")
		#add to confirm, for shop to confirm + user to check history
		g.db.execute('insert into confirm (name, lecture, stickynote, exercisebook, notebook, pencil, tumbler, clearholder, vanguard, cardholder, umbrella, jhbadge, shbadge, dolls, date) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [currorder[0], currorder[1], currorder[2], currorder[3], currorder[4], currorder[5], currorder[6], currorder[7], currorder[8], currorder[9], currorder[10], currorder[11],currorder[12], currorder[13], logged_date])
		g.db.commit()
		return render_template('checkout.html', currorder = fullorder, logged = True, totalcost = totalcost, date=logged_date, collectdate = collectdate)
	#check in case no order and accidentally stumble upon the page.
	else:
		flash("You can't checkout if you have no items!")
		return redirect(url_for('cart'))
		

	
#profile user stuff

@app.route('/profile')
@login_required
def profile():
	logged_user = session['username']
	return render_template('profile.html', username = logged_user, logged = True)
	
@app.route('/changeuser', methods = ['GET', 'POST'])
@login_required
def changeuser():
	error = ""
	if request.method == "POST":
		logged_user = session['username']
		g.db = connect_db()
		curruser = request.form['username']
		#validate if username empty
		correct = True
		if curruser == "":
			error = "You did not enter any username!"
			correct = False
		else:
		#VALIDATE IF USERNAME ALREADY USED
			g.db = connect_db()
			cur = g.db.execute('select username from users')
			users = [row[0] for row in cur.fetchall()]
			if curruser in users:
				error = "The username is already taken. Please choose another one."
				curruser = ""
				correct = False
		if correct:
			g.db.execute('update users set username="'+curruser+'" where username="'+logged_user+'"') 
			g.db.execute('update orders set name="'+curruser+'" where name="'+logged_user+'"')
			g.db.execute('update confirm set name="'+curruser+'" where name="'+logged_user+'"')
			g.db.commit()
			flash("Successfully changed your username.")
			session['username'] = curruser
			return redirect(url_for('profile'))
	return render_template('changeuser.html', error = error, logged = True)

@app.route('/changepass', methods = ['GET', 'POST'])
@login_required
def changepass():
	error = ""
	password1, password2 = "", ""
	if request.method == "POST":
		logged_user = session['username']
		g.db = connect_db()
		currpass = request.form['currpass']
		password1 = request.form['password1']
		password2 = request.form['password2']
		#validate if any is empty
		correct = True
		if currpass == "":
			error = "You did not enter your current password!"
			correct = False
		elif password1 =="" or password2 == "":
			error = "You did not enter any info for your passwords"
			correct = False
		elif password1 != password2:
			error = "You did not re-type your password correctly."
			correct = False
		else:
		#VALIDATE IF PASSWORD IS CORRECT
			hash1 = hashlib.sha1()
			hash1.update(currpass)
			g.db = connect_db()
			cur = g.db.execute('select username, password from users')
			users = [[row[0], row[1]] for row in cur.fetchall()]
			for user in users:
				if user[0]==logged_user:
					if user[1]!=hash1.hexdigest():
						error = "You did not type your current password correctly. Please try again."
						correct = False
		if correct:
			hash2 = hashlib.sha1()
			hash2.update(password1)
			g.db.execute('update users set password="'+hash2.hexdigest()+'" where password="'+hash1.hexdigest()+'"')
			g.db.commit()
			flash("Successfully changed your password.")
			return redirect(url_for('profile'))
	return render_template('changepass.html', error = error, logged = True, password1=password1)
	
@app.route('/changeemail', methods = ['GET', 'POST'])
@login_required
def changeemail():
	error = ""
	if request.method == "POST":
		logged_user = session['username']
		g.db = connect_db()
		curremail = request.form['email']
		correct = True
		search = curremail.find("@")
		#validate if emailempty
		if curremail == "":
			error = "You did not enter any email!"
			correct = False
		# VALIDATE IF @ IS PRESENT
		elif search<0:
			error = ("You did not enter your email correctly, there must be a @ symbol in the email address, e.g. lim@def.com")
			curremail = ""
			correct = False
		# VALIDATE IF THERE IS A PROPER ADDRESS (THERE IS BLABLA@BLA.COM, NOT @BLA.COM
		elif search==0:
			error = ("You did not enter your email correctly, there should be some text before the @ symbol, e.g. ah@def.com")
			curremail = ""
			correct = False
		# VALIDATE IF THERE IS A . AFTER THE @ FOR PROPER ADDRESS
		else:
			if "." not in curremail:
				error =("You did not enter your email correctly, there should be a . after the @ symbol, e.g. seng@def.com")
				curremail = ""
				correct = False
		if correct:
			cur = g.db.execute('select * from users where username="'+logged_user+'"')
			info = [[row[0], row[1], row[2]] for row in cur.fetchall()]
			info[0][2] = curremail
			g.db.execute('delete from users where username="'+logged_user+'"')
			g.db.execute('insert into users (username, password, email) values (?, ?, ?)', [info[0][0], info[0][1], info[0][2]])
			g.db.commit()
			flash("Successfully changed your email.")
			return redirect(url_for('profile'))
	return render_template('changeemail.html', error = error, logged = True)
	
#history of invoices
@app.route('/invoice')
@login_required
def invoice():
	logged_user = session['username']
	g.db = connect_db()
	cur = g.db.execute('select * from confirm')
	orders = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]] for row in cur.fetchall()]
	person_order = []
	gotorder = False
	for order in orders:
		if order[0]==logged_user:
			person_order.append(order)
			gotorder = True
	if gotorder:
		cur = g.db.execute('select price from prices')
		prices = [row[0] for row in cur.fetchall()]
		allorder = []
		for order in person_order:
			full_curr_order = []
			full_curr_order.append(order[-1])
			full_curr_order, totalcost, temp = format_order(order, full_curr_order, prices)
			allorder.append(full_curr_order)
		return render_template('invoice.html', logged = True, gotorder = True, allorder = allorder)
	return render_template('invoice.html', logged = True, gotorder = False)
	
if __name__ == '__main__':
    app.run(debug=True)