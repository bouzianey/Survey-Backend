from init import db
from datetime import datetime
from flask_login import UserMixin


class Classtb(db.Model):

	classID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	className = db.Column(db.String(64), nullable=False)
	instructorID = db.Column(db.Integer, db.ForeignKey('instructor.instructorID'))
	instructor = db.relationship('Instructor', backref='class_instructor')

	def __repr__(self):
		return f"Class('{self.classID}','{self.className}')"

	def get_id(self):
		return '{}'.format(self.classID)

	def get_class_name(self):
		return '{}'.format(self.className)

	def get_instructor_id(self):
		return '{}'.format(self.instructorID)


class Team(db.Model):

	teamID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	teamName = db.Column(db.String(64), nullable=False)
	classID = db.Column(db.Integer, db.ForeignKey('classtb.classID'))
	classtb = db.relationship('Classtb', backref='class_team')

	def __repr__(self):
		return f"Team('{self.teamID}','{self.teamName}')"

	def get_id(self):
		return '{}'.format(self.teamID)

	def get_team_name(self):
		return '{}'.format(self.teamName)

	def get_class_id(self):
		return '{}'.format(self.classID)


class Instructor(db.Model):

	instructorID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	instructorName = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(64), nullable=True)
	password = db.Column(db.String(64), nullable=True)

	def __repr__(self):
		return f"Instructor('{self.instructorID}','{self.instructorName}')"

	def get_id(self):
		return '{}'.format(self.instructorID)

	def get_instructor_name(self):
		return '{}'.format(self.instructorName)

	def get_email(self):
		return '{}'.format(self.email)

	def get_password(self):
		return '{}'.format(self.password)


class User(db.Model):

	userID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	userName = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	teamID = db.Column(db.Integer, db.ForeignKey('team.teamID'))
	team = db.relationship('Team', backref='team_user')

	def __repr__(self):
		return f"User('{self.userID}','{self.userName}')"

	def get_id(self):
		return '{}'.format(self.userID)

	def get_email(self):
		return '{}'.format(self.email)

	def get_name(self):
		return '{}'.format(self.userName)

	def get_team_id(self):
		return '{}'.format(self.teamID)


class SurveyClass(db.Model):

	SurveyClassID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	surveyID = db.Column(db.Integer, db.ForeignKey('survey.surveyID'), nullable=False)
	classID = db.Column(db.Integer, db.ForeignKey('classtb.classID'), nullable=False)
	classtb = db.relationship('Classtb', backref='survey_class')

	def __repr__(self):
		return f"SurveyClass('{self.SurveyClassID}')"

	def get_class_id(self):
		return '{}'.format(self.classID)

	def get_survey_class_id(self):
		return '{}'.format(self.SurveyClassID)

	def get_survey_id(self):
		return '{}'.format(self.surveyID)


