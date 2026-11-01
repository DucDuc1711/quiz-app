from typing import Any, Dict, List, Tuple
from flask import request, jsonify
from app.models import db, Quiz, Question, Choice, Attempt, User
from app.routes import admin_bp
from app.utils import admin_required, error_response

@admin_bp.route('/quizzes', methods=['GET'])
@admin_required
def get_admin_quizzes() -> Tuple[Any, int]:
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return jsonify({'quizzes': [q.to_dict(include_questions=True, is_admin=True) for q in quizzes]}), 200

@admin_bp.route('/quizzes', methods=['POST'])
@admin_required
def create_quiz() -> Tuple[Any, int]:
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    time_limit = data.get('time_limit', 10)
    if not title: return error_response('Tên bộ quiz không được để trống', 400)
    try:
        time_limit = int(time_limit)
        if time_limit <= 0: raise ValueError()
    except ValueError:
        return error_response('Thời gian làm bài phải là số nguyên dương', 400)
    quiz = Quiz(title=title, description=description, time_limit=time_limit)
    db.session.add(quiz); db.session.commit()
    return jsonify({'message': 'Tạo bộ quiz thành công', 'quiz': quiz.to_dict(include_questions=True, is_admin=True)}), 201

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
@admin_required
def get_admin_quiz(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)
    if not quiz: return error_response('Không tìm thấy bộ quiz này', 404)
    return jsonify({'quiz': quiz.to_dict(include_questions=True, is_admin=True)}), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)
    if not quiz: return error_response('Không tìm thấy bộ quiz này', 404)
    data = request.get_json() or {}
    if 'title' in data:
        t = str(data['title']).strip()
        if not t: return error_response('Tên bộ quiz không được để trống', 400)
        quiz.title = t
    if 'description' in data: quiz.description = str(data['description']).strip()
    if 'time_limit' in data:
        try:
            val = int(data['time_limit'])
            if val <= 0: raise ValueError()
            quiz.time_limit = val
        except ValueError:
            return error_response('Thời gian làm bài phải là số nguyên dương', 400)
    db.session.commit()
    return jsonify({'message': 'Cập nhật bộ quiz thành công', 'quiz': quiz.to_dict(include_questions=True, is_admin=True)}), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def create_question(quiz_id: int) -> Tuple[Any, int]:
    quiz = Quiz.query.get(quiz_id)
    if not quiz: return error_response('Không tìm thấy bộ quiz này', 404)
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    explanation = data.get('explanation', '').strip()
    choices_data = data.get('choices', [])
    if not content: return error_response('Nội dung câu hỏi không được để trống', 400)
    if not choices_data or len(choices_data) < 2: return error_response('Câu hỏi phải có ít nhất 2 lựa chọn đáp án', 400)
    if sum(1 for c in choices_data if c.get('is_correct')) != 1: return error_response('Phải có chính xác 1 đáp án đúng', 400)

    question = Question(quiz_id=quiz.id, content=content, explanation=explanation, order_num=len(quiz.questions) + 1)
    db.session.add(question); db.session.flush()
    for c in choices_data:
        c_text = str(c.get('content', '')).strip()
        if not c_text:
            db.session.rollback()
            return error_response('Nội dung đáp án không được để trống', 400)
        db.session.add(Choice(question_id=question.id, content=c_text, is_correct=bool(c.get('is_correct'))))
    db.session.commit()
    return jsonify({'message': 'Thêm câu hỏi thành công', 'question': question.to_dict(is_admin=True)}), 201

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id: int) -> Tuple[Any, int]:
    question = Question.query.get(question_id)
    if not question: return error_response('Không tìm thấy câu hỏi này', 404)
    data = request.get_json() or {}
    if 'content' in data:
        cnt = str(data['content']).strip()
        if not cnt: return error_response('Nội dung câu hỏi không được để trống', 400)
        question.content = cnt
    if 'explanation' in data: question.explanation = str(data['explanation']).strip()
    if 'choices' in data:
        choices_data = data['choices']
        if len(choices_data) < 2: return error_response('Câu hỏi phải có ít nhất 2 đáp án', 400)
        if sum(1 for c in choices_data if c.get('is_correct')) != 1: return error_response('Phải có chính xác 1 đáp án đúng', 400)
        Choice.query.filter_by(question_id=question.id).delete()
        for c in choices_data:
            c_text = str(c.get('content', '')).strip()
            if not c_text:
                db.session.rollback()
                return error_response('Nội dung đáp án không được để trống', 400)
            db.session.add(Choice(question_id=question.id, content=c_text, is_correct=bool(c.get('is_correct'))))
    db.session.commit()
    return jsonify({'message': 'Cập nhật câu hỏi thành công', 'question': question.to_dict(is_admin=True)}), 200

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id: int) -> Tuple[Any, int]:
    question = Question.query.get(question_id)
    if not question: return error_response('Không tìm thấy câu hỏi này', 404)
    quiz_id = question.quiz_id
    db.session.delete(question); db.session.commit()
    for idx, q in enumerate(Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order_num.asc()).all(), 1):
        q.order_num = idx
    db.session.commit()
    return jsonify({'message': 'Xóa câu hỏi thành công'}), 200

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats() -> Tuple[Any, int]:
    return jsonify({
        'stats': {
            'total_users': User.query.count(),
            'total_quizzes': Quiz.query.count(),
            'total_questions': Question.query.count(),
            'total_attempts': Attempt.query.count(),
            'recent_attempts': [a.to_dict() for a in Attempt.query.order_by(Attempt.submitted_at.desc()).limit(5).all()]
        }
    }), 200

    if not quiz: return error_response('Không tìm thấy bộ quiz này', 404)
    db.session.delete(quiz); db.session.commit()
    return jsonify({'message': 'Xóa bộ quiz thành công'}), 200
