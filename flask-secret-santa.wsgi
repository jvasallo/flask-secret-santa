#!/usr/bin/python

# Make sure to update this path to the virtualenv path
activate_this = '/var/www/html/flask-secret-santa/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
# Make sure to update the path that correlates to your webroot
sys.path.insert(0, '/var/www/html/flask-secret-santa')

from santa import app as application

# Feel free to generate your own, but this isn't used today
# import os
# os.urandom(24)
# Paste output below
application.secret_key = ''
