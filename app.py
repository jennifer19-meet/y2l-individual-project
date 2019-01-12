from flask import *
import json, requests
from database import *

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template("homepage.html")

	
@app.route('/<"insert charity name">')
def charity_page():
	return render_template("charitypage.html")


@app.route('/aboutus')
def about():
	return render_template("aboutus.html")


@app.route('/results')
def results():
	return render_template("searchpage.html")


@app.route ('/<str:username>')
def profile():
	return render_template("profilepage.html")


if __name__ == '__main__':
	app.run(debug = True)