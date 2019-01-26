from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users_charities.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

#######################CREATE#####################################

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
create_user("j", "j.com","jk","hi")
def create_charity(name, cause, email, website,pic,short_intro, paragraph):
	new_charity = Charity(
		name = name,
		cause = cause,
		email = email,
		website = website,
		pic = pic,
		short_intro = short_intro,
		paragraph = paragraph
		)
	session.add(new_charity)
	session.commit()

create_charity("save the pandas","animals", "sunflowermaster234@yahoo.com", "www.pandas.com", "hi","here at san diagos very own save the pandas we aim to increase there natural diversity in the wild and make them healthy again","PPPPPPPPPPPPPPPPPPPPAAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRRRRAAAAAAAAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRAAAAAAAAAAAAAAAAAAAAAAAAPPPPPPPPPPPPPPPPPPPPPPPPPPHHHHHHHHHHHHHHHHHHHHHHH")

def add_photo(pic,keywords, user_id,user_username, price,currency,percentage):
	new_photo = Photos(
		pic = pic,
		keywords = keywords,
		user_id = user_id,
		user_username=user_username, 
		price = price,
		currency = currency,
		percentage=percentage
		)
	session.add(new_photo)
	session.commit()
add_photo("lantern","animal,cute,china", 1, "j", 10, "dollar",25)

###########################UPDATE###################################
def follow_now(username):
	followed  = session.query(User).filter_by(username = username).first()
	f = user.followers
	user.followers =f +1
	session.commit()
	return user

def update_user():
	session.commit()

def update_charity():
	session.commit()

###########################GET/SEARCH################################


def get_user(username):
	user = session.query(User).filter_by(username= username).first()
 	# print(user)
	return user

def get_users(username):
	user = session.query(User).filter_by(username= username).all()
	# print(user)
	return user

def get_user_by_id(id):
	user = session.query(User).filter_by(id= id).first()
	return user

def get_last_user_id():
	user = session.query(User).order_by(User.id.desc()).first()
	return user

def get_charity_by_id(id):
	charity = session.query(Charity).filter_by(id= id).first()
	return charity

def get_charity_by_name(name):
	charity = session.query(Charity).filter_by(name=name).all()
	return charity

def get_last_charity_id():
	charity  = session.query(Charity).order_by(Charity.id.desc()).first()
	return charity

def get_photos_by_user_id(user_id):
	photos = session.query(Photos).filter_by(user_id=user_id).all()
	return photos

def get_photo_by_keywords(keywords):
	photos = session.query(Photos).filter_by(keywords=keywords).all()
	return photos

def get_photo_by_name(pic):
	photo = session.query(Photos).filter_by(pic=pic).first()
	return photo

def get_all_photos():
	photos = session.query(Photos).all()
	return photos

def get_last_id():
	photo = session.query(Photos).order_by(Photos.id.desc()).first()
	return photo

def get_photos_desc():
	photo = session.query(Photos).order_by(Photos.id.desc()).all()
	return photo

def get_all_charities():
    charities = session.query(Charity).all()
    return charities

###########################DELETE###################################

def delete_user(username):
	session.query(User).filter_by(username= username).delete()
	session.commit()

def delete_charity(id):
	session.query(Charity).filter_by(id= id).delete()
	session.commit()

def delete_photo(id):
	session.query(Photos).filter_by(id=id).delete()
	session.commit()
# a = get_last_id()


# print(a.id)
#search for users, charities & photo tags (option to pick which results to bring up like in insta)