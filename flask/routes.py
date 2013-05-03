from flask import *
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = ('GreatWhiteBlueRedBlackGreenDragonsAreSoMuchCoolerThanTheStupidHouseDrakon')

DATABASE = 'shop.db'

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login to access the site.')
            return redirect(url_for('login'))
    return wrap 

def check_logged_in():
	if 'logged_in' in session:
		return True
	else:
		return False
	
@app.route('/')
@login_required
def home():
	return render_template('home.html', logged = True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
	
@app.route('/welcome')
def welcome():
	if check_logged_in():
		return render_template('welcome.html', logged = True)
	else:
		return render_template('welcome.html', logged = False)

@app.route('/cart')
@login_required
def cart():
	g.db = connect_db()
	cur = g.db.execute('select name, lecture, stickynote, exercisebook, notebook, pencil, tumbler, clearholder, vanguard, cardholder, umbrella, jhbadge, shbadge, dolls from orders')
	orders = [[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]] for row in cur.fetchall()]
	#check for persons order
	for order in orders:
		if row[0] == logged_user:
			currorder = order
			break
	return render_template('cart.html', currorder = currorder, logged = True)

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
				if user[1]==currpass:
					session['logged_in'] = True
					global logged_user
					logged_user = curruser
					return redirect(url_for('welcome'))
				else:
					error = "You entered the wrong password."
		if not found:
			error = "You entered a wrong username."
	if check_logged_in():
		return render_template('log.html', error=error, logged = True)
	else:
		return render_template('log.html', error=error, logged = False)

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
		if search<0:
			error.append("You did not enter your email correctly, there must be a @ symbol in the email address, e.g. lim@def.com")
			curremail = ""
			correct = False
		elif search==0:
			error.append("You did not enter your email correctly, there should be some text before the @ symbol, e.g. ah@def.com")
			curremail = ""
			correct = False
		else:
			if "." not in curremail:
				error.append("You did not enter your email correctly, there should be a . after the @ symbol, e.g. seng@def.com")
				curremail = ""
				correct = False
		#VALIDATE IF BOTH PASSWORDS ENTERED MATCH
		if password1 != password2:
			error.append("The passwords you entered are not the same! Please reenter.")
			password1 = ""
			correct = False
			
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
			session['logged_in'] = True
			g.db.execute('insert into users (username, password, email) values (?, ?, ?)', [curruser, password1, curremail])
			g.db.commit()
			global logged_user
			logged_user = curruser
			flash('Thanks for signing up!')
			return redirect(url_for('welcome'))
		else:
			return render_template('signup.html', username = curruser, password = password1, email = curremail, error = error, logged = False)
	else:
		return render_template('signup.html', logged = False)
		
#MIDDLE-PAGE FOR STORING ORDERS, THEN LINK STRAIGHT TO CART.
		
@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
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
	g.db = connect_db()
	cur = g.db.execute('select name from orders')
	names = [row[0] for row in cur.fetchall()]
	if logged_user in names:
		g.db.execute('delete from orders where name='+str(logged_user))
		#g.db.execute('update orders set (lecture, stickynote, exercisebook, notebook, pencil, tumbler, clearholder, vanguard, cardholder, umbrella, jhbadge, shbadge, dolls) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) where name='+str(logged_user), [number])
	g.db.execute('insert into orders (name, lecture, stickynote, exercisebook, notebook, pencil, tumbler, clearholder, vanguard, cardholder, umbrella, jhbadge, shbadge, dolls) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [logged_user, number[0], number[1], number[2], number[3], number[4], number[5], number[6], number[7], number[8], number[9], number[10], number[11], number[12]])
	g.db.commit()
	return redirect(url_for('cart'))
	#return render_template('order.html', loggeduser = logged_user, names = number)
		
if __name__ == '__main__':
    app.run(debug=True)