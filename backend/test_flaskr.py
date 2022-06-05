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
        self.database_path = 'postgresql://{}@localhost:5432/{}'.format('postgres', self.database_name)
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
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_list_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])
    
    def test_categories_not_found(self):
        res = self.client().get("/categoriesx")
        self.assertEqual(res.status_code, 404)

    def test_list_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_question_search_found(self):
        res = self.client().post("/questions/search", json={'searchTerm': 'did', 'category': None })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_delete_question(self):
        question = Question(question='what is the largest organ in the body', answer='liver', category=1, difficulty=1)
        question.insert()

        res = self.client().delete("/questions/{}".format(question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question.id)
    
    def test_delete_question_fail(self):
        res = self.client().delete("/questions/{}".format(50000000000))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        res = self.client().post("/questions", json={'question': 'Nigeria is in which continent', 'answer': 'africa', 'category': 3, 'difficulty': 1})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])

    def test_get_question_for_quiz(self):
        res = self.client().post("/quizzes", json={'quiz_category': {'type': 'science', 'id': 1}, 'previous_questions': []})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_get_question_based_on_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)
    
    def test_get_question_based_on_category_fail(self):
        res = self.client().get("/categories/500000000/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()