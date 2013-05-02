from flask import *
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = ('Aussircaex')

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
            flash('You need to login first.')
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
    #g.db  = connect_db()
    #cur = g.db.execute('select name, cost from items')
    #sales = [dict(name=row[0], cost=row[1]) for row in cur.fetchall()]
    #g.db.close()
    if check_logged_in():
		return render_template('home.html', logged = True)
    else:
		return render_template('home.html', logged = False)

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
	if check_logged_in():
		return render_template('cart.html', logged = True)
	else:
		return render_template('cart.html', logged = False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('welcome'))
	if check_logged_in():
		return render_template('log.html', error=error, logged = True)
    else:
		return render_template('log.html', error=error, logged = False)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
	item = request.form['item']
	number = request.form['value']
	return render_template('order.html', number = number)
		
if __name__ == '__main__':
    app.run(debug=True)