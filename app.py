from flask import render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import UserMixin
import pprint, string, random
from surveyManager import *
from init import app
from email_gen import send_email
from email_gen import notify_student
from config import ADMINS


@app.route('/', methods=['GET', 'POST'])
def my_index():

    return render_template("index.html", token="OWL")


@app.route('/add_student_post', methods=['POST'])
@cross_origin()
def add_student_post():

    result = "success"
    content = request.json
    q = db.session.query(User).filter(User.userName == content["studentName"]).filter(User.email == content["studentEmail"]).first()

    if q is None:

        #generate a random password for student
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = []

        for x in range(9):
            password.append(random.choice(password_characters))

        pwd = "".join(password)
        idx = content["team_id"]

        s = User(teamID=idx, userName=content["studentName"], email=content["studentEmail"], password=pwd)
        db.session.add(s)
        db.session.commit()
        recipient = []
        recipient = [content["studentEmail"]]
        send_email(ADMINS[0], recipient, content["studentName"], content["studentEmail"], pwd)
    else:
        result = "failed"

    return jsonify(result)


@app.route('/notify_student_missed_surveys', methods=['POST'])
@cross_origin()
def notify_student_missed_surveys():

    content = request.json
    student_id = int(content["studentID"])
    q = db.session.query(User).filter(User.userID == student_id).first()
    recipient = [q.get_email()]
    notify_student(ADMINS[0], recipient, content["studentName"], content["surveyList"])
    return jsonify("")


@app.route('/get_instructor_feedback_list', methods=['POST'])
@cross_origin()
def get_instructor_feedback_list():

    content = request.json
    student_id = int(content["studentID"])

    res_dict = {
        "result": "success"
    }
    q = db.session.query(ProFeedback).filter(ProFeedback.userID == student_id).all()
    if q:
        dict_array = []
        for i in q:
            dt = i.get_date()
            chunks = dt.split('.')
            data = {
                "surveyName": i.get_survey_name(),
                "date": chunks[0],
                "content": i.get_content()
            }
            dict_array.append(data)
        res_dict.update({"feedbackList": []})
        res_dict.update({"feedbackList": dict_array})
    else:
        res_dict.update({"result": "failed"})

    return jsonify(res_dict)


@app.route('/post_instructor_feedback', methods=['POST'])
@cross_origin()
def post_instructor_feedback():

    result = "success"
    content = request.json
    student_id = int(content["studentID"])
    survey_id = int(content["surveyID"])
    q = db.session.query(ProFeedback).filter(ProFeedback.userID == student_id).\
        filter(ProFeedback.surveyID == survey_id).first()

    if q is None:
        j = db.session.query(Survey).filter(Survey.surveyID == survey_id).first()
        s = ProFeedback(surveyName=j.get_name(), userID=student_id,
                        surveyID=survey_id, content=content["feedback_comment"])
        db.session.add(s)
        db.session.commit()
    else:
        result = "failed"

    return jsonify(result)


@app.route('/get_student_contribution', methods=['POST'])
@cross_origin()
def get_student_contribution():

    content = request.json
    idx = int(content["teamID"])

    q = db.session.query(User).filter(User.teamID == idx).all()
    q1 = db.session.query(Survey).filter(Survey.surveyID == SurveyClass.surveyID).\
        filter(SurveyClass.classID == Team.classID).filter(Team.teamID == idx).all()
    res_dict = {
        "result": "success",
        "surveyTotal": len(q1)
    }
    if q and q1:

        dict_array = []
        for x in q:
            score = 0
            missed_survey = []
            for z in q1:
                q2 = db.session.query(Surveyresponse).filter(Surveyresponse.studentID == x.get_id()).\
                    filter(Surveyresponse.surveyID == z.get_id()).first()
                if q2:
                    score = score + 1
                else:
                    missed_survey.append(z.get_name())
            data = {
                "studentID": x.get_id(),
                "studentName": x.get_name(),
                "score": score,
                "missed_survey": missed_survey
            }
            dict_array.append(data)
        res_dict.update({"studentContributionList": []})
        res_dict.update({"studentContributionList": dict_array})
    else:
        res_dict.update({"result": "failed"})

    return jsonify(res_dict)


@app.route('/add_class_post', methods=['POST'])
@cross_origin()
def add_class_post():

    result = "success"
    content = request.json
    q = db.session.query(Classtb).filter(Classtb.className == content["className"]).first()
    if q is None:
        idx = content["id"]
        s = Classtb(instructorID=idx, className=content["className"])
        db.session.add(s)
        db.session.commit()
    else:
        result = "failed"
    return jsonify(result)


@app.route('/add_team_post', methods=['POST'])
@cross_origin()
def add_team_post():

    result = "success"
    content = request.json
    q = db.session.query(Team).filter(Team.teamName == content["teamName"]).first()
    if q is None:
        idx = content["id"]
        s = Team(classID=idx, teamName=content["teamName"])
        db.session.add(s)
        db.session.commit()
    else:
        result = "failed"
    print(result)
    return jsonify(result)


@app.route('/get_team_list', methods=['POST'])
@cross_origin()
def get_team_list():

    content = request.json
    idx = int(content["id"])

    res_dict = {
        "result": "success"
    }
    q = db.session.query(Team).filter(Team.classID == idx).all()
    if q:

        dict_array = []
        for x in q:
            data = {
                "teamName": x.get_team_name(),
                "teamID": x.get_id()
            }
            dict_array.append(data)
        res_dict.update({"teamList": []})
        res_dict.update({"teamList": dict_array})
    else:
        res_dict.update({"result": "failed"})

    return jsonify(res_dict)


