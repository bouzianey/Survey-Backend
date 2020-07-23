from flask import render_template, request, jsonify
from flask_cors import cross_origin
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
    a = InstructorObj(1)
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
    idx = request.json
    a = SurveyFillObj(idx)
    a.construct_survey()

    #return jsonify(a.get_survey_dict(3))
    return jsonify(a.get_survey_dict_plain())


@app.route('/get_survey_response', methods=['POST'])
@cross_origin()
def get_survey_response():

    return jsonify("")


@app.route('/get_survey_list', methods=['GET'])
@cross_origin()
def get_survey_list():

    a = InstructorObj(1)
    return jsonify(a.get_survey_list())


