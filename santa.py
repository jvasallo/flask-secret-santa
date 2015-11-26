from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/santa', methods=['POST', 'GET'])
def santa():
    error = None
    if request.method == 'POST':
        return 'You Posted!'
    return render_template('santa.html', error=error)

if __name__ == '__main__':
    # Enable Debug mode
    app.debug = True
    app.run()
