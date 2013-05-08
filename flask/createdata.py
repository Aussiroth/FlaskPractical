import sqlite3 as lite
import sys

con = lite.connect('shop.db')

foo = "dummy"

with con:
	cur = con.cursor()
	#cur.execute("DROP TABLE IF EXISTS prices")
	#cur.execute("CREATE TABLE prices (price float)")
	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("CREATE TABLE users(username text, password text, email text)")
	#cur.execute("INSERT INTO users VALUES ('admin', 'admin', 'leow.justin@dhs.sg')")
	#cur.execute("INSERT INTO users VALUES ('Aussiroth', 'WhiteDragon', 'yan.hongyao.alvin@dhs.sg')")
	#cur.execute("DROP TABLE IF EXISTS orders")
	#cur.execute("CREATE TABLE orders (name text, lecture number, stickynote number, exercisebook number, notebook number, pencil number, tumbler number, clearholder number, vanguard number, cardholder number, umbrella number, jhbadge number, shbadge number, dolls number)")
	#cur.execute("INSERT INTO orders VALUES ('admin', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
	#cur.execute("DROP TABLE IF EXISTS confirm")
	#cur.execute("CREATE TABLE confirm (name text, lecture number, stickynote number, exercisebook number, notebook number, pencil number, tumbler number, clearholder number, vanguard number, cardholder number, umbrella number, jhbadge number, shbadge number, dolls number, date text)")