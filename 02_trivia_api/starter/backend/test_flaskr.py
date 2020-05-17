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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation 
    and for expected errors.
    """
    def test_get_paginated(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))



    def test_404_get_paginated_beyond_valid_page(self):
        res = self.client().get('/questions?page=50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")   

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        book = Book.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        post_data = {
            'question': 'a',
            'answer': 'a',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_create_new_question(self):
        post_data = {
            'question': 'a',
            'answer': 'a',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")  
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))    

    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/search/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 4)
    
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/search/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data["message"], "There is no questions matched")
        self.assertEqual(len(data['questions']), 0)              


    def test_404_question_search_beyond_valid_page(self):
        post_data = {
            'search': 'a',

        }
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")  
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))  

    def test_get_paginated_question_by_category(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_404_get_paginated_question_by_category_beyond_valid_page(self):
        res = self.client().get('/categories/1/questions?page=50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


     def test_post_play_quiz(self):
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
                'id': 6
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_post_play_quiz(self):
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
            }
        }x
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_post_play_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()