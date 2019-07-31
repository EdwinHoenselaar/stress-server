from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Initialize app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init DB
db = SQLAlchemy(app)
# Init MA
ma = Marshmallow(app)

# Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    answer_one = db.Column(db.String(100))
    answer_two = db.Column(db.String(100))
    answer_three = db.Column(db.String(100))
    correct_answer = db.Column(db.String(100))

    def __init__(self, question, answer_one, answer_two, answer_three, correct_answer):
        self.question = question
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.correct_answer = correct_answer

# Setting up schemas
class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'answer_one', 'answer_two', 'answer_three', 'correct_answer')

class QuestionWithoutAnswerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'answer_one', 'answer_two', 'answer_three')

class AnswerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'correct_answer')

# Init Schemas
question_schema = QuestionSchema(strict=True)
questions_schema = QuestionSchema(many=True, strict=True)
question_without_answer_schema = QuestionWithoutAnswerSchema(strict=True)
answer_schema = AnswerSchema(strict=True)

# Routes
# Create question
@app.route('/question', methods=['POST'])
def add_question():
    question = request.json['question']
    answer_one = request.json['answer_one']
    answer_two = request.json['answer_two']
    answer_three = request.json['answer_three']
    correct_answer = request.json['correct_answer']

    new_question = Question(question, answer_one, answer_two, answer_three, correct_answer)
 
    db.session.add(new_question)
    db.session.commit()

    return question_schema.jsonify(new_question)

# Get all questions
@app.route('/question', methods=['GET'])
def get_questions():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)
    return jsonify(result.data)

# Get a random question
@app.route('/question/random', methods=['GET'])
def get_random_question():
    random_question = Question.query.with_entities(Question.question, Question.answer_one, Question.answer_two, Question.answer_three, Question.id).order_by(func.random()).limit(1).one()
    result = question_without_answer_schema.dump(random_question)
    return jsonify(result.data)

# Get one answer
@app.route('/answer/<id>', methods=['GET'])
def get_answer(id):
    answer = Question.query.get(id)
    result = answer_schema.dump(answer)
    return jsonify(result.data)

# Get one single question
@app.route('/question/<id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)
    result = question_schema.dump(question)
    return jsonify(result.data)

# Update question
@app.route('/question/<id>', methods=['PUT'])
def update_question(id):
    put_question = Question.query.get(id)

    question = request.json['question']
    answer_one = request.json['answer_one']
    answer_two = request.json['answer_two']
    answer_three = request.json['answer_three']
    correct_answer = request.json['correct_answer']

    put_question.question = question
    put_question.answer_one = answer_one
    put_question.answer_two = answer_two
    put_question.answer_three = answer_three
    put_question.correct_answer = correct_answer

    db.session.commit()

    return question_schema.jsonify(put_question)

# Delete question
@app.route('/question/<id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    return question_schema.jsonify(question)

# /End of routes



# Run server
if __name__ == '__main__':
    app.run(debug=True)