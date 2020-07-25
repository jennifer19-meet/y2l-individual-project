from flask import Flask, render_template, request, session, flash, url_for, redirect,send_from_directory
# from flask_session.__init__ import Session
# to install ---> pip install Flask-Session
# from flask_session import Session
# OR from flask.ext.session import Session
# from sqlalchemy.orm import sessionmaker (?????????)
import random
from werkzeug.utils import secure_filename
import os.path
import json, requests
import database
from clarifai.rest import ClarifaiApp
from clarifai.errors import ApiError
import shutil
from currency_converter import CurrencyConverter

app = Flask(__name__)

# sess = Session()
######################NOT LOGGED IN###################
app1 = ClarifaiApp(api_key='081607dc569141dfb8ee36cd09759172')
model = app1.public_models.general_model
converter = CurrencyConverter()

UPLOAD_FOLDER = 'static/user_images'
UPLOAD_FOLDER_2 = 'static/profile_pic'
UPLOAD_FOLDER_3 = 'static/charity_pic'
UPLOAD_FOLDER_4 = ''
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2
app.config['UPLOAD_FOLDER_3'] = UPLOAD_FOLDER_3
app.config['UPLOAD_FOLDER_4'] = UPLOAD_FOLDER_4

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search(searched, db_txt): 
	num_of_letters_searched = len(searched) 
	num_of_letters_db_txt = len(db_txt) 
	found = None
	for i in range(num_of_letters_db_txt - num_of_letters_searched + 1): 
		j = 0
		  
		while(j < num_of_letters_searched): 
			if (db_txt[i + j] != searched[j]): 
				break
			j += 1

		if (j == num_of_letters_searched): 
			found = True 
			
	return found

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if "logged_in" in session and session['logged_in']:
		if request.method == 'POST':
			failed = None
			no_file = None
			list1=[]
			file = request.files['file']
			
			if file and allowed_file(file.filename):
				a= database.get_last_id()
				b = file.filename
				if a ==None:
					f= str(1)+"."+b.rsplit('.', 1)[1].lower()
				else:
					f = str((int(a.id) +1))+"." + b.rsplit('.', 1)[1].lower()
				target = os.path.join(app.config['UPLOAD_FOLDER'], f)
				file.save(target)
				response = model.predict_by_filename('/Users/DakMac/Desktop/jennyz/MEET/Whats on the meet laptop/labs/y2l-individual-project/static/user_images/'+f)
				frames = response["outputs"]
				if a ==None:
					for frame in frames:
						for concept in frame["data"]["concepts"]:
							list1.append(concept["name"])
					for i in range (10):
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
					for frame in frames:
						for concept in frame["data"]["concepts"]:
							list1.append(concept["name"])
					for i in range(10):
						database.add_keyword(list1[i], a.id+1)
	
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
		photos = database.get_all_photos()
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
			file = request.files['file']	
			failed = None	
			if file and allowed_file(file.filename):
				a= database.get_last_user_id()
				b = file.filename
				if a ==None:
					f= str(1)+"."+b.rsplit('.', 1)[1].lower()
				else:
					f = str((int(a.id) +1))+"." + b.rsplit('.', 1)[1].lower()
				target = os.path.join(app.config['UPLOAD_FOLDER_2'], f)
				file.save(target)
				database.create_user(username, email, password,f,0,0)
				
				
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
		a = True
		following = False
		user = database.get_user(username)
		pics = database.get_photos_by_user_id(user.id)
		followers = database.get_followers_for(user.id)
		for i in pics:
			a = i.id
			list1.append(a)
		list1.sort(reverse=True) 
		if user.id == session["id"]:
			a = False
		
		for i in range (len(followers)):
			if followers[i].followed_by == session["id"]:
				following = True
		return render_template("profilepage.html", user=user, pics = pics, a = a, following=following) 
	else:
		return redirect(url_for("home_page"))

@app.route("/user/<string:username>/follow")
def follow(username):
	if "logged_in" in session and session['logged_in']:
		b=None
		id_for_function = None
		user = database.get_user(username)
		followers = database.get_followers_for(user.id)
		for i in range (len(followers)):
			if followers[i].followed_by == session["id"]:
				 b= True
				 id_for_function= followers[i].id
		if b == True:
			database.unfollow_now(user.username, session["username"],id_for_function)
			
		else:
			database.follow_now(user.username, session["username"])
				
		return redirect(url_for("profile", username = user.username))
	else:
		return redirect(url_for("home_page"))
@app.route('/user/<string:username>/followers')
def followers_user(username):
	if "logged_in" in session and session['logged_in']:
		followers=[]
		number_of_photos =[]
		least_p=[]
		most_p=[]
		has_photos = []
		user= database.get_user(username)
		followers_2=database.get_followers_for(user.id)

		for i in range(len(followers_2)):
			followers.append(database.get_user_by_id(followers_2[i].followed_by))
			number_of_photos.append(len(database.get_photos_by_user_id(followers_2[i].followed_by)))
			prices=[]
			if number_of_photos[i] == 0:
				has_photos.append(False)
			else:
				has_photos.append(True)
				for j in database.get_photos_by_user_id(followers_2[i].followed_by):
					converted_p =converter.convert(j.price, j.currency, 'USD')
					prices.append(converted_p)
				least_p.append(min(prices))
				most_p.append(max(prices))
		return render_template("followers_page.html", followers=followers, user=user, number_of_photos=number_of_photos, least_p = least_p, most_p = most_p, has_photos=has_photos)
	else:
		return redirect(url_for("home_page"))


