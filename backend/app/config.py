import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    ]
