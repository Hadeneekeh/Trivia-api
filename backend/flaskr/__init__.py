import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # instantiate CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # add cors headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """ Returns the categories.

        Parameters:
            None.

        Returns:
            categories: A list of categories.

        """
        categories = Category.query.all()
        formated_categories = [category.format() for category in categories]

        if len(formated_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
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

        paginated_questions = formated_questions[start:end]
        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'questions': formated_questions[start:end],
            'total_questions': len(formated_questions),
            'categories': formated_categories
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """ Returns the id of the question deleted.

        Parameters:
             question_id(int): The id of the question to be deleted

        Returns:
            deleted_id: A list of categories
            success: True

        """
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)
            else:
                question.delete()

            return jsonify({
                'success': True,
                'deleted_id': question_id
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def new_question():
        try:
            get_input = request.get_json()

            question = get_input['question']
            category = get_input['category']
            difficulty = get_input['difficulty']
            answer = get_input['answer']

            if question == '' or answer == '':
                abort(400)
            # else:
            new_question = Question(
                question=question,
                category=category,
                difficulty=difficulty,
                answer=answer)
            new_question.insert()

            return jsonify({
                'success': True,
                'message': 'Question added successfully'
            }), 201

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            get_input = request.get_json()

            search_term = get_input['searchTerm']

            questions = Question.query.filter(
                Question.question.ilike("%" + search_term + "%")).all()

            if questions is None:
                abort(400)
            formatted_questions = [question.format() for question in questions]
            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'totalQuestion': len(formatted_questions),
                'currentCategory': None
            })
        except:
            abort(404)

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_by_catgory(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        total_questions = len(formatted_questions)
        if total_questions == 0:
            abort(404)
        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': total_questions
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            previous_question = request.get_json()['previous_questions']
            selected_category = request.get_json()['quiz_category']

            if selected_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=selected_category['id']).all()

            random_num = random.randint(0, len(questions)-1)
            next_question = questions[random_num]
            select_question = False

            while select_question is False:
                if next_question.id in previous_question:
                    random_num = random.randint(0, len(questions)-1)
                    next_question = questions[random_num]
                else:
                    select_question = True
                if len(previous_question) == len(questions):
                    break

            formatted_next_question = next_question.format()
            return jsonify({
                'success': True,
                'question': formatted_next_question
            })
        except:
            abort(500)

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Item not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable request'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad request'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Server error'
        }), 500

    return app
