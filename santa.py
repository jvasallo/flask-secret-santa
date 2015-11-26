from flask import Flask, render_template, request
app = Flask(__name__)

MAX_GIFT_LIMIT = "$50.00 USD"

@app.route('/santa', methods=['POST', 'GET'])
def santa():
    error = None
    if request.method == 'POST':
        real_name = request.form.get('name')
        email_address = request.form.get('email_address')
	return "You got: %s\nTheir email is: %s\nRemember the max limit of: %s!" % (real_name, email_address, MAX_GIFT_LIMIT)
    return render_template('santa.html', error=error)

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()
