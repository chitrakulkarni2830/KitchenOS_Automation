import os

class Config:
    PORT = int(os.environ.get("PORT", 8000))
    DB_PATH = os.environ.get("DB_PATH", "database/kitchen_os.db")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS", 3600))
    STATIC_FOLDER = os.environ.get("STATIC_FOLDER", "frontend")
