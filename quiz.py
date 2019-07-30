from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Schema

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'answer_one', 'answer_two', 'answer_three', 'correct_answer')

# Init Schema
question_schema = QuestionSchema(strict=True)
questions_schema = QuestionSchema(many=True, strict=True)

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
# Run server
if __name__ == '__main__':
    app.run(debug=True)