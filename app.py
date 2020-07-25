from flask import render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import UserMixin
import pprint
from surveyManager import *
from init import app


@app.route('/', methods=['GET', 'POST'])
def my_index():

    return render_template("index.html", token=" Yacine Bouziane")


@app.route('/api_post', methods=['POST'])
@cross_origin()
def my_api_post():
    content = request.json
    idx = int(content["id"])
    a = InstructorObj(idx)
    a.add_new_survey(content)
    #pprint.pprint(content)
    #s = SurveyObj(content["survey"], content["instructor"], content["questionList"])
    #s.add_survey()

    #a = SurveyFillObj(3)
    #a.construct_survey()
    return ""


@app.route('/get_api', methods=['POST'])
@cross_origin()
def get_api():
    st = request.json
    idx = int(st)
    a = SurveyFillObj(idx)
    a.construct_survey()

    #return jsonify(a.get_survey_dict(3))
    return jsonify(a.get_survey_dict_plain())


@app.route('/get_survey_response', methods=['POST'])
@cross_origin()
def get_survey_response():

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
    content = request.json
    pprint.pprint(content)
    q = db.session.query(Instructor).filter(Instructor.email == content["email"]).first()
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

    return data


@app.route('/signup_instructor', methods=['GET', 'POST'])
@cross_origin()
def signup_instructor():
    content = request.json
    pprint.pprint(content)
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

    return data


@app.route('/logout_instructor')
def logout_instructor():
    return ""