from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


UPLOAD_FOLDER = '/static/img/profile_pic/<user.id>'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

Base = declarative_base()

# Write your classes here :
class User(Base):
	__tablename__ ="users"
	id = Column(Integer, primary_key= True)
	username = Column(String)
	email = Column(String)
	password = Column (String)
	profile_pic = Column (String)
	followers = Column(Integer)
	following = Column(Integer)

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
