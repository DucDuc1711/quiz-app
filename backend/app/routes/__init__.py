from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

from app.routes import auth, quiz, admin  # noqa: E402, F401
