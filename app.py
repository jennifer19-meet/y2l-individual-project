from flask import Flask, render_template, request, session, flash, url_for, redirect,send_from_directory
# from flask_session.__init__ import Session
# to install ---> pip install Flask-Session
# from flask_session import Session
# OR from flask.ext.session import Session
# from sqlalchemy.orm import sessionmaker (?????????)
import random
from werkzeug.utils import secure_filename
import os
import json, requests
import database
from clarifai.rest import ClarifaiApp
from clarifai.errors import ApiError

app = Flask(__name__)
# sess = Session()
######################NOT LOGGED IN###################
app1 = ClarifaiApp(api_key='737ed43ee3e54455a067f36e36cd56d9')
model = app1.public_models.general_model

UPLOAD_FOLDER = 'static/user_images'
UPLOAD_FOLDER_2 = 'static/profile_pic'
UPLOAD_FOLDER_3 = 'static/charity_pic'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2
app.config['UPLOAD_FOLDER_3'] = UPLOAD_FOLDER_3

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if "logged_in" in session and session['logged_in']:
		if request.method == 'POST':
			failed = None
			list1=[]
			# check if the post request has the file part
			if 'file' not in request.files:
				print('No file part')
				return redirect(request.url)
			file = request.files['file']
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				return redirect(request.url)
			if file and allowed_file(file.filename):
				a= database.get_last_id()
				response = model.predict_by_filename('/home/meet/Desktop/labs/y2l-apis-continued/frame0.jpg')
				f = response["outputs"]
				if a ==None:
					for frame in f:
						for concept in frame["data"]["concepts"]:
							list1.append(concept["name"])
					for i in range (len(list1)):
							database.add_keyword(list1[i], 1)
					keywords1 = request.form["keywords1"]
					if keywords1 == '':
						d = None
					else:
						database.add_keyword(keywords1, 1)
					keywords2 = request.form["keywords2"]
					if keywords2 == "":
						b = None
					else:
						database.add_keyword(keywords2, 1)
					keywords3 = request.form["keywords3"]
					if keywords3 == '':
						c = None
					else:
						database.add_keyword(keywords3, 1)
				else:
					for frame in f:
						for concept in frame["data"]["concepts"]:
							database.add_keyword((' %s ' % (concept["name"])), a.id+1)
	
					keywords1 = request.form["keywords1"]
					if keywords1 == '':
						d = None
					else:
						database.add_keyword(keywords1, a.id+1)
					keywords2 = request.form["keywords2"]
					if keywords2 == "":
						b = None
					else:
						database.add_keyword(keywords2, a.id+1)
					keywords3 = request.form["keywords3"]
					if keywords3 == '':
						c = None
					else:
						database.add_keyword(keywords3, a.id+1)
				
				b = file.filename
				if a ==None:
					f= str(1)+"."+b.rsplit('.', 1)[1].lower()
				else:
					f = str((int(a.id) +1))+"." + b.rsplit('.', 1)[1].lower()
				target = os.path.join(app.config['UPLOAD_FOLDER'], f)
				file.save(target)
				print(session['id'])
				c=database.get_user_by_id(session['id'])
				y = c.username
				price = request.form["price"]
				currency = request.form["currency"]
				percentage = request.form["percentage"]
				database.add_photo(f, session['id'],y, price,currency,percentage)
				return redirect(url_for('home_page'))
			if file and not allowed_file(file.filename):
				failed = True
				return render_template("upload.html", failed = failed)

		return render_template("upload.html")
	else:
		return redirect(url_for("home_page"))


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
# 	return send_from_directory(app.config['UPLOAD_FOLDER'],
# 							   filename)

@app.route('/', methods = ["POST", "GET"])
def home_page():
	list1 = []
	if "logged_in" in session and session['logged_in']:
		print(session["id"])
		photos = database.get_all_photos()
		print(photos)
		random.shuffle(photos)
		random.shuffle(photos)
		for i in photos:
			d= database.get_user_by_id(i.user_id)
			list1.append(d)
		return render_template("logged_in_homepage.html", photos = photos, list1=list1)
	else:
		return render_template("homepage.html")
#does the'username' thingi work?


#####################USERS#######################
@app.route("/signup", methods=["POST","GET"])
def signup():
	if "logged_in" in session and session['logged_in']:
		return redirect(url_for("home_page"))
	else:
		if request.method =='POST':	
			username = request.form['username']
			email = request.form['email']
			password = request.form['password']
			failed = None
				# check if the post request has the file part
			if 'file' not in request.files:
				print('No file part')
				return redirect(request.url)
			file = request.files['file']
				# if user does not select file, browser also
				# submit a empty part without filename
			if file.filename == '':
				return redirect(request.url)
			if file and allowed_file(file.filename):
				a= database.get_last_user_id()
				b = file.filename
				if a ==None:
					f= str(1)+"."+b.rsplit('.', 1)[1].lower()
				else:
					f = str((int(a.id) +1))+"." + b.rsplit('.', 1)[1].lower()
				target = os.path.join(app.config['UPLOAD_FOLDER_2'], f)
				file.save(target)
				
				database.create_user(username, email, password,f)
				person = database.get_user(username)
				d = database.get_photos_by_user_id(person.id)
				
	# ###########################IMPORTANT Q: how to create a new name for session['pics(1/2/3/4/5/6/7/....)'] everytime it goes through the for loop
				return redirect(url_for('home_page'))
			if file and not allowed_file(file.filename):
				failed = True
				return render_template("signup.html", failed = failed)
		else:
			return render_template("signup.html")

