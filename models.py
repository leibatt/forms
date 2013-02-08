from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from database import Base
import datetime

#table storing all users by flask session id,
#and whether they did the surveys
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	#has to have a valid session id
	flask_session_id = Column(String(50),unique=True, nullable=False)

	def __init__(self, flask_session_id):
		self.flask_session_id = flask_session_id

	def __repr__(self):
		return "User(%r)" % (self.flask_session_id)

#table storing all survey names
class Survey(Base):
	__tablename__ = "surveys"
	id = Column(Integer, primary_key=True)
	name = Column(String(10),nullable=False)

	def __init__(self,name):
		self.name = name

	def __repr__(self):
		return "Survey(%r)" % (self.name)

#table storing all questions for all surveys
class SurveyQuestion(Base):
	__tablename__ = "survey_questions"
	id = Column(Integer, primary_key=True) # question id
	question_text = Column(Text, nullable=False) #text of the question
	input_type = Column(String(50),nullable=False) #checkboxes, menus, textbox, etc.
	response_type = Column(String(10)) #number, string, null if checkbox
	parent_question = Column(Integer) # if this is a subquestion, which question is the parent
	survey_id = Column(Integer,ForeignKey("surveys.id"),nullable=False) #which survey this is

	survey = relationship("Survey",backref=backref('questions'))

	#questions must be unique for each survey
	__table_args__ = (UniqueConstraint('survey_id', 'question_text', name='uix_1'),)

	def __init__(self,question_text,input_type,response_type,parent_question,survey_id):
		self.survey_id = survey_id
		self.question_text = question_text
		self.input_type = input_type
		self.response_type = response_type
		self.parent_question = parent_question

	def __repr__(self):
		return "SurveyQuestion(%r, %r, %r)" % (self.survey_id,self.question_text,self.input_type)

#table storing predefined answers for relevant survey questions
class SurveyResponse(Base):
	__tablename__ = "survey_responses"
	id = Column(Integer,primary_key=True)
	value = Column(String(150),nullable=False)
	question_id = Column(Integer,ForeignKey("survey_questions.id"),nullable=False)

	question = relationship("SurveyQuestion",backref=backref("responses"))

	#responses must be unique for each question
	__table_args__ = (UniqueConstraint('question_id', 'value', name='uix_2'),)

	def __init__(self,value,question_id):
		self.value = value
		self.question_id = question_id

	def __repr__(self):
		return "SurveyResponse(%r, %r)" % (self.question_id,self.value)

class UserResponse(Base):
	__tablename__ = "user_responses"
	value = Column(Text) #user's response text, may be empty or null
	comment = Column(Text) # additional comments from user (i.e. elaborate on "Other")
	user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
	question_id = Column(Integer,ForeignKey("survey_questions.id"),primary_key=True)
	response_id = Column(Integer,ForeignKey("survey_responses.id")) #may not have predefined survey response
	timestamp = Column(DateTime)

	user = relationship("User",backref=backref("responses"))
	question = relationship("SurveyQuestion",backref=backref("user_responses"))
	response = relationship("SurveyResponse",backref=backref("user_responses"))

	def __init__(self,value,comment,user_id,question_id,response_id):
		self.user_id = user_id
		self.question_id = question_id
		self.response_id = response_id
		self.value = value
		self.comment = comment
		self.timestamp = datetime.datetime.now()

	def __repr__(self):
		return "UserResponse(%r, %r, %r, %r, %r)" % (self.user_id,self.question_id,self.response_id,self.value,self.timestamp)

# user movement history
class UserTrace(Base):
	__tablename__ = "user_traces"
	id = Column(Integer,primary_key=True)
	tile_id = Column(Text,nullable=False)
	timestamp = Column(DateTime(timezone=True),nullable=False)
	query = Column(Text,nullable=False) # must know what query was run
	user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
	dataset_id = Column(Integer,ForeignKey("data_sets.id")) # dataset used? may be null, but hopefully isn't

	user = relationship("User",backref=backref("traces"))
	dataset = relationship("DataSet",backref=backref("traces"))

	def __init__(self,tile_id,query,user_id,dataset_id):
		self.user_id = user_id
		self.tile_id = tile_id
		self.timestamp = datetime.datetime.now()
		self.query = query
		self.dataset_id = dataset_id

	def __repr__():
		return "UserTrace(%r, %r, %r, %r, %r, %r)" % (self.user_id,self.tile_id,self.query,self.dataset_id,self.timestamp)

# predetermined data sets
class DataSet(Base):
	__tablename__ = "data_sets"
	id = Column(Integer,primary_key=True)
	name = Column(String(50),unique=True,nullable=False)
	query = Column(Text,unique=True,nullable=False)

	def __init__(self,name,query):
		self.name = name
		self.query = query

	def __repr__():
		return "DataSet(%r, %r)" % (self.name,self.query)