@app.route('/get_class_list', methods=['POST'])
@cross_origin()
def get_class_list():
    content = request.json
    idx = int(content["id"])

    res_dict = {
        "result": "success"
    }
    q = db.session.query(Classtb).filter(Classtb.instructorID == idx).all()
    if q:

        dict_array = []
        for x in q:
            data = {
                "className": x.get_class_name(),
                "classID": x.get_id()
            }
            dict_array.append(data)
        res_dict.update({"classList": []})
        res_dict.update({"classList": dict_array})
    else:
        res_dict.update({"result": "failed"})

    return jsonify(res_dict)


@app.route('/get_team_student_list', methods=['POST'])
@cross_origin()
def get_team_student_list():
    content = request.json
    user_id = int(content["user_id"])
    team_id = content["team_id"]
    a = InstructorObj(user_id)
    res_dict = {
        "result": "success"
    }
    res_dict.update({"studentList": []})
    res_dict.update({"studentList": a.get_team_students(team_id)})

    return jsonify(res_dict)


@app.route('/add_survey_api', methods=['POST'])
@cross_origin()
def add_survey_api():
    content = request.json
    idx = int(content["id"])
    a = InstructorObj(idx)
    a.add_new_survey(content)

    return ""


@app.route('/set_survey_to_class', methods=['POST'])
@cross_origin()
def set_survey_to_class():

    obj = request.json
    class_id = int(obj["classID"])
    survey_id = int(obj["surveyID"])
    result = "success"
    q = db.session.query(SurveyClass).filter(SurveyClass.classID == class_id).filter(SurveyClass.surveyID == survey_id).first()
    if q is None:
        c = SurveyClass(classID=class_id, surveyID=survey_id)
        db.session.add(c)
        db.session.commit()
    else:
        result = "failed"

    return jsonify(result)


@app.route('/get_class_survey_list', methods=['POST'])
@cross_origin()
def get_class_survey_list():
    obj = request.json
    user_id = int(obj["user_id"])
    class_id = int(obj["class_id"])
    a = InstructorObj(user_id)

    res_dict = {
        "result": "success"
    }
    res_dict.update({"surveyList": []})
    res_dict.update({"surveyList": a.get_class_survey_list(class_id)})

    return jsonify(res_dict)


@app.route('/get_student_survey_list', methods=['POST'])
@cross_origin()
def get_student_survey_list():
    obj = request.json
    idx = int(obj["id"])
    a = StudentObj(idx)

    return jsonify(a.get_student_survey_list())


@app.route('/get_student_survey', methods=['POST'])
@cross_origin()
def get_student_survey():
    obj = request.json
    idx = int(obj["survey_id"])
    a = SurveyFillObj(idx)
    a.construct_survey()

    return jsonify(a.get_survey_dict(obj["id"]))


@app.route('/get_student_survey_performance', methods=['POST'])
@cross_origin()
def get_student_survey_performance():

    obj = request.json
    survey_id = int(obj["survey_id"])
    student_id = int(obj["student_id"])
    a = SurveyFillObj(survey_id)
    a.construct_survey()
    j = a.get_student_survey_performance(student_id)

    return jsonify(j)


@app.route('/get_api', methods=['POST'])
@cross_origin()
def get_api():
    st = request.json
    idx = int(st)
    a = SurveyFillObj(idx)
    a.construct_survey()

    return jsonify(a.get_survey_dict_plain())


@app.route('/post_survey_response', methods=['POST'])
@cross_origin()
def post_survey_response():

    content = request.json
    o = StudentObj(content["studentID"])
    o.save_survey_response(content)

    return jsonify("")


@app.route('/get_survey_list', methods=['POST'])
@cross_origin()
def get_survey_list():

    st = request.json
    idx = int(st)
    a = InstructorObj(idx)
    return jsonify(a.get_survey_list())


@app.route('/login_instructor', methods=['POST'])
@cross_origin()
def login_instructor():
    email = "boho@gmail.com"
    password = "123456"

    print("get data =======")
    print(request.get_data())
    print("data ===========")
    print(request.data)
    print("Json ===========")
    print(request.json)
    print("Get Json ===========")
    print(request.get_json())
    print("form Items ===========")
    print(request.form.items())

    q = db.session.query(Instructor).filter(Instructor.email == email).filter(Instructor.password == password).first()
    if q:
        data = {
            "logged_in": True,
            "user": {
                "email": q.get_email(),
                "id": q.get_id(),
                "password": ""
            }
        }
    else:
        data = {
            "logged_in": False,
            "user": {}
        }

    return jsonify(data)


@app.route('/login_student', methods=['POST'])
@cross_origin()
def login_student():

    content = request.json
    q = db.session.query(User).filter(User.email == content["email"]).filter(User.password == content["password"]).first()
    if q:
        data = {
            "logged_in": True,
            "user": {
                "email": q.get_email(),
                "id": q.get_id(),
                "password": ""
            }
        }
    else:
        data = {
            "logged_in": False,
            "user": {}
        }

    return jsonify(data)


@app.route('/signup_instructor', methods=['GET', 'POST'])
@cross_origin()
def signup_instructor():

    content = request.json
    q = db.session.query(Instructor).filter(Instructor.email == content["email"]).first()

    if q is None:

        flName = content["firstName"] + " " + content["lastName"]
        s = Instructor(instructorName=flName, email=content["email"], password=content["password"])
        db.session.add(s)
        db.session.commit()

        x = db.session.query(Instructor).filter(Instructor.email == content["email"]).first()

        data = {
            "logged_in": True,
            "user": {
                "email": x.get_email(),
                "id": x.get_id(),
                "password": ""
            }
        }
    else:
        data = {
            "logged_in": True,
            "user": {
                "email": q.get_email(),
                "id": q.get_id(),
                "password": ""
            }
        }

    return jsonify(data)


@app.route('/logout_instructor')
def logout_instructor():

    return ""
