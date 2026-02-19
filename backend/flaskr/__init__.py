from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """Helper function to paginate questions.

    Takes the request (to read the 'page' query param) and a list of
    Question model objects. Returns a list of formatted question dicts
    for the requested page.
    """
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # Set up CORS — allows all origins by default.
    # In production you'd restrict this to your frontend's domain.
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        """Set Access-Control-Allow headers on every response."""
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )
        return response

    # ------------------------------------------------------------------
    # GET /categories
    # Returns all categories as { id: type } dict
    # ------------------------------------------------------------------
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {
                category.id: category.type for category in categories
            }
        })

    # ------------------------------------------------------------------
    # GET /questions?page=<int>
    # Returns paginated questions, total count, categories, and
    # current_category.
    # ------------------------------------------------------------------
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {
                category.id: category.type for category in categories
            },
            'current_category': None
        })

    # ------------------------------------------------------------------
    # DELETE /questions/<int:question_id>
    # Deletes the question with the given ID.
    # ------------------------------------------------------------------
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = db.session.get(Question, question_id)

        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            db.session.rollback()
            abort(422)

    # ------------------------------------------------------------------
    # POST /questions
    # Two purposes:
    #   1. If request body contains 'searchTerm', search questions.
    #   2. Otherwise, create a new question.
    # ------------------------------------------------------------------
    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        if body is None:
            abort(400)

        search_term = body.get('searchTerm', None)

        if search_term is not None:
            # --- SEARCH ---
            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).all()

            return jsonify({
                'success': True,
                'questions': [q.format() for q in selection],
                'total_questions': len(selection),
                'current_category': None
            })

        # --- CREATE ---
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        if not all([question, answer, difficulty, category]):
            abort(400)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category
            )
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })
        except Exception:
            db.session.rollback()
            abort(422)

    # ------------------------------------------------------------------
    # GET /categories/<category_id>/questions
    # Returns questions for a specific category.
    # ------------------------------------------------------------------
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(
            Question.category == str(category_id)
        ).order_by(Question.id).all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': [q.format() for q in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })

    # ------------------------------------------------------------------
    # POST /quizzes
    # Returns a random question for the quiz, excluding previously
    # asked questions.
    # ------------------------------------------------------------------
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        if body is None:
            abort(400)

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category is None:
            abort(400)

        # id of 0 means "All" categories
        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == str(quiz_category['id'])
            ).all()

        # Filter out previously asked questions
        remaining = [q for q in questions if q.id not in previous_questions]

        question = random.choice(remaining) if remaining else None

        return jsonify({
            'success': True,
            'question': question.format() if question else None
        })

    # ------------------------------------------------------------------
    # Error handlers
    # ------------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
