from flask_security.utils import hash_password,verify_password,login_user,logout_user
from flask import current_app as app, jsonify, request, render_template, send_file,send_from_directory,logging,current_app as app
from flask_security import auth_required, roles_required
from .models import *
from .sec import datastore
from flask_cors import CORS,cross_origin
from celery.result import AsyncResult
from .tasks import create_service_req_csv
import json
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from collections import Counter
import uuid
import numpy as np
##################################################################################################################################################
###############################################################       Handle 404 errors       ####################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def giving_questions_name(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    l=[]
    for i in questions:
        l.append(i.question_id)
    if l==[]:
        return 0
    return max(l)

def giving_emails():
    users = User.query.all()
    emails = []
    for i in users:
        emails.append(i.email)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('static/uploads', filename, mimetype='image/jpeg')

############################################################################################################################################################
######################################################################        USERS       ##################################################################

@app.route('/api/postUsers',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
def postUsers():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    dob_str = request.form.get('dob')
    if dob_str:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    else:
        dob = None
    qualification_image = request.files['qualification_image']
    if qualification_image and allowed_file(qualification_image.filename):
        filename = secure_filename(qualification_image.filename)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        qualification_image.save(file_path)

    if not fullname or not email or not password or not qualification_image :
        return jsonify({'success':False,'message':"All Fields are Required!"})
    user_role = datastore.find_role("user")
    new_user = User(
                        fullname = fullname,
                        email=email,
                        password=hash_password(password),   
                        dob = dob,
                        qualification = file_path,
                        fs_uniquifier = str(uuid.uuid4())
                    )
    datastore.add_role_to_user(new_user,user_role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'success':True,
        'message':'Please check you email!'
    })

@app.route('/api/getUsers',methods=['GET'])
def getUsers():
    users = Role.query.filter_by(name ="user").first()
    users = users.users
    return jsonify([{
        'user_id' : p.user_id,
        'email' : p.email,
        'password' : p.password,
        'fullname' : p.fullname,
        'qualification' : p.qualification,
        'dob' : p.dob,
    } for p in users ])

############################################################################################################################################################
######################################################################        SUBJECTS       ###############################################################

@app.route('/api/getSubjects', methods=['GET'])
def getSubjects():
    subjects = Subject.query.all()
    return jsonify([
        {
            'subject_id': p.subject_id,
            'name': p.name,
            'description': p.description,
            'chapters': [
                {
                    'chapter_id': c.chapter_id,
                    'name': c.name,
                    'description': c.description
                } for c in p.chapters
            ]
        } for p in subjects
    ])

@app.route('/api/postSubject',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def postSubject():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    new_subject = Subject(name=name,description=description)
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Subject Added Successfully!'
    })

@app.route('/api/editSubject',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def editSubject():
    data = request.json
    subject_id = data.get('id')
    edited_name = data.get('name')
    edited_description = data.get('description')
    edited_subject = Subject.query.get(subject_id)
    edited_subject.name = edited_name
    edited_subject.description = edited_description

    db.session.commit()

    return jsonify({
        'success':True,
        'message':'Subject Edited Successfully!'
    })

@app.route('/api/deleteSubject',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def deleteSubject():
    data = request.json
    id = data.get('id')
    subject_to_be_deleted = Subject.query.get(id)
    for i in subject_to_be_deleted.chapters:
        to_be_deletedChapter = Chapter.query.get(i.chapter_id)
        quiz_selected = Quiz.query.filter_by(chapter_id = to_be_deletedChapter.chapter_id).first()
        if(quiz_selected):
            return jsonify({
                'success':True,
                'message':to_be_deletedChapter.name+' chapter of the subject '+subject_to_be_deleted.name+' is in the Quiz '+str(quiz_selected.quiz_id)
            })
        db.session.delete(to_be_deletedChapter)
    db.session.delete(subject_to_be_deleted)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Subject Deleted Successfully!'
    })

############################################################################################################################################################
######################################################################        CHAPTERS       ###############################################################

@app.route('/api/getChapters',methods=['GET'])
def getChapters():
    chapters = Chapter.query.all()
    return ([
        {
            'chapter_id': c.chapter_id,
            'name': c.name,
            'description': c.description
        } for c in chapters
    ])

@app.route('/api/postChapter',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def postChapter():
    data = request.json
    subject_id = data.get('subject_id')
    name = data.get('name')
    description = data.get('description')
    new_chapter = Chapter(name=name,description=description,subject_id = subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Chapter Added Successfully!'
    })

