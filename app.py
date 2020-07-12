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
    #pprint.pprint(content)
    #s = SurveyObj(content["survey"], content["instructor"], content["questionList"])
    #s.add_survey()

    a = SurveyFillObj(3, "CSC330", "Dr.Imad")
    a.construct_survey()
    #for i in a.get_question_list():
     #   if i.get_type() == "radio":
      #      for j in i.get_option_list():
       #         print("radio :  ", j.get_content(), "label :", j.get_label())

        #else:
         #   print("text :  ", i.get_content(), "label :", i.get_label())
    #pprint.pprint(a.get_survey_dict())

    return jsonify(a.get_survey_dict())




