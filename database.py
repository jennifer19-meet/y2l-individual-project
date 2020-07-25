from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///picnchoose.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

#######################CREATE#####################################

def create_user(username, email, password,profile_pic,followers,following):
	new_user = User(
		username = username,
		email = email,
		password = password,
		profile_pic = profile_pic,
		followers = followers,
		following = following
		)
	session.add(new_user)
	session.commit()
# create_user("j", "j.com","jk","hi", 0, 0)
def create_charity(name, cause, email, website,age,pic,short_intro, paragraph):
	new_charity = Charity(
		name = name,
		cause = cause,
		email = email,
		website = website,
		age = age,
		pic = pic,
		short_intro = short_intro,
		paragraph = paragraph
		)
	session.add(new_charity)
	session.commit()

# create_charity("save the pandas","animals", "sunflowermaster234@yahoo.com", "www.pandas.com", "hi","here at san diagos very own save the pandas we aim to increase there natural diversity in the wild and make them healthy again","PPPPPPPPPPPPPPPPPPPPAAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRRRRAAAAAAAAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRAAAAAAAAAAAAAAAAAAAAAAAAPPPPPPPPPPPPPPPPPPPPPPPPPPHHHHHHHHHHHHHHHHHHHHHHH")

def add_photo(pic, user_id,user_username, price,currency,percentage):
	new_photo = Photos(
		pic = pic,
		user_id = user_id,
		user_username=user_username, 
		price = price,
		currency = currency,
		percentage=percentage
		)
	session.add(new_photo)
	session.commit()
# add_photo("lantern", 1, "j", 10, "dollar",25)
def add_keyword(keyword, pic_id):
	new_keyword = Keywords(
		keyword = keyword,
		pic_id = pic_id
		)
	session.add(new_keyword)
	session.commit()
# add_keyword("panda",1)

def add_follower(followed,followed_by):
	new_follower = Follows(
		followed = followed,
		followed_by =followed_by
		)
	session.add(new_follower)
	session.commit()

def remove_follow(id):
	session.query(Follows).filter_by(id= id).delete()
	session.commit()
###########################UPDATE###################################
def follow_now(username, now_username):
	user  = session.query(User).filter_by(username = username).first()
	user.followers=user.followers+1
	user_now = session.query(User).filter_by(username= now_username).first()
	user_now.following =user_now.following+1
	add_follower(user.id,user_now.id)
	print (user.followers)
	print (user_now.following)
	session.commit()
	return user

def unfollow_now(username, now_username,f_id):
	user  = session.query(User).filter_by(username = username).first()
	user.followers=user.followers-1
	user_now = session.query(User).filter_by(username= now_username).first()
	user_now.following =user_now.following-1
	remove_follow(f_id)
	print (user.followers)
	print (user_now.following)
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

def get_photo_id_by_keywords(keyword):
	photo_id = session.query(Keywords).filter_by(keyword=keyword).all()
	return photo_id

def get_photo_by_name(pic):
	photo = session.query(Photos).filter_by(pic=pic).first()
	return photo

def get_photo_by_id(id):
	photo = session.query(Photos).filter_by(id=id).first()
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

def get_all_users():
    users = session.query(User).all()
    return users

def get_all_keywords():
    keywords = session.query(Keywords).all()
    return keywords
def get_followers_for(followed):
	followers= session.query(Follows).filter_by(followed = followed).all()
	return followers
def get_following_for(followed_by):
	following= session.query(Follows).filter_by(followed_by = followed_by).all()
	return following
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
# delete_photo(1)
# a = get_last_id()
# # delete_user("jen")
# delete_user("Olive3")
# print(a.id)
#search for users, charities & photo tags (option to pick which results to bring up like in insta)