class Survey(db.Model):

	surveyID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	instructorName = db.Column(db.String(64), nullable=False)
	name = db.Column(db.String(64), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	instructorID = db.Column(db.Integer, db.ForeignKey('instructor.instructorID'), nullable=False)
	instructor = db.relationship('Instructor', backref='survey_instructor')

	def __repr__(self):
		return f"Survey('{self.instructorName}','{self.name})'"

	def get_id(self):
		return '{}'.format(self.surveyID)

	def get_instructor(self):
		return '{}'.format(self.instructorName)

	def get_name(self):
		return '{}'.format(self.name)

	def get_date(self):
		return '{}'.format(self.date)


class Question(db.Model):

	questionID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	label = db.Column(db.String(64))
	type = db.Column(db.String(10), nullable=False)
	repetition = db.Column(db.String(15))
	content = db.Column(db.String(300), nullable=True)
	surveyID = db.Column(db.Integer, db.ForeignKey('survey.surveyID'), nullable=False)
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
		return f"Option('{self.optionID}','{self.questionID}','{self.content}')"

	def get_id(self):
		return '{}'.format(self.optionID)

	def get_label(self):
		return '{}'.format(self.label)

	def get_content(self):
		return '{}'.format(self.content)

	def get_question_id(self):
		return '{}'.format(self.questionID)


class Surveyresponse(db.Model):

	surveyResponseID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	surveyName = db.Column(db.String(100), nullable=True)
	surveyID = db.Column(db.Integer, db.ForeignKey('survey.surveyID'), nullable=False)
	studentID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
	user = db.relationship('User', backref='response_student')

	def __repr__(self):
		return f"SurveyResponse('{self.surveyResponseID}')"

	def get_response_id(self):
		return '{}'.format(self.surveyResponseID)

	def get_survey_id(self):
		return '{}'.format(self.surveyID)

	def get_survey_name(self):
		return '{}'.format(self.surveyName)

	def get_student_id(self):
		return '{}'.format(self.studentID)


class Questionresponse(db.Model):
	questionResponseID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	type = db.Column(db.String(10), nullable=False)
	content = db.Column(db.String(300), nullable=False)
	author_id = db.Column(db.Integer, nullable=False)
	author_name = db.Column(db.String(20), nullable=False)
	student_ID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
	questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)
	surveyResponseID = db.Column(db.Integer, db.ForeignKey('surveyresponse.surveyResponseID'), nullable=False)
	surveyresponse = db.relationship('Surveyresponse', backref='question_response')

	def __repr__(self):
		return f"Questionresponse('{self.questionResponseID}','{self.type}','{self.content}')"

	def get_id(self):
		return '{}'.format(self.questionResponseID)

	def get_student_id(self):
		return '{}'.format(self.student_ID)

	def get_author_name(self):
		return '{}'.format(self.author_name)

	def get_author_id(self):
		return '{}'.format(self.author_id)

	def get_survey_response_id(self):
		return '{}'.format(self.surveyResponseID)

	def get_question_id(self):
		return '{}'.format(self.questionID)

	def get_type(self):
		return '{}'.format(self.type)

	def get_content(self):
		return '{}'.format(self.content)

	def get_content(self):
		return '{}'.format(self.content)


class Optionresponse(db.Model):
	optionResponseID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	content = db.Column(db.Integer, nullable=False)
	author_id = db.Column(db.Integer, nullable=False)
	author_name = db.Column(db.String(20), nullable=False)
	questionResponseID = db.Column(db.Integer, db.ForeignKey('questionresponse.questionResponseID'), nullable=False)
	questionresponse = db.relationship('Questionresponse', backref='question_response')

	def __repr__(self):
		return f"Optionresponse('{self.optionResponseID}','{self.content}')"

	def get_id(self):
		return '{}'.format(self.optionResponseID)

	def get_content(self):
		return '{}'.format(self.content)

	def get_author_name(self):
		return '{}'.format(self.author_name)

	def get_author_id(self):
		return '{}'.format(self.author_id)

	def get_question_response_id(self):
		return '{}'.format(self.questionResponseID)


class ProFeedback(db.Model):

	feedbackID = db.Column(db.Integer, autoincrement=True, primary_key=True)
	surveyName = db.Column(db.String(64), nullable=False)
	dt_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.String(500), nullable=False)
	userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
	surveyID = db.Column(db.Integer, db.ForeignKey('survey.surveyID'))
	survey = db.relationship('Survey', backref='survey_feedback')

	def __repr__(self):
		return f"Feedback('{self.feedbackID}','{self.surveyName}')"

	def get_id(self):
		return '{}'.format(self.feedbackID)

	def get_survey_name(self):
		return '{}'.format(self.surveyName)

	def get_content(self):
		return '{}'.format(self.content)

	def get_date(self):
		return '{}'.format(self.dt_time)

	def get_user_id(self):
		return '{}'.format(self.userID)

	def get_survey_id(self):
		return '{}'.format(self.surveyID)




