from models import *
import pprint

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

    def __init__(self, att1):

        self.surveyID = att1
        q = db.session.query(Survey).filter(Survey.surveyID == att1).first()
        if q:
            self.surveyName = q.get_name()
            self.instructorName = q.get_instructor()
            self.questionList = []

    def construct_survey(self):

        q = db.session.query(Question).filter(Question.surveyID == self.surveyID).all()
        if q:
            for i in q:
                self.questionList.append(QuestionObj(i.get_id(), i.get_type(), i.get_repetition(), i.get_label(),
                                                     i.get_content(), i.get_survey_id()))
        return ""

    def get_survey_dict_plain(self):

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

    def get_survey_dict(self, studentid):

        x = db.session.query(User.teamID).filter(User.userID == studentid).first()
        student_list = db.session.query(User).filter(User.teamID == x[0]).filter(User.userID != studentid).all()

        survey_dict = {
            "InstructorName": self.instructorName,
            "survey_id": self.surveyID,
            "surveyName": self.surveyName,
            "studentid": studentid,
            "questionList": []
        }

        question_dict_array = []

        for i in self.questionList:

            if i.get_repetition() == "multiple":
                for exp in student_list:
                    question_dict = {
                        "id": i.get_id(),
                        "student_id": exp.get_id(),
                        "student_name": exp.get_name(),
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

            else:

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

    def get_student_survey_performance(self, studentid):

        x = db.session.query(User.teamID).filter(User.userID == studentid).first()
        student_list = db.session.query(User).filter(User.teamID == x[0]).filter(User.userID != studentid).all()

        std_list_len = 0
        for student in student_list:
            d = db.session.query(Surveyresponse).filter(Surveyresponse.surveyID == self.surveyID).\
                filter(Surveyresponse.studentID == student.userID).first()
            if d:
                std_list_len = std_list_len+1

        survey_dict = {
            "InstructorName": self.instructorName,
            "survey_id": self.surveyID,
            "surveyName": self.surveyName,
            "studentid": studentid,
            "questionAnswerList": []
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
                counter = 0
                option_dict_array = []
                for j in i.get_option_list():

                        option_dict = {
                            "label": j.get_label(),
                            "optionContent": j.get_content(),
                            "question_id": j.get_question_id()
                        }

                        if i.get_repetition() == "multiple":

                            z = db.session.query(Optionresponse).filter(Surveyresponse.surveyID == self.surveyID). \
                                filter(Questionresponse.surveyResponseID == Surveyresponse.surveyResponseID). \
                                filter(Questionresponse.student_ID == studentid).filter(
                                Questionresponse.questionID == j.get_question_id()). \
                                filter(Questionresponse.questionResponseID == Optionresponse.questionResponseID).all()

                            iterator = 0
                            student_answer_array = []

                            print("length : ", std_list_len)
                            pprint.pprint(z)
                            for exp in range(std_list_len):
                                print(exp)
                                student_answer_dict = {
                                    "student_id": z[counter+iterator].get_author_id(),
                                    "optionAnswer": z[counter+iterator].get_content(),
                                    "student_name": z[counter+iterator].get_author_name()
                                }
                                iterator = iterator + len(i.get_option_list())
                                student_answer_array.append(student_answer_dict)

                            counter = counter+1
                            option_dict.update({"studentGridAnswer": []})
                            option_dict.update({"studentGridAnswer": student_answer_array})
                        else:

                            m = db.session.query(Surveyresponse).filter(Surveyresponse.surveyID == self.surveyID).\
                                filter(Surveyresponse.studentID == studentid).first()
                            if m:
                                w = db.session.query(Optionresponse).filter(Surveyresponse.surveyResponseID == m.get_response_id()).filter(
                                    Surveyresponse.surveyResponseID == Questionresponse.surveyResponseID).filter(
                                    Questionresponse.questionID == j.get_question_id()).filter(
                                    Questionresponse.questionResponseID == Optionresponse.questionResponseID).all()
                                option_dict.update({"optionAnswer": w[counter].get_content()})
                                counter = counter + 1

                        option_dict_array.append(option_dict)

                question_dict.update({"options": []})
                question_dict.update({"options": option_dict_array})

                question_dict_array.append(question_dict)

            else:
                if i.get_repetition() == "multiple":

                    c = db.session.query(Questionresponse).filter(Questionresponse.student_ID == studentid).filter(
                        Questionresponse.questionID == i.get_id()).all()
                    student_text_answer_array = []
                    counter1 = 0

                    for exp in range(std_list_len):
                        student_answer_dict = {
                            "student_id": c[counter1].get_author_id(),
                            "optionAnswer": c[counter1].get_content(),
                            "student_name": c[counter1].get_author_name()
                        }

                        student_text_answer_array.append(student_answer_dict)
                        counter1 = counter1 + 1
                    question_dict.update({"studentTextAnswer": []})
                    question_dict.update({"studentTextAnswer": student_text_answer_array})
                else:
                    c = db.session.query(Questionresponse).filter(Questionresponse.author_id == studentid).\
                        filter(Questionresponse.questionID == i.get_id()).first()
                    if c:
                        question_dict.update({"studentTextAnswer": c.get_content()})

                question_dict_array.append(question_dict)
            survey_dict.update({"questionAnswerList": question_dict_array})

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

    def __init__(self, att1, att2, att3, att4):
        self.surveyName = att1
        self.instructorName = att2
        self.instructorID = att4
        self.questionList = att3

    def add_survey(self):
        s = Survey(instructorName=self.instructorName, name=self.surveyName, instructorID=self.instructorID)
        db.session.add(s)
        db.session.commit()
        s_id = s.get_id()
        content = self.questionList
        for i in content:
            if i["type"] == "radio":
                q = Question(label=i["label"], type=i["type"], repetition=i["repetition"], content="empty",
                             surveyID=s_id)
                db.session.add(q)
                db.session.commit()
                q_id = q.get_id()
                for j in i["options"]:
                    q = Option(label=j["label"], content=j["content"], questionID=q_id)
                    db.session.add(q)
                    db.session.commit()
            else:
                q = Question(label=i["label"], type=i["type"], repetition=i["repetition"],
                             content=i["content"], surveyID=s_id)
                db.session.add(q)
                db.session.commit()
        return ""


class InstructorObj:

    def __init__(self, att1):
        self.instructor_id = att1
        x = db.session.query(Instructor).filter(Instructor.instructorID == self.instructor_id).first()
        self.instructor_name = x.get_instructor_name()

    def create_class(self, class_name):

        c = Classtb(className=class_name, instructorID=self.instructor_id)
        db.session.add(c)
        db.session.commit()

        return ""

    def create_team(self, team_name, class_id):

        t = Team(teamName=team_name, classID=class_id)
        db.session.add(t)
        db.session.commit()

        return ""

    def get_team_students(self, team_id):
        x = db.session.query(User).filter(User.teamID == team_id).all()
        survey_dict_array = []
        if x:
            for j in x:
                survey_dict = {
                    "studentName": j.get_name(),
                    "studentID": j.get_id(),
                    "studentTeamID": j.get_team_id()
                }
                survey_dict_array.append(survey_dict)

        return survey_dict_array

    def assign_survey_class(self, team_name, class_id):

        return ""

    def invite_student(self):

        return ""

    def get_survey_list(self):
        x = db.session.query(Survey).filter(Survey.instructorID == self.instructor_id).all()
        survey_dict_array = []
        if x:
            for j in x:
                dt = j.get_date()
                chunks = dt.split('.')
                survey_dict = {
                    "name": j.get_name(),
                    "instructorName": j.get_instructor(),
                    "surveyID": j.get_id(),
                    "date": chunks[0]
                }
                survey_dict_array.append(survey_dict)

        return survey_dict_array

    def get_class_survey_list(self, class_id):

        x = db.session.query(Survey).filter(SurveyClass.classID == class_id).\
            filter(Survey.surveyID == SurveyClass.surveyID).all()
        survey_dict_array = []
        if x:
            for j in x:
                dt = j.get_date()
                chunks = dt.split('.')
                survey_dict = {
                    "surveyName": j.get_name(),
                    "surveyID": j.get_id(),
                    "date": chunks[0]
                }
                survey_dict_array.append(survey_dict)

        return survey_dict_array

    def add_new_survey(self, content):

        s = SurveyObj(content["survey"], self.instructor_name, content["questionList"], self.instructor_id)
        s.add_survey()

        return ""

    def retrieve_survey_dict(self, survey_id, student_id):

        a = SurveyFillObj(survey_id)
        a.construct_survey()

        return a.get_survey_dict(student_id)

    def modify_new_survey(self):

        return ""

    def display_student_performance(self, survey_id, student_id):

        return ""


class StudentObj:

    def __init__(self, att1):
        self.student_id = att1

    def get_student_survey_list(self):

        q = db.session.query(User).filter(User.userID == self.student_id).first()
        team_id = q.get_team_id()
        x = db.session.query(Team).filter(Team.teamID == team_id).first()
        class_id = x.get_class_id()
        z = db.session.query(SurveyClass).filter(SurveyClass.classID == class_id).all()
        survey_dict_array = []
        if z:
            for i in z:
                j = db.session.query(Survey).filter(Survey.surveyID == i.get_survey_id()).first()
                y = db.session.query(Surveyresponse).filter(Surveyresponse.surveyID == i.get_survey_id()).\
                    filter(Surveyresponse.studentID == self.student_id).first()
                if y is None:
                    dt = j.get_date()
                    chunks = dt.split('.')
                    survey_dict = {
                        "name": j.get_name(),
                        "instructorName": j.get_instructor(),
                        "surveyID": j.get_id(),
                        "date": chunks[0]
                    }
                    survey_dict_array.append(survey_dict)

        return survey_dict_array

    def save_survey_response(self, survey_response_dict):

            s = Surveyresponse(surveyName=survey_response_dict["survey"], surveyID=survey_response_dict["surveyID"],
                               studentID=survey_response_dict["studentID"])
            db.session.add(s)
            db.session.commit()
            sr_id = s.get_response_id()
            b = db.session.query(User).filter(User.userID == int(survey_response_dict["studentID"])).first()
            author_name = b.get_name()
            author_id = int(survey_response_dict["studentID"])
            content = survey_response_dict["responseList"]
            for i in content:
                if "options" in i:
                    if "studentId" in i:
                        q = Questionresponse(content="empty", surveyResponseID=sr_id,
                                             questionID=i["questionId"],
                                             type="radio", student_ID=i["studentId"], author_name=author_name,
                                               author_id=author_id)
                    else:
                        q = Questionresponse(content="empty", surveyResponseID=sr_id,
                                             questionID=i["questionId"], type="radio", student_ID=0, author_name=author_name,
                                               author_id=author_id)
                    db.session.add(q)
                    db.session.commit()
                    q_id = q.get_id()
                    for j in i["options"]:

                        if "studentId" in i:
                            q = Optionresponse(content=j["content"], questionResponseID=q_id, author_name=author_name,
                                               author_id=author_id)
                        else:
                            q = Optionresponse(content=j["content"], questionResponseID=q_id, author_name=author_name,
                                               author_id=author_id)

                        db.session.add(q)
                        db.session.commit()
                else:
                    if "studentId" in i:
                        q = Questionresponse(content=i["content"], surveyResponseID=sr_id,
                                             questionID=i["questionId"], type="text", student_ID=i["studentId"], author_name=author_name,
                                               author_id=author_id)
                    else:
                        q = Questionresponse(content=i["content"], surveyResponseID=sr_id,
                                             questionID=i["questionId"], type="text",
                                             student_ID=0, author_name=author_name,
                                               author_id=author_id)
                    db.session.add(q)
                    db.session.commit()
            return ""





