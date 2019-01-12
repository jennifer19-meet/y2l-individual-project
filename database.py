from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///cats.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_user():
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

def create_charity():
	new_charity = Charity(
		name = name,
		cause = cause,
		email = email,
		website = website,
		pic = pic,
		intro = intro
		)
	session.add(new_charity)
	session.commit()


def update_user():
	pass

def update_charity():
	pass

def delete_user():
	session.query(User).filter_by(username= username).delete()
	session.commit()

def delete_charity():
	session.query(Charity).filter_by(id= id).delete()
	session.commit()
	
def request_recieve ():
	search_results=session.query(User).filter_by().first()
	return (search_results)

#search for users, charities & photo tags (option to pick which results to bring up like in insta)