from typing import Any, Tuple
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User
from app.routes import auth_bp
from app.utils import error_response

@auth_bp.route('/register', methods=['POST'])
def register() -> Tuple[Any, int]:
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return error_response('Vui lòng điền đầy đủ username, email và password', 400)

    if len(username) < 3:
        return error_response('Tên đăng nhập phải có ít nhất 3 ký tự', 400)

    if len(password) < 6:
        return error_response('Mật khẩu phải có ít nhất 6 ký tự', 400)

    if User.query.filter_by(username=username).first():
        return error_response('Tên đăng nhập đã tồn tại', 400)

    if User.query.filter_by(email=email).first():
        return error_response('Email đã được sử dụng', 400)

    user = User(username=username, email=email, role='user')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'message': 'Đăng ký tài khoản thành công',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login() -> Tuple[Any, int]:
    data = request.get_json() or {}
    account = data.get('username_or_email', '').strip()
    password = data.get('password', '')

    if not account or not password:
        return error_response('Vui lòng nhập tên đăng nhập/email và mật khẩu', 400)

    user = User.query.filter((User.username == account) | (User.email == account.lower())).first()

    if not user or not user.check_password(password):
        return error_response('Tên đăng nhập hoặc mật khẩu không chính xác', 401)

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'message': 'Đăng nhập thành công',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me() -> Tuple[Any, int]:
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return error_response('Không tìm thấy thông tin người dùng', 404)
    return jsonify({'user': user.to_dict()}), 200