@app.route("/login", methods=["POST","GET"])
def signin():
	passs= None
	uuuu = None
	if "logged_in" in session and session['logged_in']:
		return redirect(url_for("home_page"))
	else:
		if request.method =='POST':
			u = request.form['username']
			p = request.form['password']
			person = database.get_user(u)
			if database.get_user(u) == None:
				not_u = True
				return render_template("login.html", not_u =not_u)
			elif person.username == u and person.password == p:
				a = database.get_photos_by_user_id(person.id)
				session['logged_in'] = True
				session['id'] = person.id
				session['username'] = person.username
				session['password'] = person.password
				session['email'] = person.email
				session['followers'] = person.followers
				session['following'] = person.following
				session['profile_pic'] = person.profile_pic
				for b in a :
					session['pics']= b.pic
				return redirect(url_for("home_page"))
			elif person.username == u and person.password != p:
				not_p = True
				return render_template("login.html", not_p= not_p)
		else:
			return render_template("login.html")


@app.route("/logout", methods=["POST","GET"])
def logout():
	if "logged_in" in session and session['logged_in']:
		del session["logged_in"]
	
	return redirect(url_for("home_page"))


											 
@app.route ('/user/<string:username>')
def profile(username):
	list1=[]
	if "logged_in" in session and session['logged_in']:
		
		user = database.get_user(username)
		pics = database.get_photos_by_user_id(user.id)
		for i in pics:
			a = i.id
			list1.append(a)
		print(list1)
		list1.sort(reverse=True) 
		print(list1.sort(reverse=True))
		return render_template("profilepage.html", user=user, pics = pics)
	else:
		return redirect(url_for("home_page"))

# @app.route("/user/<string:username>/follow")
# def follow(username):
# 	if "logged_in" in session and session['logged_in']:
# 		user = database.get_user(username)
# 		database.follow_now(user.username)
# 		return redirect(url_for("profile", username = user.username)) and render_template(user = user)
# 	else:
# 		return redirect(url_for("home_page"))
# @app.route('/user/<string:username>/followers')
# def followers_user(username):
# 	user = database.get_user(username)
# 	return render_template("followers_page.html", user=user)


# @app.route('/user/<string:username>/following')
# def following_user(username):
# 	user = database.get_user(username)
# 	#find out how to do user.following here
# 	return render_template("following_page.html", user=user)

##################CHARITIES#####################

@app.route ("/add_charity", methods = ["POST","GET"])
def new_charity():
	if request.method =='POST':	
				# check if the post request has the file part

		file = request.files['file']
				# if user does not select file, browser also
				# submit a empty part without filename
		if file.filename == '':
			return redirect(request.url)
		if file and allowed_file(file.filename):
			a = database.get_last_charity_id()
			b = file.filename
			if a ==None:
					f= str(1)+"."+b.rsplit('.', 1)[1].lower()
			else:
				f = str((int(a.id) +1))+"." + b.rsplit('.', 1)[1].lower()
			target = os.path.join(app.config['UPLOAD_FOLDER_3'], f)
			file.save(target)
			name = request.form['name']
			cause = request.form['cause']
			email = request.form['email']
			website = request.form['website']
			short_intro = request.form['short_intro']
			paragraph = request.form['paragraph']
			database.create_charity(name, cause, email, website,f,short_intro,paragraph)
			return redirect(url_for("home_page"))
	else:
		return render_template("new_charity.html")


@app.route('/charities')
def all_charities():
	j = None
	if "logged_in" in session and session['logged_in']:
		j= True
	charities = database.get_all_charities()
	return render_template("all_charities.html",charities=charities, j = j)


@app.route('/charities/<int:id>')
def charity_page(id):
	j = None
	if "logged_in" in session and session['logged_in']:
		j= True
	charity = database.get_charity_by_id(id)
	return render_template("charitypage.html", charity = charity, j =j )

####################SEARCH##########################

@app.route('/results',  methods= ["POST","GET"])
def results():

	if "logged_in" in session and session['logged_in']:
		if request.method =='POST':	 
			a = None
			user_search = None
			results = []
			if request.form['search_type'] == "users":
				results = database.get_users(request.form['search'])
				user_search = True
				if results == None:
					a = True
				return render_template("searchpage.html",results=results, a=a,user_search=user_search)
		 
			if request.form['search_type'] == "images":
				path = database.get_photo_id_by_keywords(request.form['search'])
				print(path)
				for i in path:
					results.append (database.get_photo_by_id(i.pic_id))

				user_search = False
				if results == None:
					a = True
				return render_template("searchpage.html",results=results, a=a,user_search=user_search)
			else:
				return redirect(url_for("home_page"))
		else:
			return render_template("searchpage.html")
	else:
		return redirect(url_for("home_page"))

####################EXTRAS########################

@app.route('/aboutus')
def about():
	j = None
	if "logged_in" in session and session['logged_in']:
		j= True
	return render_template("aboutus.html", j = j)

@app.route('/image/<string:pic>')
def clicked_img(pic):

	photo = database.get_photo_by_name(pic)
	user = database.get_user_by_id(photo.user_id)
	return render_template("img_selected.html", photo = photo, user = user)
@app.route("/image/<string:pic>/buy_now")
def buy_now(pic):

	charities  = database.get_all_charities()
	photo = database.get_photo_by_name(pic)
	user = database.get_user_by_id(photo.user_id)
	return render_template("buy.html", photo = photo, user = user, charities=charities)
if __name__ == '__main__':
	app.secret_key = 'yay'
	# app.config['SESSION_TYPE'] = 'sqlalchemy'
	#  memcached or filesystem or  mongodb or redis???
	# sess.init_app(app)
	app.run(debug = True)