import os
import unittest

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = os.getenv("POSTGRES_PWD", "password")
        self.database_host = "localhost:5432"
        self.database_path = (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}/{self.database_name}"
        )

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Seed test data
        with self.app.app_context():
            db.create_all()
            # Add a category and a question for tests to use
            if Category.query.count() == 0:
                cat = Category(type='Science')
                db.session.add(cat)
                db.session.commit()
            if Question.query.count() == 0:
                q = Question(
                    question='What is the chemical symbol for water?',
                    answer='H2O',
                    difficulty=1,
                    category='1'
                )
                db.session.add(q)
                db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ------------------------------------------------------------------
    # GET /categories
    # ------------------------------------------------------------------
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertGreater(len(data['categories']), 0)

    def test_404_get_categories_when_none_exist(self):
        with self.app.app_context():
            Category.query.delete()
            db.session.commit()

        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ------------------------------------------------------------------
    # GET /questions
    # ------------------------------------------------------------------
    def test_get_paginated_questions(self):
        res = self.client.get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)

    def test_404_requesting_beyond_valid_page(self):
        res = self.client.get('/questions?page=1000')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ------------------------------------------------------------------
    # DELETE /questions/<id>
    # ------------------------------------------------------------------
    def test_delete_question(self):
        # First, get an existing question id
        with self.app.app_context():
            question = Question.query.first()
            question_id = question.id

        res = self.client.delete(f'/questions/{question_id}')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    def test_404_delete_nonexistent_question(self):
        res = self.client.delete('/questions/99999')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # ------------------------------------------------------------------
    # POST /questions (create)
    # ------------------------------------------------------------------
    def test_create_question(self):
        new_question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'difficulty': 1,
            'category': '1'
        }
        res = self.client.post('/questions', json=new_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('created', data)

    def test_400_create_question_missing_fields(self):
        bad_question = {
            'question': 'Incomplete question'
            # missing answer, difficulty, category
        }
        res = self.client.post('/questions', json=bad_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # ------------------------------------------------------------------
    # POST /questions (search)
    # ------------------------------------------------------------------
    def test_search_questions(self):
        res = self.client.post('/questions', json={'searchTerm': 'water'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertGreater(len(data['questions']), 0)

    def test_search_questions_no_results(self):
        res = self.client.post(
            '/questions', json={'searchTerm': 'xyznonexistent'}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)

    # ------------------------------------------------------------------
    # GET /categories/<id>/questions
    # ------------------------------------------------------------------
    def test_get_questions_by_category(self):
        res = self.client.get('/categories/1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertGreater(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 1)

    def test_404_get_questions_by_nonexistent_category(self):
        res = self.client.get('/categories/9999/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # ------------------------------------------------------------------
    # POST /quizzes
    # ------------------------------------------------------------------
    def test_play_quiz(self):
        res = self.client.post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'type': 'Science', 'id': 1}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_play_quiz_all_categories(self):
        res = self.client.post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'type': 'click', 'id': 0}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_400_play_quiz_missing_category(self):
        res = self.client.post('/quizzes', json={
            'previous_questions': []
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
