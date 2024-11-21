import os

class Config:
    # Using a more secure connection string with environment variables
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce.db'  # Using SQLite for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'