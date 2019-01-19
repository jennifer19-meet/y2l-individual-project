from flask import Flask, render_template, request, session, flash, url_for, redirect
# from flask_session.__init__ import Session
# to install ---> pip install Flask-Session
# OR from flask_session import Session
# OR from flask.ext.session import Session
import json, requests
from database import *

app = Flask(__name__)
# sess = Session()
######################NOT LOGGED IN###################

@app.route('/')
def home_page():
	if in session:
		return render_template("logged_in_homepage.html")
	else:
		return render_template("homepage.html")
#does the'username' thingi work?


#####################USERS#######################
@app.route("/signup", methods=["POST","GET"])
def signup():
	if request.method =='POST':	
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		profile_pic = "hi"
		create_user(username, email, password,profile_pic)
		return redirect(url_for("home_page"))
	else:
		return render_template("signup.html")

@app.route("/login", methods=["POST","GET"])
def signin():
	passs= None
	uuuu = None
	if request.method =='POST':
		u = request.form['username']
		p = request.form['password']
		person = get_user(u)
		if get_user(u) == None:
			uuuu = True
			return render_template("login.html", uuuu =uuuu)
		elif {{ person.username }} == u and  {{ person.password }} == p:
			session['logged_in'] = True
			return render_template("logged_in_homepage.html")
		elif {{ person.username }} == u and {{ person.password }} != p:
			passs = True
			return render_template("login.html", passs= passs)
	else:
		return render_template("login.html")


@app.route("/logout", methods=["POST","GET"])
def logout():
	session['logged_in'] = False
	return render_template("homepage.html")

											 
@app.route ('/user/<string:username>')
def profile(username):
	user = get_user(username)
	return render_template("profilepage.html", user=user)

##################CHARITIES#####################

@app.route ("/add_charity", methods = ["POST","GET"])
def new_charity():
	if request.method =='POST':	
		name = request.form['name']
		cause = request.form['cause']
		email = request.form['email']
		website = request.form['website']
		pic = "hi"
		short_into = request.form['short_intro']
		paragraph = request.form['paragraph']
		create_user(name, cause, email, website,pic,short_intro,paragraph)
		return render_template("homepage.html")

@app.route('/charities')
def all_charities():
	return render_template("all_charities.html")


@app.route('/charities/<int:id>')
def charity_page(id):
	charity = get_charity(id)
	return render_template("charitypage.html", charity = charity)

####################SEARCH##########################

@app.route('/results')
def results():
	return render_template("searchpage.html")

####################EXTRAS########################

@app.route('/aboutus')
def about():
	return render_template("aboutus.html")


if __name__ == '__main__':
	app.secret_key = 'yay'
	app.config['SESSION_TYPE'] = 'sqlalchemy'
	#  memcached or filesystem or  mongodb or redis???
	# sess.init_app(app)
	app.run(debug = True)