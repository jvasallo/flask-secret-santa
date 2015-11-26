from flask import Flask, render_template, request, g
import sqlite3
app = Flask(__name__)

MAX_GIFT_LIMIT = "$50.00 USD"
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

@app.route('/santa', methods=['POST', 'GET'])
def santa():
    error = None
    if request.method == 'POST':
        real_name = request.form.get('name')
        email_address = request.form.get('email_address')
	try:
            g.db.execute('insert into secret_santa (name, email_address) values (?, ?)', [real_name, email_address])
	    g.db.commit()
	except Exception as e:
            return "There was a problem with your submission! %s" % e
	return "Your submission has been recorded!"
    return render_template('santa.html', error=error)

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()
