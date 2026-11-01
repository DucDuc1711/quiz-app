from typing import Any, Dict, List, Tuple
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Quiz, Question, Choice, Attempt, AttemptDetail, User
from app.routes import quiz_bp
from app.utils import error_response

@quiz_bp.route('/quizzes', methods=['GET'])
def get_quizzes() -> Tuple[Any, int]:
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return jsonify({'quizzes': [q.to_dict(include_questions=False, is_admin=False) for q in quizzes]}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return error_response('Không tìm thấy bộ quiz này', 404)
    return jsonify({'quiz': quiz.to_dict(include_questions=True, is_admin=False)}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id: int) -> Tuple[Any, int]:
    user_id = int(get_jwt_identity())
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return error_response('Không tìm thấy bộ quiz này', 404)

    data = request.get_json() or {}
    answers: List[Dict[str, Any]] = data.get('answers', [])
    time_spent: int = int(data.get('time_spent', 0))

    user_answers_map = {ans.get('question_id'): ans.get('choice_id') for ans in answers if ans.get('question_id')}
    total_questions = len(quiz.questions)
    if total_questions == 0:
        return error_response('Bộ quiz chưa có câu hỏi nào', 400)

    correct_answers = 0
    details_to_save = []
    question_reviews = []

    for q in quiz.questions:
        sel_id = user_answers_map.get(q.id)
        c_choice = Choice.query.filter_by(question_id=q.id, is_correct=True).first()
        c_id = c_choice.id if c_choice else None
        is_correct = (sel_id is not None and c_id is not None and sel_id == c_id)
        if is_correct:
            correct_answers += 1

        details_to_save.append({'question_id': q.id, 'selected_choice_id': sel_id})
        question_reviews.append({
            'question_id': q.id, 'content': q.content, 'explanation': q.explanation or '',
            'order_num': q.order_num, 'selected_choice_id': sel_id, 'correct_choice_id': c_id,
            'is_correct': is_correct,
            'choices': [{'id': c.id, 'content': c.content, 'is_correct': c.is_correct} for c in q.choices]
        })

    score = round((correct_answers / total_questions) * 10, 2)
    attempt = Attempt(
        user_id=user_id, quiz_id=quiz_id, score=score,
        total_questions=total_questions, correct_answers=correct_answers, time_spent=time_spent
    )
    db.session.add(attempt)
    db.session.flush()

    for item in details_to_save:
        db.session.add(AttemptDetail(attempt_id=attempt.id, question_id=item['question_id'], selected_choice_id=item['selected_choice_id']))
    db.session.commit()

    return jsonify({'message': 'Nộp bài thành công', 'attempt': attempt.to_dict(), 'question_reviews': sorted(question_reviews, key=lambda x: x['order_num'])}), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/leaderboard', methods=['GET'])
def get_leaderboard(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return error_response('Không tìm thấy bộ quiz này', 404)
    attempts = Attempt.query.filter_by(quiz_id=quiz_id).order_by(Attempt.score.desc(), Attempt.time_spent.asc(), Attempt.submitted_at.asc()).limit(10).all()
    leaderboard = [dict(att.to_dict(), rank=r) for r, att in enumerate(attempts, 1)]
    return jsonify({'quiz_id': quiz.id, 'quiz_title': quiz.title, 'leaderboard': leaderboard}), 200

@quiz_bp.route('/me/attempts', methods=['GET'])
@jwt_required()
def get_my_attempts() -> Tuple[Any, int]:
    user_id = int(get_jwt_identity())
    attempts = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.submitted_at.desc()).all()
    return jsonify({'attempts': [att.to_dict() for att in attempts]}), 200

@quiz_bp.route('/attempts/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt_detail(attempt_id: int) -> Tuple[Any, int]:
    user_id = int(get_jwt_identity())
    attempt = Attempt.query.get(attempt_id)
    if not attempt:
        return error_response('Không tìm thấy kết quả làm bài', 404)
    user = User.query.get(user_id)
    if attempt.user_id != user_id and (not user or user.role != 'admin'):
        return error_response('Bạn không có quyền xem kết quả này', 403)
    quiz = Quiz.query.get(attempt.quiz_id)
    details = AttemptDetail.query.filter_by(attempt_id=attempt.id).all()
    user_answers_map = {d.question_id: d.selected_choice_id for d in details}
    reviews = []
    if quiz:
        for q in sorted(quiz.questions, key=lambda x: x.order_num):
            sel_id = user_answers_map.get(q.id)
            c_choice = Choice.query.filter_by(question_id=q.id, is_correct=True).first()
            c_id = c_choice.id if c_choice else None
            reviews.append({
                'question_id': q.id, 'content': q.content, 'explanation': q.explanation or '',
                'order_num': q.order_num, 'selected_choice_id': sel_id, 'correct_choice_id': c_id,
                'is_correct': (sel_id is not None and c_id is not None and sel_id == c_id),
                'choices': [{'id': c.id, 'content': c.content, 'is_correct': c.is_correct} for c in q.choices]
            })
    return jsonify({'attempt': attempt.to_dict(), 'question_reviews': reviews}), 200