@app.route('/user/<string:username>/following')
def following_user(username):
	if "logged_in" in session and session['logged_in']:
		following =[]
		number_of_photos =[]
		least_p=[]
		most_p=[]
		has_photos = []
		user= database.get_user(username)
		following_2 = database.get_following_for(user.id)
		for i in range (len(following_2)):
			following.append(database.get_user_by_id(following_2[i].followed))
			number_of_photos.append(len(database.get_photos_by_user_id(following_2[i].followed)))
			
			prices=[]
			if number_of_photos[i] == 0:
				has_photos.append(False)
				
			else:
				has_photos.append(True)
				for j in database.get_photos_by_user_id(following_2[i].followed):
					converted_p =converter.convert(j.price, j.currency, 'USD')
					prices.append(converted_p)
				least_p.append(min(prices))
				most_p.append(max(prices))

		return render_template("following_page.html", following=following, user=user, number_of_photos=number_of_photos, least_p = least_p, most_p = most_p, has_photos=has_photos)
	else:
		return redirect(url_for("home_page"))

##################CHARITIES#####################

@app.route ("/add_charity", methods = ["POST","GET"])
def new_charity():
	if request.method =='POST':	
		file = request.files['file']
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
			age = request.form['age']
			short_intro = request.form['short_intro']
			paragraph = request.form['paragraph']
			database.create_charity(name, cause, email, website,age,f,short_intro,paragraph)
			return redirect(url_for("home_page"))
		elif file and not allowed_file(file.filename):
				failed = True
				return render_template("new_charity.html", failed = failed)
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
				number_of_photos =[]
				least_p=[]
				most_p=[]
				has_photos = []
				all_users= database.get_all_users()
				for i in range (len(all_users)):
					found = search(request.form['search'].lower(),all_users[i].username.lower())
					if found == True:
						if all_users[i] not in results:
							results.append(all_users[i])
							number_of_photos.append(len(database.get_photos_by_user_id(all_users[i].id)))
							prices=[]
							if number_of_photos[-1] == 0:
								has_photos.append(False)
								
							else:
								has_photos.append(True)
								for j in database.get_photos_by_user_id(all_users[i].id):
									converted_p =converter.convert(j.price, j.currency, 'USD')
									prices.append(converted_p)
								least_p.append(min(prices))
								most_p.append(max(prices))
				# results = database.get_users(request.form['search'])
				user_search = True
				if results == []:
					a = True
				return render_template("searchpage.html",results=results, a=a,user_search=user_search, search=True, number_of_photos=number_of_photos, least_p = least_p, most_p = most_p, has_photos=has_photos)
		 
			if request.form['search_type'] == "images":
				# path = database.get_photo_id_by_keywords(request.form['search'])
				# print(path)
				# for i in path:
				# 	results.append(database.get_photo_by_id(i.pic_id))
				all_keywords= database.get_all_keywords()
				for i in range (len(all_keywords)):
					found = search(request.form['search'].lower(),all_keywords[i].keyword.lower())
					if found == True:
						photo = database.get_photo_by_id(all_keywords[i].pic_id)
						if photo not in results:
							results.append(photo)
				user_search = False
				if results == []:
					a = True
				return render_template("searchpage.html",results=results, a=a,user_search=user_search, search=True)
			else:
				return redirect(url_for("home_page"))
		else:
			return render_template("searchpage.html")
	else:
		return redirect(url_for("home_page"))


@app.route('/similar_keywords/<string:keyword>')
def similar_keys(keyword):
	if "logged_in" in session and session['logged_in']:
		results = []
		all_keywords= database.get_all_keywords()
		for i in range (len(all_keywords)-1):
			found = search(keyword.lower(),all_keywords[i].keyword.lower())
			if found == True:
				photo = database.get_photo_by_id(all_keywords[i].pic_id)
				if photo not in results:
					results.append(photo)
		return render_template("searchpage.html",results=results, a=None,user_search=False, search=False, keyword=keyword)
####################EXTRAS########################

@app.route('/aboutus')
def about():
	j = None
	if "logged_in" in session and session['logged_in']:
		j= True
	return render_template("about.html", j = j)

@app.route('/image/<string:pic>', methods= ['POST', 'GET'])
def clicked_img(pic):
	charities  = database.get_all_charities()
	photo = database.get_photo_by_name(pic)
	user = database.get_user_by_id(photo.user_id)
	percent_price=photo.percentage*.01*photo.price
	if request.method == 'POST':	
		return render_template("img_selected.html", photo = photo, user = user,charities=charities,buy=True, percent_price=percent_price)
	elif request.method== 'GET':
		return render_template("img_selected.html", photo = photo, user = user,charities=charities,buy=False, percent_price=percent_price)





if __name__ == '__main__':
	app.secret_key = 'yay'
	# app.config['SESSION_TYPE'] = 'sqlalchemy'
	#  memcached or filesystem or  mongodb or redis???
	# sess.init_app(app)
	app.run(debug = True)