import os
from app import create_app
from app.models import db, User, Quiz, Question, Choice

app = create_app()

@app.cli.command('seed')
def seed_data() -> None:
    """Seed initial admin account and sample 5-question quiz."""
    with app.app_context():
        db.create_all()

        # Seed Admin User
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin_user.set_password('123456')
            db.session.add(admin_user)
            print("[SEED] Đã tạo tài khoản admin thành công (Username: admin, Password: admin123)")

        # Seed Sample Quiz
        sample_quiz = Quiz.query.filter_by(title='Lập Trình Python Cơ Bản').first()
        if not sample_quiz:
            sample_quiz = Quiz(
                title='Lập Trình Python Cơ Bản',
                description='Bộ câu hỏi kiểm tra kiến thức cơ bản về ngôn ngữ Python.',
                time_limit=10
            )
            db.session.add(sample_quiz)
            db.session.flush()

            questions_data = [
                {
                    'content': 'Python là ngôn ngữ lập trình thuộc loại nào?',
                    'explanation': 'Python là ngôn ngữ thông dịch (interpreted), hướng đối tượng và có cú pháp đơn giản.',
                    'order_num': 1,
                    'choices': [
                        ('Ngôn ngữ thông dịch (Interpreted)', True),
                        ('Ngôn ngữ biên dịch thuần túy (Compiled)', False),
                        ('Ngôn ngữ máy (Machine Language)', False),
                        ('Hợp ngữ (Assembly)', False)
                    ]
                },
                {
                    'content': 'Kiểu dữ liệu nào trong Python là MUTABLE (có thể thay đổi)?',
                    'explanation': 'List và Dictionary trong Python là mutable (có thể sửa đổi phần tử sau khi khởi tạo). Tuple, int, str là immutable.',
                    'order_num': 2,
                    'choices': [
                        ('Tuple', False),
                        ('List', True),
                        ('String', False),
                        ('Integer', False)
                    ]
                },
                {
                    'content': 'HTTP status code nào đại diện cho "200 OK"?',
                    'explanation': 'Mã trạng thái HTTP 200 biểu thị yêu cầu đã thành công.',
                    'order_num': 3,
                    'choices': [
                        ('200', True),
                        ('404', False),
                        ('500', False),
                        ('302', False)
                    ]
                },
                {
                    'content': 'Decorator nào trong Flask-JWT-Extended dùng để bảo vệ API route?',
                    'explanation': '@jwt_required() được sử dụng để bắt buộc yêu cầu có JWT Access Token trong Header.',
                    'order_num': 4,
                    'choices': [
                        ('@jwt_required()', True),
                        ('@login_required', False),
                        ('@auth_only', False),
                        ('@check_jwt()', False)
                    ]
                },
                {
                    'content': 'Lệnh nào trong Flask dùng để chạy ứng dụng ở chế độ phát triển?',
                    'explanation': 'Lệnh `flask run` khởi chạy máy chủ thử nghiệm của Flask.',
                    'order_num': 5,
                    'choices': [
                        ('flask run', True),
                        ('python start.py', False),
                        ('flask start', False),
                        ('npm start', False)
                    ]
                }
            ]

            for q_data in questions_data:
                question = Question(
                    quiz_id=sample_quiz.id,
                    content=q_data['content'],
                    explanation=q_data['explanation'],
                    order_num=q_data['order_num']
                )
                db.session.add(question)
                db.session.flush()

                for choice_text, is_correct in q_data['choices']:
                    choice = Choice(
                        question_id=question.id,
                        content=choice_text,
                        is_correct=is_correct
                    )
                    db.session.add(choice)

            print("[SEED] Đã tạo bộ Quiz mẫu 5 câu hỏi thành công!")

        db.session.commit()
        print("[SEED] Hoàn thành seed dữ liệu lần đầu!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
