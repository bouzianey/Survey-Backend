from models import *


class OptionObj:

    def __init__(self, att1, att2, att3, att4):
        self.id = att1
        self.content = att2
        self.label = att3
        self.questionID = att4

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_content(self):
        return self.content

    def get_question_id(self):
        return self.questionID


class QuestionObj:

    def __init__(self, att1, att2, att3, att4, att5, att6):
        self.id = att1
        self.type = att2
        self.repetition = att3
        self.label = att4
        self.content = att5
        self.surveyID = att6
        self.optionsList = []

        if self.type == "radio":
            q = db.session.query(Option).filter(Option.questionID == self.id).all()
            if q:
                for i in q:
                    self.optionsList.append(OptionObj(i.get_id(), i.get_content(), i.get_label(), i.get_question_id()))

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_repetition(self):
        return self.repetition

    def get_label(self):
        return self.label

    def get_content(self):
        return self.content

    def get_survey_id(self):
        return self.surveyID

    def get_option_list(self):
        return self.optionsList


class SurveyFillObj:

    def __init__(self, att1, att2, att3):
        self.surveyID = att1
        self.surveyName = att2
        self.instructorName = att3
        self.questionList = []

    def construct_survey(self):

        q = db.session.query(Question).filter(Question.surveyID == self.surveyID).all()
        if q:
            for i in q:
                self.questionList.append(QuestionObj(i.get_id(), i.get_type(), i.get_repetition(), i.get_label(),
                                                     i.get_content(), i.get_survey_id()))
        return ""

    def get_survey_dict(self):

        survey_dict = {
            "InstructorName": self.instructorName,
            "survey_id": self.surveyID,
            "surveyName": self.surveyName,
            "questionList": []
        }

        question_dict_array = []

        for i in self.questionList:

            question_dict = {
                "id": i.get_id(),
                "type": i.get_type(),
                "repetition": i.get_repetition(),
                "label": i.get_label(),
                "content": i.get_content(),
                "survey_id": i.get_survey_id(),
            }
            if i.get_type() == "radio":

                option_dict_array = []

                for j in i.get_option_list():

                    option_dict = {
                        "label": j.get_label(),
                        "content": j.get_content(),
                        "question_id": j.get_question_id()
                    }
                    option_dict_array.append(option_dict)
                question_dict.update({"options": []})
                question_dict.update({"options": option_dict_array})

            question_dict_array.append(question_dict)

        survey_dict.update({"questionList": question_dict_array})

        return survey_dict

    def get_question_list(self):
        return self.questionList

    def get_survey_id(self):
        return self.surveyID

    def get_survey_name(self):
        return self.surveyName

    def get_instructor_name(self):
        return self.instructorName


class SurveyObj:

    def __init__(self, att1, att2, att3):
        self.surveyName = att1
        self.InstructorName = att2
        self.questionList = att3

    def add_survey(self):
        s = Survey(instructorName=self.InstructorName, name=self.surveyName)
        db.session.add(s)
        db.session.commit()
        s_id = s.get_id()
        content = self.questionList
        for i in content:
            if i["type"] == "radio":
                q = Question(label=i["label"], type=i["type"], repetition=i["Repetition"], content="empty",
                             surveyID=s_id)
                db.session.add(q)
                db.session.commit()
                q_id = q.get_id()
                for j in i["options"]:
                    q = Option(label=j["label"], content=j["content"], questionID=q_id)
                    db.session.add(q)
                    db.session.commit()
            else:
                q = Question(label=i["label"], type=i["type"], repetition=i["Repetition"],
                             content=i["content"], surveyID=s_id)
                db.session.add(q)
                db.session.commit()
        return ""