@app.route('/api/editChapter',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def editChapter():
    data = request.json
    chapter_id = data.get('chapter_id')
    subject_id = data.get('subject_id')
    edited_name = data.get('name')
    edited_description = data.get('description')
    edited_chapter = Chapter.query.filter_by(chapter_id=chapter_id,subject_id=subject_id).first()
    edited_chapter.name = edited_name
    edited_chapter.description = edited_description

    db.session.commit()

    return jsonify({
        'success':True,
        'message':'Chapter Edited Successfully!'
    })

@app.route('/api/deleteChapter',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def deleteChapter():
    data = request.json
    id = data.get('id')
    Chapter_to_be_deleted = Chapter.query.get(id)
    count=0
    l=[]
    for i in Chapter_to_be_deleted.quizzes:
        l.append(i.quiz_id)
        count+=1
    quiz_id_str = ''
    for i in l:
        quiz_id_str+=' '+str(i)
    if count>0 :
        if count == 1:
            return jsonify({
                'success':True,
                'message':'This Chapter is in '+str(count)+' no. of quiz and their id is:'+quiz_id_str+'.'
            })
        return jsonify({
            'success':True,
            'message':'This Chapter is in '+str(count)+' number of quizzes and their id\'s are:'+quiz_id_str+'.'
        })
    db.session.delete(Chapter_to_be_deleted)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Chapter Deleted Successfully!'
    })

############################################################################################################################################################
######################################################################        QUIZZES       ###############################################################

@app.route('/api/getQuizzes',methods=['GET'])
def getQuizzes():
    quizzes = Quiz.query.all()
    return ([
        {
            'quiz_id': c.quiz_id,
            'name': c.name,
            'chapter_id': c.chapter_id,
            'date_of_quiz': c.date_of_quiz,
            'time_duration': c.time_duration,
            'remarks': c.remarks,
            'active': c.active,
            'no_of_questions': len(c.questions),
            'subject': getSubject(c.chapter_id),
            'questions': [
                {
                    'question_id': p.question_id,
                    'quiz_id': p.quiz_id,
                    'question_statement': p.question_statement,
                    'option1': p.option1,
                    'option2': p.option2,
                    'option3': p.option3,
                    'option4': p.option4,
                    'correct_option': p.correct_option
                } for p in c.questions
            ]
        } for c in quizzes
    ])

def getSubject(chapterId):
    chapter = Chapter.query.get(chapterId)
    subject = Subject.query.get(chapter.subject_id)
    return subject.name

@app.route('/api/postQuiz',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def postQuiz():
    data = request.json
    name = data.get('name')
    chapter_name = data.get('chapter_name')
    date_of_quiz = data.get('date_of_quiz')
    quiz_datetime = datetime.strptime(date_of_quiz, '%Y-%m-%dT%H:%M')
    time_duration = data.get('time_duration')
    new_quiz = Quiz(name=name,time_duration=time_duration,chapter_id = chapter_name,date_of_quiz=quiz_datetime)
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Quiz Added Successfully!'
    })

@app.route('/api/editQuiz',methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def editQuiz():
    data = request.json
    quiz_id = data.get('quiz_id')
    edited_name = data.get('name')
    edited_chapter_name = data.get('chapter_name')
    edited_time_duration = data.get('time_duration')
    edited_date_of_quiz = data.get('date_of_quiz')
    edited_quiz = Quiz.query.get(quiz_id)
    if edited_name!='':
        edited_quiz.name = edited_name
    if edited_chapter_name:
        edited_quiz.chapter_id = edited_chapter_name
    if edited_time_duration!='':
        edited_quiz.time_duration = edited_time_duration
    if edited_date_of_quiz!='':
        quiz_datetime = datetime.strptime(edited_date_of_quiz, '%Y-%m-%dT%H:%M')
        edited_quiz.date_of_quiz = quiz_datetime
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Quiz Edited Successfully!'
    })

@app.route('/api/deleteQuiz',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def deleteQuiz():
    data = request.json
    id = data.get('id')
    quiz_to_be_deleted = Quiz.query.get(id)
    for i in quiz_to_be_deleted.questions:
        to_be_deletedQuestion = Question.query.get(i.question_id)
        db.session.delete(to_be_deletedQuestion)
    db.session.delete(quiz_to_be_deleted)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Quiz Deleted Successfully!'
    })

@app.route('/api/makeActive',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def makeActive():
    data = request.json
    id = data.get('id')
    quiz = Quiz.query.get(id)
    quiz.active = True
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Quiz Active'
    })

@app.route('/api/makeInActive',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def makeInActive():
    data = request.json
    id = data.get('id')
    quiz = Quiz.query.get(id)
    quiz.active = False
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Quiz In Active'
    })

@app.route('/api/submitQuiz',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required('user')
def submitQuiz():
    data = request.json
    quiz_id = data.get('quiz_id')
    remainingTimeInSeconds = data.get('remainingTimeInSeconds')
    selectedOptions = data.get('selectedOptions')
    userEmail = data.get('userEmail')
    l=[]
    for i in selectedOptions:
        if i == 'a':
            l.append('option1')
        if i == 'b':
            l.append('option2')
        if i == 'c':
            l.append('option3')
        if i == 'd':
            l.append('option4')
    user = User.query.filter_by(email = userEmail).first()
    quiz = Quiz.query.get(int(quiz_id))
    total = len(quiz.questions)
    sum=0
    for i in range(len(quiz.questions)):
        if quiz.questions[i].correct_option == l[i]:
            sum+=1
    new_score = Score(quiz_id=int(quiz_id),total_scored=sum,user_id=user.user_id)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':"You will see Your Score in Scores Section."
    })

