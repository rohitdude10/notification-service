"""
Configuration settings for different environments
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    # Mailjet Configuration
    MJ_APIKEY_PUBLIC = os.getenv('MJ_APIKEY_PUBLIC')
    MJ_APIKEY_PRIVATE = os.getenv('MJ_APIKEY_PRIVATE')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'rohitkumardude10@gmail.com')
    SENDER_NAME = os.getenv('SENDER_NAME', 'Inquiry')
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # CORS Configuration
    CORS_ORIGINS = "*"  # Allow all origins by default
    CORS_METHODS = ["GET", "POST", "OPTIONS"]
    CORS_HEADERS = ["Content-Type", "Authorization", "Access-Control-Allow-Origin"]
    
    # API Configuration
    API_PREFIX = '/api/v1'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    CORS_ORIGINS = "*"  # Allow all origins in development

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    RATELIMIT_DEFAULT = "50 per minute"  # Stricter rate limiting in production
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # Allow all origins by default

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    RATELIMIT_DEFAULT = "1000 per minute"  # Higher rate limit for testing
    CORS_ORIGINS = "*"  # Allow all origins in testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 