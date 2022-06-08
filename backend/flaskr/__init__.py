import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from sqlalchemy import false

from models import setup_db, Question, Category
from helpers import get_paginated_data

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs [PROBABLY DONE]
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow  [DONE]
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories. [DONE]
    """

    @app.route("/categories")
    def list_categories():
        categories = Category.query.all()
        formatted_categories = {}

        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. [DONE]

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def list_questions():
        questions = Question.query.all()
        paginated_questions, total_questions = get_paginated_data(request, questions, Question)

        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'questions': paginated_questions,
            'categories': list_categories().get_json()['categories'],
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID. [DONE]

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if not question:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score. [DONE]

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
                'question': question.question,
                'answer': question.answer,
                'category': question.category,
                'difficulty': question.difficulty
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question. [DONE]

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', "")
        current_category = body.get('category', None)

        questions = []
        if current_category:
            questions = Question.query.filter(Question.question.ilike('%' + search_term + '%'), Question.category == current_category).all()
            
        else:
            questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()

        paginated_questions, total_questions = get_paginated_data(request, questions, Question)

        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'questions': paginated_questions,
            'current_category': current_category
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):

        # check if category exists
        category = Category.query.get(category_id)
        if not category:
            abort(404)
        else:
            questions = Question.query.filter_by(category=category_id)
            paginated_questions, total_questions = get_paginated_data(request, questions, Question)
            
            return jsonify({
                'success': True,
                'total_questions': total_questions,
                'questions': paginated_questions,
                'current_category': category_id
            })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        body = request.get_json()
        print(body)
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', {}) 
        category_id = quiz_category.get('id')

        questions = []
        if category_id:
            questions = Question.query.filter_by(category=category_id).all()
        else:
            questions = Question.query.all()
        
        questions = [Question.format(question) for question in questions]

        def not_in_previous(question):
            for item in previous_questions:
                if(question['id'] == item):
                    return False
            return True

        questions_for_quiz = list(filter(not_in_previous, questions))
        random_question = None
        if (len(questions_for_quiz) > 0):
            random_question = random.choice(questions_for_quiz)

        return jsonify({
            'success': True,
            'question': random_question
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app