############################################################################################################################################################
######################################################################        QUESTIONS       ##################################################################

@app.route('/api/postQuestion', methods=["POST"])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def postQuestion():
    quiz_id = request.form.get('quiz_id')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_option = request.form.get('correct_option')
    question_statement = request.files.get('question_statement')

    file_path = None
    if question_statement and allowed_file(question_statement.filename):
        original_extension = os.path.splitext(question_statement.filename)[1]

        max_question = giving_questions_name(quiz_id)
        custom_name = f"question{max_question + 1}{original_extension}"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], custom_name)

        # Save the file
        question_statement.save(file_path)

    new_question = Question(
        question_statement=file_path,
        quiz_id=quiz_id,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Question Added Successfully!'
    })

@app.route('/api/editQuestion',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def editQuestion():
    quiz_id = request.form.get('quiz_id')
    question_id = request.form.get('question_id')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_option = request.form.get('correct_option')
    question_statement = request.files.get('question_statement')

    file_path = None
    if question_statement !='':
        if question_statement and allowed_file(question_statement.filename):
            original_extension = os.path.splitext(question_statement.filename)[1]

            max_question = giving_questions_name(quiz_id)
            custom_name = f"question{max_question + 1}{original_extension}"

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], custom_name)

            # Save the file
            question_statement.save(file_path)
    
    question = Question.query.filter_by(quiz_id=quiz_id,question_id=question_id).first()

    print(file_path)

    if option1!='':
        question.option1 = option1
        
    if option2!='':
        question.option2 = option2
        
    if option3!='':
        question.option3 = option3
        
    if option4!='':
        question.option4 = option4
        
    if correct_option!='':
        question.correct_option = correct_option
    
    if file_path:
        question.question_statement = file_path

    db.session.commit()

    return jsonify({
        'success':True,
        'message':'Question Edited Successfully!'
    })

@app.route('/api/deleteQuestion',methods=['POST'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("admin")
def deleteQuestion():
    data = request.json
    id = data.get('id')
    Question_to_be_deleted = Question.query.get(id)
    
    db.session.delete(Question_to_be_deleted)
    db.session.commit()
    return jsonify({
        'success':True,
        'message':'Question Deleted Successfully!'
    })

@app.route('/api/getQuizQuestions/<int:quiz_id>', methods=['GET'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("user")
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    questions_data = [
        {
            "question_id": q.question_id,
            "statement": q.question_statement,
            "options": [q.option1, q.option2, q.option3, q.option4],
            "correct_option": q.correct_option,
        }
        for q in questions
    ]
    return jsonify({
        "success": True,
        "quiz_id": quiz_id,
        "quiz_name": quiz.name,
        "date_of_quiz": quiz.date_of_quiz,
        "time_duration": quiz.time_duration,
        "questions": questions_data,
    })


############################################################################################################################################################
######################################################################        SCORES       ##################################################################
@app.route('/api/getScores/<string:userEmail>', methods=['GET'])
@cross_origin(origins=["http://localhost:5173"])
@auth_required('token')
@roles_required("user")
def getScores(userEmail):
    user = User.query.filter_by(email=userEmail).first()
    scores = Score.query.filter_by(user_id=user.user_id).all()
    return ([
        {
            'id': c.score_id,
            'numQuestions': find_numQuestions(c.quiz_id),
            'date': c.time_stamp_of_attempt,
            'score': giveScoresFraction(c.total_scored,c.quiz_id)
        } for c in scores
    ])

def giveScoresFraction(score,quizId):
    quiz = Quiz.query.get(quizId)
    count = len(quiz.questions)
    score_str=str(score)+'/'+str(count)
    return score_str

def find_numQuestions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    count = len(quiz.questions)
    return count

############################################################################################################################################################
######################################################################        ADMIN       ##################################################################

@app.route("/api/authenticate",methods = ["GET","POST"])
def login_func():
    credentials = request.get_json()
    user = datastore.find_user(email = credentials.get("email"))
    if user and verify_password(credentials.get("password"),user.password):
        login_user(user)
        if user.has_role("admin"):
            return jsonify({"role": "admin","token": user.get_auth_token(), "user_id": user.user_id}),200
        elif user.has_role("user"):
            return jsonify({"role": "user","token": user.get_auth_token(), "user_id": user.user_id}),200
    return jsonify({"message": "Invalid Credentials"}),404

@app.route("/api/logout")
def l():
    logout_user()
    return jsonify({"message" : "Successfully Logged out!!","success": True}),200

