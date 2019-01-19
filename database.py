from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users_charities.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_user(username, email, password,profile_pic):
	new_user = User(
		username = username,
		email = email,
		password = password,
		profile_pic = profile_pic,
		followers = 0,
		following = 0
		)
	session.add(new_user)
	session.commit()

def create_charity(name, cause, email, website,pic,short_intro, paragraph):
	new_charity = Charity(
		name = name,
		cause = cause,
		email = email,
		website = website,
		pic = pic,
		short_intro = intro,
		paragraph = paragraph
		)
	session.add(new_charity)
	session.commit()


def update_user():
	session.commit()

def update_charity():
	session.commit()

def get_user(username):
	user = session.query(User).filter_by(username= username).first()
 	# print(user)
	return user

def get_charity(id):
	charity = session.query(Charity).filter_by(id= id).first()
	return charity

def delete_user(username):
	session.query(User).filter_by(username= username).delete()
	session.commit()

def delete_charity(id):
	session.query(Charity).filter_by(id= id).delete()
	session.commit()
	
def request_recieve ():
	search_results=session.query(User).filter_by().first()
	return (search_results)

#search for users, charities & photo tags (option to pick which results to bring up like in insta)