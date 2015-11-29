Purpose:
Every year we do a secret santa within a group of friends. The biggest challenge is getting everyone together during the holiday season rush. That's why I created this simple (and I mean SIMPLE) flask webapp. Tried and tested, it worked great for our needs. Can it be improved? Sure, but this was written during a post Thanksgiving Day food coma. :) Hope this helps someone else out there!

Setup:
1) Setup Webserver of choice. For simplicity, I use httpd + mod_wsgi. I assume this setup throughout the rest of the README; feel free to try something else!
2) Setup a user/group for the wsgi daemon process. For the example, I created a `jvasallo:jvasallo` as the user:group on the OS.
3) Create virtualenv with the user created in step 2, and `pip install -r requirements.txt`
4) Run `bash setup.sh` to create the base sqlite3 table schema. Feel free to change this to whatever DB technology you want.
5) Check over the wsgi file to make sure all endpoints match that of your system. Namely, the venv path and the app path.
6) Check the conf.d file and make sure it has all the right endpoints from the previous steps. Namely, the user:group, the webserver specific IPs/names, and path to the virtualenv.
6) Start up your webserver with PROD Mode settings, open `santa.py` and change the main block to have PROD settings and comment out the debug settings.
