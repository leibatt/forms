from wtforms import Form, BooleanField, TextField, validators
from database import db_session
import models

class BaseSurveyForm(Form):
	username     = TextField('Username', [validators.Length(min=4, max=25,message="must be 4-25 characters")])
	email        = TextField('Email Address', [validators.Length(min=6),validators.Email(message="this doesn't seem like an email")])
	password        = TextField('Password', [validators.Length(min=6, max=35,message="must be 6-35 characters")])
	accept_rules = BooleanField('I accept the site rules', [validators.Required(message="must accept site rules to proceed")])

def show_survey(survey_name):
	survey_questions = get_survey_questions(survey_name) #list of model question objects

	class SurveyInstanceForm(BaseSurveyForm):
		pass

	for question in survey_questions:
		print question

	form = SurveyInstanceForm(request.form)

def get_survey_questions(survey_name):
	survey = db_session.query(models.Survey).filter_by(name=survey_name).one()
	print "survey id:",survey.id
	survey_id = survey.id # better be a number
	questions = db_session.query(models.SurveyQuestion).filter_by(survey_id=survey_id).all()
	return questions
