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

    @app.route("/questions/search", methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', "")
        current_category = body.get('category', None)

        if not search_term:
            abort(400)

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


    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        body = request.get_json()
        print(body)
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', {}) 
        category_id = quiz_category.get('id')

        if previous_questions == None:
            abort(400)

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

    @app.route("/categories", methods=["POST"])
    def create_category():
        body = request.get_json()
        category = body.get('type')

        if not category:
            abort(400)

        category = Category(type=category)
        category.insert()

        return jsonify({
            'success': True,
            'created': category.id,
            'categories': list_categories().get_json()['categories'],
        })

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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app

