from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Write your classes here :
class User(Base):
	__tablename__ ="Information about users"
	username = Column(String, primary_key= True)
	email = Column(String)
	password = Column (String)
	profile_pic = Column (BLOB)
	followers = Column(Integer)
	following = Column(Integer)

#I need to ask about how the uploaded images are going to be stored since each image takes a collumn and i cant create infinite collums
##also ask about the username being the id and how that works


class Charity(Base):
	__tablename__ ="Information about charities"
	id = Column(Integer, primary_key= True)
	name = Column(String)
	cause = Column(String)
	email = Column(String)
	website = Column (String)
	pic = Column (BLOB)
	intro = Column(String)
