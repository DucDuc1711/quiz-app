from datetime import datetime
from typing import Any, Dict, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attempts = db.relationship('Attempt', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    time_limit = db.Column(db.Integer, nullable=False, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='quiz', lazy='select', cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_questions: bool = False, is_admin: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'time_limit': self.time_limit,
            'question_count': len(self.questions),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_questions:
            data['questions'] = [q.to_dict(is_admin=is_admin) for q in sorted(self.questions, key=lambda x: x.order_num)]
        return data

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    order_num = db.Column(db.Integer, nullable=False, default=1)

    choices = db.relationship('Choice', backref='question', lazy='select', cascade='all, delete-orphan')

    def to_dict(self, is_admin: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'content': self.content,
            'order_num': self.order_num,
            'choices': [c.to_dict(is_admin=is_admin) for c in self.choices]
        }
        if is_admin:
            data['explanation'] = self.explanation or ''
        return data

class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self, is_admin: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'question_id': self.question_id,
            'content': self.content
        }
        if is_admin:
            data['is_correct'] = self.is_correct
        return data

class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float, nullable=False, default=0.0)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    time_spent = db.Column(db.Integer, nullable=False, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    details = db.relationship('AttemptDetail', backref='attempt', lazy=True, cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'quiz_id': self.quiz_id,
            'quiz_title': self.quiz.title if self.quiz else None,
            'score': round(self.score, 2),
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'time_spent': self.time_spent,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

class AttemptDetail(db.Model):
    __tablename__ = 'attempt_details'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=True)

    question = db.relationship('Question', lazy='select')
    selected_choice = db.relationship('Choice', lazy='select')
