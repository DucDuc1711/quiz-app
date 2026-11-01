from functools import wraps
from typing import Any, Callable, Tuple
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User

def error_response(message: str, status_code: int = 400) -> Tuple[Any, int]:
    return jsonify({'error': message}), status_code

def admin_required(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return error_response('Invalid identity', 401)
            
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return error_response('Yêu cầu quyền Quản trị viên (Admin)', 403)
        return fn(*args, **kwargs)
    return wrapper
