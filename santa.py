from flask import Flask, render_template, request, g
import sqlite3
app = Flask(__name__)

MAX_GIFT_LIMIT = "$50.00 USD"
SECRET_PASS = 'turkeysanta'
DATABASE = 'santa.db'

def connect_to_database():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_to_database()

@app.teardown_request
def close_connection(exception):
    if g.db is not None:
        g.db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/santa', methods=['POST', 'GET'])
def santa():
    error = None
    if request.method == 'POST':
        real_name = request.form.get('name')
        password = request.form.get('password')
	try:
            g.db.execute('insert into secret_santa (name, password, match) values (?, ?, NULL)', [real_name, password])
	    g.db.commit()
	except Exception as e:
            return "There was a problem with your submission!\n\n%s" % e
	return "Your submission has been recorded!"
    return render_template('santa.html', error=error)

@app.route('/randomizer', methods=['POST', 'GET'])
def randomizer():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
	if password == SECRET_PASS:
            return "You got the password! Stuff should be randomized now!"
        else:
            return "Nice try..."
    return render_template('randomizer.html', error=error)

@app.route('/status', methods=['POST', 'GET'])
def status():
    error = None
    if request.method == 'POST':
        real_name = request.form.get('name')
        password = request.form.get('password')

	user_data = None
        query = "select match from secret_santa where name='%s' AND password='%s'" % (real_name, password)
	print query
	try:
	    user_data = query_db(query)
	except Exception as e:
            return "Unable to find user (Did you register?)\n\n%s" % e
        
        print user_data
        try:
            if user_data[0][0]:
	        match_query = 'select name from secret_santa where id=%d' % int(user_data[0][0])
                match_data = query_db(match_query)
	    else:
	        return "Match not yet available! Check back soon!"
        except Exception as e:
            return "There was an error trying to find your match!"
        print match_data
	return 'You got: %s!' % match_data[0][0]
    return render_template('status.html', error=error)

@app.route('/')
def welcome_page():
    return render_template('index.html')

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()
@app.route('/')
def welcome_page():
    return render_template('index.html')

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()
