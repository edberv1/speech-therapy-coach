import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "jwtsecretkey"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
