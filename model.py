from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, ForeignKey
from flask import Flask, render_template, request, session, flash, url_for, redirect

app = Flask(__name__)


Base = declarative_base()

# Write your classes here :

class Keywords(Base):
	__tablename__ = "keywords"
	id =  Column(Integer, primary_key= True)
	keyword = Column(String)
	pic_id = Column(Integer, ForeignKey('photos.id'))
	pics = relationship("Photos", back_populates="keyword")
	def __repr__(self):
		return "%s" % self.keyword


class Photos(Base):
	__tablename__ = "photos"
	id = Column(Integer, primary_key= True)
	pic = Column(String)
	name = Column(String)
	user_id = Column(Integer, ForeignKey('users.id'))
	user_username = Column(String)
	price = Column(Integer)
	currency = Column(String)
	percentage = Column(Integer)
	user = relationship("User", back_populates="pics")

	def __repr__(self):
		return "<Photos(pic='%s')>" % self.pic
Photos.keyword = relationship("Keywords", back_populates="pics")

# class Follows(Base):
# 	__tablename__= "follows"
# 	names = Column(String, primary_key=True)
# 	"bob" follows "alice"
# 	"bob-alice"
# 	followed = Column(Integer, ForeignKey('users.id'))
# 	followed_by = Column(Integer, ForeignKey('users.id'))
# 	followed1 = relationship("User", foreign_keys ="Follows.followed")
# 	followed_by1 = relationship("User", foreign_keys ="Follows.followed_by")
# 	def __repr__(self):
# 		return "<Follows(followed='%i')>" % self.followed and "<Folllows(followed_by='%i')>" % self.followed_by

class User(Base):
	__tablename__ ="users"
	id = Column(Integer, primary_key= True)
	username = Column(String)
	email = Column(String)
	password = Column (String)
	profile_pic = Column (String)
	followers = Column(Integer)
	following = Column(Integer)
User.pics = relationship("Photos", order_by=Photos.id, back_populates="user")
# User.followed = relationship("Follows",order_by = Follows.id, foreign_keys = "followed1")
# User.followed_by = relationship("Follows",order_by = Follows.id, foreign_keys = "followed_by1")
#I need to ask about how the uploaded images are going to be stored since each image takes a collumn and i cant create infinite collums
##also ask about the username being the id and how that works


class Charity(Base):
	__tablename__ ="charities"
	id = Column(Integer, primary_key= True)
	name = Column(String)
	cause = Column(String)
	email = Column(String)
	website = Column (String)
	pic = Column (String)
	short_intro = Column(String)
	paragraph = Column(String)

		