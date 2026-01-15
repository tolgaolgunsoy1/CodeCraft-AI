"""
Advanced Configuration Management for Android App Generator
Provides secure, scalable configuration with environment-based settings
"""

import os
from datetime import timedelta
from dynaconf import Dynaconf
from typing import Dict, Any

# Initialize Dynaconf with multiple sources
settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    envvar_prefix='ANDROID_GEN',
    load_dotenv=True,
)

# Core Configuration Class
class Config:
    """Production-ready configuration with security and performance optimizations"""

    # Flask Configuration
    SECRET_KEY = settings.get('SECRET_KEY', os.urandom(32).hex())
    DEBUG = settings.get('DEBUG', False)
    TESTING = settings.get('TESTING', False)

    # Server Configuration
    HOST = settings.get('HOST', '0.0.0.0')
    PORT = settings.get('PORT', 5000)
    WORKERS = settings.get('WORKERS', 4)

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = settings.get(
        'DATABASE_URL',
        'sqlite:///android_generator.db'
    )
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///android_generator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'echo': DEBUG
    }

    # Redis Configuration
    REDIS_URL = settings.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'RedisCache' if REDIS_URL != 'redis://localhost:6379/0' else 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'android_gen:'

    # JWT Configuration
    JWT_SECRET_KEY = settings.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRE = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = not DEBUG
    JWT_COOKIE_CSRF_PROTECT = True

    # Rate Limiting
    RATELIMIT_STORAGE_URI = REDIS_URL
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '100 per hour'
    RATELIMIT_API = '50 per minute'

    # File Upload Configuration
    UPLOAD_FOLDER = settings.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'md', 'doc', 'docx', 'pdf', 'json'}

    # Project Storage
    PROJECT_STORAGE_PATH = settings.get('PROJECT_STORAGE_PATH', os.path.join(os.path.dirname(__file__), '..', 'generated_apps'))
    TEMP_STORAGE_HOURS = settings.get('TEMP_STORAGE_HOURS', 24)
    MAX_PROJECT_SIZE_MB = settings.get('MAX_PROJECT_SIZE_MB', 100)

    # Concurrent Processing
    MAX_CONCURRENT_GENERATIONS = settings.get('MAX_CONCURRENT_GENERATIONS', 5)
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    # External API Keys (loaded from environment)
    STRIPE_SECRET_KEY = settings.get('STRIPE_SECRET_KEY')
    FIREBASE_PROJECT_ID = settings.get('FIREBASE_PROJECT_ID')
    GOOGLE_ANALYTICS_ID = settings.get('GOOGLE_ANALYTICS_ID')
    SENTRY_DSN = settings.get('SENTRY_DSN')

    # Security Settings
    SESSION_COOKIE_SECURE = not DEBUG
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # CORS Configuration
    CORS_ORIGINS = settings.get('CORS_ORIGINS', ['http://localhost:3000', 'http://localhost:5000'])
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    CORS_EXPOSE_HEADERS = ['X-Total-Count', 'X-Page-Count']
    CORS_SUPPORTS_CREDENTIALS = True

    # Logging Configuration
    LOG_LEVEL = settings.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = settings.get('LOG_FILE', 'app.log')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    # Monitoring
    ENABLE_METRICS = settings.get('ENABLE_METRICS', True)
    METRICS_PORT = settings.get('METRICS_PORT', 9090)

    # Feature Flags
    ENABLE_REAL_TIME_UPDATES = settings.get('ENABLE_REAL_TIME_UPDATES', True)
    ENABLE_ANALYTICS = settings.get('ENABLE_ANALYTICS', True)
    ENABLE_CACHING = settings.get('ENABLE_CACHING', True)
    ENABLE_BACKGROUND_TASKS = settings.get('ENABLE_BACKGROUND_TASKS', True)

    @classmethod
    def init_app(cls, app):
        """Initialize Flask application with configuration"""
        # Configure logging
        import logging
        from logging.handlers import RotatingFileHandler

        # Clear existing handlers
        app.logger.handlers.clear()

        # Set log level
        app.logger.setLevel(getattr(logging, cls.LOG_LEVEL))

        # Create formatters
        formatter = logging.Formatter(cls.LOG_FORMAT)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

        # File handler
        if cls.LOG_FILE:
            file_handler = RotatingFileHandler(
                cls.LOG_FILE,
                maxBytes=cls.LOG_MAX_BYTES,
                backupCount=cls.LOG_BACKUP_COUNT
            )
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)

        # Configure SQLAlchemy
        from flask_sqlalchemy import SQLAlchemy
        db = SQLAlchemy()
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cls.SQLALCHEMY_TRACK_MODIFICATIONS
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = cls.SQLALCHEMY_ENGINE_OPTIONS
        db.init_app(app)

        # Configure JWT
        from flask_jwt_extended import JWTManager
        jwt = JWTManager()
        jwt.init_app(app)

        # Configure caching
        # from flask_caching import Cache
        # cache = Cache()
        # cache.init_app(app, config={
        #     'CACHE_TYPE': cls.CACHE_TYPE,
        #     'CACHE_REDIS_URL': cls.REDIS_URL if cls.CACHE_TYPE == 'RedisCache' else None,
        #     'CACHE_DEFAULT_TIMEOUT': cls.CACHE_DEFAULT_TIMEOUT,
        #     'CACHE_KEY_PREFIX': cls.CACHE_KEY_PREFIX
        # })

        # Configure rate limiting
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=cls.RATELIMIT_STORAGE_URI,
            strategy=cls.RATELIMIT_STRATEGY
        )

        # Configure CORS
        from flask_cors import CORS
        CORS(app, resources={
            r"/*": {
                "origins": cls.CORS_ORIGINS,
                "methods": cls.CORS_METHODS,
                "allow_headers": cls.CORS_ALLOW_HEADERS,
                "expose_headers": cls.CORS_EXPOSE_HEADERS,
                "supports_credentials": cls.CORS_SUPPORTS_CREDENTIALS
            }
        })

        # Initialize monitoring if enabled
        if cls.ENABLE_METRICS:
            cls._init_monitoring(app)

        app.config.from_object(cls)

    @classmethod
    def _init_monitoring(cls, app):
        """Initialize monitoring and metrics"""
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration

            if cls.SENTRY_DSN:
                sentry_sdk.init(
                    dsn=cls.SENTRY_DSN,
                    integrations=[FlaskIntegration()],
                    environment='production' if not cls.DEBUG else 'development',
                    traces_sample_rate=1.0
                )
        except ImportError:
            app.logger.warning("Sentry SDK not available, monitoring disabled")

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_android_generator.db'
    CACHE_TYPE = 'SimpleCache'
    ENABLE_METRICS = False

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_android_generator.db'
    CACHE_TYPE = 'SimpleCache'
    WTF_CSRF_ENABLED = False
    ENABLE_METRICS = False

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    ENABLE_METRICS = True

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}

def get_config(config_name: str = None) -> Config:
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    return config.get(config_name, config['default'])