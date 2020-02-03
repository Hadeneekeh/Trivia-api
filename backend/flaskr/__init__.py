import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import math

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # instantiate CORS

  #add cors headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formated_categories = [category.format() for category in categories]
    return jsonify({
      'categories': formated_categories
    })


  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.all()
    formated_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formated_categories = [category.format() for category in categories]
    return jsonify({
      'questions': formated_questions[start:end],
      'total_questions': len(formated_questions),
      'current_category': None,
      'categories': formated_categories
    })


  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      Question.query.get(question_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
      return jsonify({
        'success': True
      })


  @app.route('/questions', methods=['POST'])
  def new_question():
    body = {}
    error = False
    try:
      get_input = request.get_json()

      question = get_input['question']
      category = get_input['category']
      difficulty = get_input['difficulty']
      answer = get_input['answer']

      new_question = Question(question=question, category=category, difficulty=difficulty, answer=answer)
      db.session.add(new_question)
      db.session.commit()

      body['question'] = question
      body['answer'] = answer
      body['category'] = category
      body['difficulty'] = difficulty
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort(400)
    else:
      return jsonify({
        'success': True
      })

  
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = {}
    error = False
    try:
      get_input = request.get_json()

      search_term = get_input['searchTerm']
      questions = Question.query.filter(
          Question.question.ilike("%" + search_term + "%")).all()
      formatted_questions = [question.format() for question in questions]

      body['search_term'] = search_term
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'totalQuestion': len(questions),
        'currentCategory': None
      })


  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def get_by_catgory(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in questions]
    total_questions = len(formatted_questions)
    return jsonify({
      'questions': formatted_questions,
      'totalQuestions': total_questions,
      'currentCategory': None
    })


  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    previous_question = request.get_json('previous_question')
    selected_category = request.get_json('quiz_category')

    if selected_category['id'] == None:
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=selected_category['id']).all()

    random_num = 
  # '''
  # @TODO: 
  # Create error handlers for al l expected errors 
  # including 404 and 422. 
  # '''
  
  return app

    
