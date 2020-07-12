from init import db
from datetime import datetime


class User(db.Model):

	userID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(64), nullable=True)
	password = db.Column(db.String(64), nullable=True)
	team = db.Column(db.String(64), nullable=True)
	role = db.Column(db.String(64))

	def __repr__(self):
		return f"User('{self.userID}','{self.name}')"

	def get_id(self):
		return '{}'.format(self.userID)


class Survey(db.Model):

	surveyID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	instructorName = db.Column(db.String(64), nullable=False)
	name = db.Column(db.String(64), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Survey('{self.instructorName}','{self.name})'"

	def get_id(self):
		return '{}'.format(self.surveyID)

	def get_instructor(self):
		return '{}'.format(self.instructorName)

	def get_name(self):
		return '{}'.format(self.name)


class Question(db.Model):

	questionID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	label = db.Column(db.String(64))
	type = db.Column(db.String(10), nullable=False)
	repetition = db.Column(db.String(15))
	content = db.Column(db.String(300), nullable=True)
	surveyID = db.Column(db.Integer, db.ForeignKey('survey.surveyID'))
	survey = db.relationship('Survey', backref='survey_questions')

	def __repr__(self):
		return f"Question('{self.questionID}','{self.type}','{self.repetition}','{self.content}','{self.surveyID}')"

	def get_id(self):
		return '{}'.format(self.questionID)

	def get_survey_id(self):
		return '{}'.format(self.surveyID)

	def get_label(self):
		return '{}'.format(self.label)

	def get_type(self):
		return '{}'.format(self.type)

	def get_repetition(self):
		return '{}'.format(self.repetition)

	def get_content(self):
		return '{}'.format(self.content)


class Option(db.Model):

	optionID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	label = db.Column(db.String(64))
	content = db.Column(db.String(300), nullable=False)
	questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)
	question = db.relationship('Question', backref='question_options')

	def __repr__(self):
		return f"Question('{self.optionID}','{self.questionID}','{self.content}')"

	def get_id(self):
		return '{}'.format(self.optionID)

	def get_label(self):
		return '{}'.format(self.label)

	def get_content(self):
		return '{}'.format(self.content)

	def get_question_id(self):
		return '{}'.format(self.questionID)




