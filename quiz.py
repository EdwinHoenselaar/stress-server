from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICSTIONS'] = False
# Init DB
db = SQLAlchemy(app)
#Init MA
ma = Marshmallow(app)

# Model
class Question(db.model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), unique=True)
    answer_one = db.Column(db.String(100))
    answer_two = db.Column(db.String(100))
    answer_three = db.Column(db.String(100))
    correct_answer = db.Column(db.Integer)

    def __init__(self, question, answer_one, answer_two, answer_three, correct_answer):
        self.question = question
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.correct_answer = correct_answer

# Schema

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'answer_one', 'answer_two', 'answer_three', 'correct_answer')

# Init Schema
question_schema = QuestionSchema(strict=True)
questions_schema = QuestionSchema(many=True, strict=True)


 
# Run server
if __name__ == '__main__':
    app.run(debug=True)