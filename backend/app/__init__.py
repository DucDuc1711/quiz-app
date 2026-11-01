import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.config import Config
from app.models import db
from app.routes import auth_bp, quiz_bp, admin_bp

jwt = JWTManager()
migrate = Migrate()

def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    CORS(app, origins=app.config.get('CORS_ORIGINS', ['http://localhost:5173']), supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Tài nguyên không tồn tại'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Lỗi hệ thống nội bộ'}), 500

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({'error': 'Yêu cầu Token xác thực'}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return jsonify({'error': 'Token không hợp lệ hoặc đã hết hạn'}), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({'error': 'Token đã hết hạn, vui lòng đăng nhập lại'}), 401

    return app
