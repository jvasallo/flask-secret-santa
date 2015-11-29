#!/usr/bin/python
from flask import Flask, render_template, request, g
import os
import sqlite3
import random
app = Flask(__name__)

MAX_GIFT_LIMIT = "$50.00 USD"
SECRET_PASS = 'turkeysanta'
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'santa.db')

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
	    check_query = "select name from secret_santa where name='%s'" % real_name
            check_results = query_db(check_query)
            if check_results:
                return "Nice try slick...you already registered! Return back <a href='/'>Home</a>"
            g.db.execute('insert into secret_santa (name, password, match) values (?, ?, NULL)', [real_name, password])
	    g.db.commit()
	except Exception as e:
            return "There was a problem with your submission!<br><br>%s" % e
	return "Your submission has been recorded! Return back <a href='/'>Home</a>"
    return render_template('santa.html', error=error)

@app.route('/randomizer', methods=['POST', 'GET'])
def randomizer():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
	user_query = 'SELECT id, name from secret_santa'
	if password == SECRET_PASS:
	    user_list = []
	    user_matching_status = False
	    try:
	        user_table_list = query_db(user_query)
		# Create a list of user_ids
	        for each_user in user_table_list:
                    unique_user_id = each_user[0]
                    user_list.append(unique_user_id)


                # randomly assign person to user so long
		# as the user isn't themselves. Also,
		# remove the user so there's no duplicate
		for each_user in user_table_list:
                    while True:
                        random_match = random.choice(user_list)
			if random_match != each_user[0]:
			    query = "UPDATE secret_santa SET match=%d WHERE name='%s' AND id=%d" % (int(random_match), each_user[1], int(each_user[0]))
			    g.db.execute(query)
			    g.db.commit()
			    print "Found a match for: %s" % each_user[1]
		            user_list.remove(random_match)
			    break
                        else:
                            print "selection still not random; recycling."
                print "All users have been matched!"
		user_matching_status = True
            except Exception as e:
                return "Error getting userlist"
	    if user_matching_status:
                return "Stuff should be randomized now! <a href='/randomizer'>Re-run</a> or Return back <a href='/'>Home</a>"
	    else:
                return "Something went wrong matching. Sorry!"
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
	try:
	    user_data = query_db(query)
	except Exception as e:
            return "Unable to find user (Did you register?)<br><br>%s" % e
        
        try:
            if user_data[0][0]:
	        match_query = 'select name from secret_santa where id=%d' % int(user_data[0][0])
                match_data = query_db(match_query)
	    else:
	        return "Match not yet available! Check back soon! Return back <a href='/'>Home</a>"
        except Exception as e:
            return "There was an error trying to find your match! Return back <a href='/'>Home</a>"
	return "You got: %s! The limit that has been set has been: %s!<br><br>Check again whenever, or remember it well! Return back <a href='/'>Home</a>" % (match_data[0][0], MAX_GIFT_LIMIT)
    return render_template('status.html', error=error)

@app.route('/')
def welcome_page():
    return render_template('index.html')

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()

    # PROD Mode
    #app.run(host='0.0.0.0', port=80)
