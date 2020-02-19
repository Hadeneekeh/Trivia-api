import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:psql@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # """
    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    # """

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=1900')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Item not found')

    def test_delete_question(self):
        response = self.client().delete('/questions/9')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_not_found_delete_question(self):
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable request')

    def test_add_question(self):
        response= self.client().post('/questions', json={'question': 'Who be my husband?', 'answer': 'Ayiki', 'category': '3', 'difficulty': '3'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['message'])

    def test_unprocessed_add_question(self):
        response= self.client().post('/questions', json={'answer': 'Kafee ni', 'category': '3', 'difficulty': '3'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertTrue(data['error'])
        self.assertEqual(data['message'], 'Unprocessable request')
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        response= self.client().post('/questions/search', json={'searchTerm': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(data['success'], True)
    
    def test_search_question_not_found(self):
        response= self.client().post('/questions/search', json={'searchTerm': 'rthyu'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Item not found')

    def test_search_question_not_found(self):
        response= self.client().post('/questions/search', json={'searchTerm': 'rthyu'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Item not found')

    def test_get_question_by_category(self):
        response = self.client().get('/categories/4/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['questions'])

    def test_get_question_by_category_not_found(self):
        response = self.client().get('/categories/74/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Item not found')

    def test_play_quiz(self):
        req = {
            'previous_questions': [],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
        response = self.client().post('/quizzes', json=req)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_error_play_quiz(self):
        req = {
            'previous_questions': [],
            'quizz_category': {
                'ids': 1,
                'types': 'Science'
            }
        }
        response = self.client().post('/quizzes', json=req)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Server error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()