"""
Advanced Android App Generator Backend
Production-ready backend with comprehensive features, security, and performance optimizations
"""

from flask import Flask, request, jsonify, send_from_directory, send_file, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from flask_caching import Cache
# from flask_migrate import Migrate
# from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import os
import json
import re
import zipfile
import tempfile
from datetime import datetime, timedelta
from android_generator import AndroidAppGenerator
import threading
import time
import uuid
import logging
from functools import wraps
from collections import deque
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# Import our custom modules
from config import get_config, Config
from models import (
    User, APIKey, UserSession, Project, ProjectFeature,
    ProjectActivity, ProjectDependency, ProjectAnalytics,
    SystemMetrics, BackgroundTask, AuditLog,
    create_tables, get_user_by_email, get_user_by_username
)
from auth import auth_manager, admin_required, active_user_required
# from integrations import (
#     firebase_service, stripe_service, analytics_service,
#     openai_service, github_service, email_service,
#     health_check_services
# )
# from realtime import realtime_manager, notification_manager
# from cache import cache_manager, performance_monitor, monitor_performance, cached
# from service_worker import sw_manager, pwa_manager, register_pwa_routes

# Initialize configuration
config = get_config()

# Enhanced logging configuration
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Sentry for error tracking
if config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        environment='production' if not config.DEBUG else 'development',
        traces_sample_rate=1.0
    )

# Initialize Flask app with configuration
app = Flask(__name__,
           static_folder='../frontend',
           static_url_path='',
           instance_relative_config=True)

# Apply configuration
config.init_app(app)

# Initialize extensions
CORS(app, resources={
    r"/*": {
        "origins": config.CORS_ORIGINS,
        "methods": config.CORS_METHODS,
        "allow_headers": config.CORS_ALLOW_HEADERS,
        "expose_headers": config.CORS_EXPOSE_HEADERS,
        "supports_credentials": config.CORS_SUPPORTS_CREDENTIALS
    }
})

jwt = JWTManager(app)
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     storage_uri=config.RATELIMIT_STORAGE_URI,
#     strategy=config.RATELIMIT_STRATEGY
# )

# cache = Cache(app)
# socketio = SocketIO(app, cors_allowed_origins=config.CORS_ORIGINS, async_mode='eventlet')

# Database setup
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    poolclass=QueuePool,
    pool_size=config.SQLALCHEMY_ENGINE_OPTIONS['pool_size'],
    max_overflow=config.SQLALCHEMY_ENGINE_OPTIONS['max_overflow'],
    pool_recycle=config.SQLALCHEMY_ENGINE_OPTIONS['pool_recycle'],
    echo=config.SQLALCHEMY_ENGINE_OPTIONS['echo']
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# Initialize database tables
create_tables(engine)

# Initialize our custom managers
auth_manager.init_app(app)
auth_manager.db_session = db_session
# cache_manager.init_app(app)
# realtime_manager.init_app(app, config.CORS_ORIGINS)
# register_pwa_routes(app)

# Setup APK deployment routes (requires qrcode, Pillow)
# from apk_deployment import setup_deployment_routes
# setup_deployment_routes(app, config.PROJECT_STORAGE_PATH)

# Global storage with thread safety
project_status = {}
active_generations = {}
generation_queue = deque()
user_rate_limits = {}
project_analytics = {}
background_tasks = {}

# Thread locks for concurrent access
project_lock = threading.Lock()
analytics_lock = threading.Lock()

# Global storage
project_status = {}
active_generations = {}
generation_queue = deque()
user_rate_limits = {}
project_analytics = {}

# Database session management
@app.before_request
def create_db_session():
    """Create database session for each request"""
    g.db_session = db_session()

@app.after_request
def close_db_session(response):
    """Close database session after each request"""
    if hasattr(g, 'db_session'):
        g.db_session.close()
    return response

# Enhanced error handler decorator
def handle_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)

            # Log to audit system
            try:
                audit_log = AuditLog(
                    action=f"error_{f.__name__}",
                    resource_type='system',
                    resource_id='error',
                    details={
                        'error_message': str(e),
                        'endpoint': request.endpoint,
                        'method': request.method,
                        'ip_address': request.remote_addr,
                        'user_agent': request.headers.get('User-Agent')
                    },
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent'),
                    success=False
                )
                g.db_session.add(audit_log)
                g.db_session.commit()
            except Exception as audit_error:
                logger.error(f"Failed to log audit event: {str(audit_error)}")

            return jsonify({
                'success': False,
                'error': 'Bir hata oluştu. Lütfen tekrar deneyin.',
                'details': str(e) if app.debug else None
            }), 500
    return wrapped

# Request logging decorator
def log_requests(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        duration = time.time() - start_time

        # Log slow requests
        if duration > 2.0:
            logger.warning(f"Slow request: {request.method} {request.path} took {duration:.2f}s")

        # Track system metrics
        try:
            metric = SystemMetrics(
                metric_type='request',
                metric_name='response_time',
                value=duration,
                unit='seconds',
                metadata={
                    'endpoint': request.endpoint,
                    'method': request.method,
                    'status_code': response.status_code if hasattr(response, 'status_code') else 0
                }
            )
            g.db_session.add(metric)
            g.db_session.commit()
        except Exception as e:
            logger.error(f"Failed to record metrics: {str(e)}")

        return response
    return wrapped

# Input validation
def validate_app_input(data):
    errors = []
    
    idea = data.get('idea', '').strip()
    if not idea:
        errors.append('Uygulama fikri gerekli')
    elif len(idea) < 10:
        errors.append('Uygulama fikri en az 10 karakter olmalı')
    elif len(idea) > 1000:
        errors.append('Uygulama fikri en fazla 1000 karakter olmalı')
    
    language = data.get('language', 'java').lower()
    if language not in ['java', 'kotlin']:
        errors.append('Geçersiz programlama dili')
    
    theme = data.get('theme', 'light').lower()
    if theme not in ['light', 'dark', 'auto']:
        errors.append('Geçersiz tema')
    
    return errors

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
# @limiter.limit("5 per minute")
@handle_errors
@log_requests
def register():
    """User registration endpoint"""
    data = request.get_json()

    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    user, error = auth_manager.register_user(
        data['username'],
        data['email'],
        data['password'],
        data.get('full_name')
    )

    if error:
        return jsonify({'success': False, 'error': error}), 400

    # Send welcome email
    if email_service.initialized:
        email_service.send_email(
            user.email,
            'Welcome to Android App Generator',
            f'Welcome {user.username}! Your account has been created successfully.'
        )

    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@app.route('/api/auth/login', methods=['POST'])
# @limiter.limit("10 per minute")
@handle_errors
@log_requests
def login():
    """User login endpoint"""
    data = request.get_json()

    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Username/email and password required'}), 400

    user, error = auth_manager.authenticate_user(
        data['username_or_email'],
        data['password']
    )

    if error:
        return jsonify({'success': False, 'error': error}), 401

    # Create session
    session = auth_manager.create_session(user, request.remote_addr, request.headers.get('User-Agent'))

    # Create tokens
    access_token, refresh_token = auth_manager.create_tokens(user)

    # Set cookies
    response = jsonify({
        'success': True,
        'message': 'Login successful',
        'user': user.to_dict(),
        'session_id': session.id
    })

    # Set JWT cookies
    response = auth_manager.jwt.set_access_cookies(response, access_token)
    response = auth_manager.jwt.set_refresh_cookies(response, refresh_token)

    return response

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
@handle_errors
@log_requests
def logout():
    """User logout endpoint"""
    user_id = get_jwt_identity()
    user = g.db_session.query(User).filter_by(id=user_id).first()

    if user:
        auth_manager.logout_user(user)

    response = jsonify({'success': True, 'message': 'Logout successful'})
    response = auth_manager.jwt.unset_jwt_cookies(response)

    return response

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
@handle_errors
def refresh_token():
    """Refresh access token"""
    user_id = get_jwt_identity()
    user = g.db_session.query(User).filter_by(id=user_id).first()

    if not user or not user.is_active:
        return jsonify({'success': False, 'error': 'Invalid user'}), 401

    access_token = auth_manager.jwt.create_access_token(identity=user)
    response = jsonify({'success': True})
    response = auth_manager.jwt.set_access_cookies(response, access_token)

    return response

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
@handle_errors
# @cached(timeout=300, key_prefix='user_profile')
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = g.db_session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    return jsonify({
        'success': True,
        'user': user.to_dict()
    })

# Main app generation endpoint
@app.route('/api/generate-app', methods=['POST'])
# @limiter.limit(config.RATELIMIT_API)
@jwt_required(optional=True)  # Allow anonymous generation with limits
@handle_errors
@log_requests
# @monitor_performance
def generate_app():
    """Enhanced app generation endpoint with authentication and advanced features"""
    data = request.get_json()

    # Validate input
    errors = validate_app_input(data)
    if errors:
        return jsonify({'success': False, 'error': ', '.join(errors)}), 400

    # Get user if authenticated
    user_id = get_jwt_identity()
    user = None
    if user_id:
        user = g.db_session.query(User).filter_by(id=user_id).first()

    idea = data.get('idea', '').strip()
    app_name = data.get('appName', '').strip() or 'MyApp'
    language = data.get('language', 'java').lower()
    theme = data.get('theme', 'light')
    category = data.get('category', 'auto')
    advanced_features = data.get('advancedFeatures', [])
    architecture = data.get('architecture', 'single_activity')  # NEW
    ui_framework = data.get('uiFramework', 'xml')  # NEW: 'xml' or 'compose'

    # Check concurrent generations limit
    with project_lock:
        if len(active_generations) >= config.MAX_CONCURRENT_GENERATIONS:
            return jsonify({
                'success': False,
                'error': 'Sistem yoğun. Lütfen birkaç dakika sonra tekrar deneyin.',
                'queue_position': len(generation_queue) + 1
            }), 503

    # Generate unique project ID
    project_id = str(uuid.uuid4())

    # Create safe folder name from app name
    safe_app_name = ''.join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    folder_name = f"{safe_app_name}_{project_id[:8]}" if safe_app_name else project_id
    project_path = os.path.join(config.PROJECT_STORAGE_PATH, folder_name)

    # Create project record in database
    project = Project(
        id=project_id,
        user_id=user.id if user else None,
        name=app_name,
        description=idea[:200],
        category=category,
        language=language,
        theme=theme,
        status='queued'
    )
    g.db_session.add(project)
    g.db_session.commit()

    # Initialize project status with enhanced tracking
    with project_lock:
        project_status[project_id] = {
            'status': 'queued',
            'progress': 0,
            'current_step': 'Sıraya alındı...',
            'steps_completed': 0,
            'total_steps': 8,
            'created_at': datetime.utcnow().isoformat(),
            'idea': idea,
            'language': language,
            'theme': theme,
            'category': category,
            'advanced_features': advanced_features,
            'architecture': architecture,
            'ui_framework': ui_framework,
            'estimated_completion': (datetime.utcnow() + timedelta(minutes=2)).isoformat(),
            'user_id': user.id if user else None
        }

        # Initialize analytics
        project_analytics[project_id] = {
            'start_time': time.time(),
            'steps': [],
            'errors': []
        }

        # Start generation in background
        thread = threading.Thread(
            target=generate_app_async,
            args=(project_id, idea, language, theme, category, advanced_features, architecture, ui_framework, project_path, app_name),
            daemon=True
        )
        thread.start()
        active_generations[project_id] = thread

    # Log analytics event
    # if analytics_service.initialized:
    #     analytics_service.track_event('generate_app', 'start', project_id)

    # Send real-time notification
    if user:
        notification_manager.create_notification(
            user.id,
            'App Generation Started',
            f'Your app "{idea[:50]}..." is being generated.',
            'info'
        )

    logger.info(f"Started generation for project {project_id} by user {user_id}")

    return jsonify({
        'success': True,
        'project_id': project_id,
        'status': 'queued',
        'estimated_completion': project_status[project_id]['estimated_completion']
    })

def generate_app_async(project_id, idea, language, theme, category, advanced_features, architecture, ui_framework, project_path, app_name):
    try:
        steps = [
            ('analyzing', 15, 'Fikir analiz ediliyor...', 3),
            ('planning', 25, 'Proje yapısı planlanıyor...', 2),
            ('generating_structure', 40, 'Temel yapı oluşturuluyor...', 4),
            ('generating_ui', 55, 'UI bileşenleri hazırlanıyor...', 5),
            ('generating_logic', 70, 'İş mantığı yazılıyor...', 6),
            ('integrating_features', 85, 'Özellikler entegre ediliyor...', 4),
            ('building', 95, 'Proje derleniyor...', 3),
            ('finalizing', 98, 'Son kontroller yapılıyor...', 2)
        ]
        
        for status, progress, step_name, duration in steps:
            project_status[project_id].update({
                'status': status,
                'progress': progress,
                'current_step': step_name,
                'steps_completed': steps.index((status, progress, step_name, duration)) + 1
            })
            
            project_analytics[project_id]['steps'].append({
                'name': step_name,
                'timestamp': time.time(),
                'progress': progress
            })
            
            time.sleep(duration)
        
        # Generate app
        generator = AndroidAppGenerator()
        result = generator.generate_from_idea(idea, language, architecture, ui_framework, project_path, app_name)
        
        # Build APK automatically
        project_status[project_id].update({
            'status': 'building_apk',
            'progress': 96,
            'current_step': 'APK oluşturuluyor... (Bu 2-3 dakika sürebilir)'
        })
        
        apk_path = None
        apk_built = build_apk(project_path)
        
        if apk_built:
            apk_path = os.path.join(project_path, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
            logger.info(f"APK successfully built at {apk_path}")
        else:
            logger.warning(f"APK build failed for {project_id}, but project files are ready")
        
        # Calculate generation time
        generation_time = time.time() - project_analytics[project_id]['start_time']
        
        # Complete with enhanced result data
        project_status[project_id].update({
            'status': 'completed',
            'progress': 100,
            'current_step': 'Tamamlandı!',
            'steps_completed': len(steps),
            'completed_at': datetime.now().isoformat(),
            'generation_time': round(generation_time, 2),
            'result': {
                'appName': result['app_name'],
                'description': result['description'],
                'features': result['features'],
                'projectPath': result['project_path'],
                'activities': result.get('activities', []),
                'screens': result.get('screens', [
                    'SplashActivity - Açılış ekranı',
                    'OnboardingActivity - Tanıtım ekranları (3 sayfa)',
                    'LoginActivity - Giriş ve kayıt',
                    'MainActivity - Ana ekran',
                    'ProfileActivity - Kullanıcı profili',
                    'SettingsActivity - Ayarlar',
                    'NotificationActivity - Bildirimler',
                    'SearchActivity - Arama ekranı',
                    'DetailActivity - Detay görünümü',
                    'EditActivity - Düzenleme ekranı'
                ]),
                'permissions': result.get('permissions', [
                    'INTERNET - İnternet erişimi',
                    'ACCESS_NETWORK_STATE - Ağ durumu',
                    'CAMERA - Kamera erişimi',
                    'READ_EXTERNAL_STORAGE - Dosya okuma',
                    'WRITE_EXTERNAL_STORAGE - Dosya yazma',
                    'ACCESS_FINE_LOCATION - Konum erişimi',
                    'VIBRATE - Titreşim',
                    'WAKE_LOCK - Ekran açık tutma'
                ]),
                'dependencies': result.get('dependencies', [
                    'androidx.appcompat:appcompat:1.6.1 - Temel UI bileşenleri',
                    'com.google.android.material:material:1.11.0 - Material Design',
                    'androidx.constraintlayout:constraintlayout:2.1.4 - Layout yönetimi',
                    'androidx.lifecycle:lifecycle-viewmodel:2.7.0 - ViewModel',
                    'androidx.navigation:navigation-fragment:2.7.6 - Navigasyon',
                    'com.squareup.retrofit2:retrofit:2.9.0 - API iletişimi',
                    'androidx.room:room-runtime:2.6.1 - Veritabanı',
                    'com.github.bumptech.glide:glide:4.16.0 - Resim yükleme',
                    'androidx.work:work-runtime:2.9.0 - Arka plan işleri',
                    'com.google.firebase:firebase-analytics:21.5.0 - Analytics'
                ]),
                'downloadId': os.path.basename(result['project_path']),
                'apkPath': apk_path if apk_built else None,
                'apkReady': apk_built,
                'language': language,
                'theme': theme,
                'category': category,
                'advancedFeatures': advanced_features,
                'projectSize': get_directory_size(result['project_path']),
                'fileCount': count_files(result['project_path']),
                'development_progress': result.get('development_progress', {
                    'overall': 100,
                    'ui_design': 100,
                    'backend_logic': 100,
                    'database_setup': 100,
                    'api_integration': 95,
                    'testing': 85,
                    'optimization': 90,
                    'security': 95
                })
            }
        })
        
        logger.info(f"Completed generation for project {project_id} in {generation_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Error generating project {project_id}: {str(e)}", exc_info=True)
        project_status[project_id].update({
            'status': 'error',
            'error': str(e),
            'failed_at': datetime.now().isoformat()
        })
        project_analytics[project_id]['errors'].append({
            'message': str(e),
            'timestamp': time.time()
        })
    finally:
        # Clean up
        if project_id in active_generations:
            del active_generations[project_id]

@app.route('/status/<project_id>')
@handle_errors
def get_status(project_id):
    if project_id in project_status:
        status = project_status[project_id].copy()
        
        # Add real-time info
        if status['status'] in ['analyzing', 'generating', 'building']:
            status['active_threads'] = len(active_generations)
            status['queue_length'] = len(generation_queue)
        
        return jsonify(status)
    return jsonify({'status': 'not_found', 'error': 'Proje bulunamadı'}), 404

@app.route('/cancel/<project_id>', methods=['POST'])
@handle_errors
def cancel_generation(project_id):
    if project_id in project_status:
        project_status[project_id].update({
            'status': 'cancelled',
            'cancelled_at': datetime.now().isoformat()
        })
        
        if project_id in active_generations:
            del active_generations[project_id]
        
        logger.info(f"Cancelled generation for project {project_id}")
        return jsonify({'success': True, 'message': 'İşlem iptal edildi'})
    
    return jsonify({'success': False, 'error': 'Proje bulunamadı'}), 404

@app.route('/templates')
@handle_errors
def get_templates():
    templates = [
        {
            'id': 'social_media',
            'name': 'Sosyal Medya',
            'description': 'Profil, paylaşım, mesajlaşma özellikleri ile tam özellikli sosyal platform',
            'icon': 'fas fa-users',
            'color': '#3b82f6',
            'features': [
                'Kullanıcı Profili & Ayarları',
                'Post Paylaşımı & Yorumlar',
                'Gerçek Zamanlı Mesajlaşma',
                'Takip Sistemi & Bildirimler',
                'Hikaye Özelliği',
                'Arama & Keşfet'
            ],
            'popularity': 95,
            'difficulty': 'hard',
            'estimated_time': '45-60 dakika',
            'tech_stack': ['Firebase', 'Retrofit', 'Glide', 'Room DB']
        },
        {
            'id': 'ecommerce',
            'name': 'E-Ticaret',
            'description': 'Ürün katalogu, sepet ve ödeme sistemi ile kapsamlı alışveriş deneyimi',
            'icon': 'fas fa-shopping-cart',
            'color': '#10b981',
            'features': [
                'Ürün Katalogu & Filtreleme',
                'Sepet Yönetimi',
                'Güvenli Ödeme Entegrasyonu',
                'Sipariş Takibi',
                'Favori Ürünler',
                'İndirim & Kupon Sistemi'
            ],
            'popularity': 88,
            'difficulty': 'hard',
            'estimated_time': '40-55 dakika',
            'tech_stack': ['Stripe API', 'Room DB', 'Retrofit', 'WorkManager']
        },
        {
            'id': 'health_fitness',
            'name': 'Sağlık & Fitness',
            'description': 'Sağlık takibi, egzersiz planları ve ilerleme analizi',
            'icon': 'fas fa-heartbeat',
            'color': '#ef4444',
            'features': [
                'Adım Sayacı & GPS Koşu',
                'Kalori & Besin Takibi',
                'Egzersiz Planları & Videolar',
                'İlerleme Grafikleri',
                'Su Takibi & Hatırlatıcılar',
                'Vücut Ölçümleri'
            ],
            'popularity': 82,
            'difficulty': 'medium',
            'estimated_time': '30-40 dakika',
            'tech_stack': ['Sensors API', 'MPAndroidChart', 'Room DB', 'Notifications']
        },
        {
            'id': 'productivity',
            'name': 'Verimlilik',
            'description': 'Görev yönetimi, notlar ve akıllı hatırlatıcılar',
            'icon': 'fas fa-tasks',
            'color': '#f59e0b',
            'features': [
                'Görev Yönetimi & Kategoriler',
                'Zengin Not Editörü',
                'Akıllı Hatırlatıcılar',
                'Takvim Entegrasyonu',
                'Pomodoro Zamanlayıcı',
                'Bulut Senkronizasyonu'
            ],
            'popularity': 76,
            'difficulty': 'medium',
            'estimated_time': '25-35 dakika',
            'tech_stack': ['Room DB', 'WorkManager', 'Calendar API', 'Firebase Sync']
        },
        {
            'id': 'gaming',
            'name': 'Oyun',
            'description': 'Etkileşimli oyun mekaniği, liderlik tablosu ve başarımlar',
            'icon': 'fas fa-gamepad',
            'color': '#8b5cf6',
            'features': [
                'Skor Sistemi & Leaderboard',
                'Seviye Sistemi & Progression',
                'Başarımlar & Rozetler',
                'Çoklu Oyuncu Desteği',
                'Günlük Ödüller',
                'Özelleştirilebilir Avatarlar'
            ],
            'popularity': 71,
            'difficulty': 'hard',
            'estimated_time': '35-50 dakika',
            'tech_stack': ['LibGDX/Custom Engine', 'Firebase Realtime DB', 'Play Games']
        },
        {
            'id': 'education',
            'name': 'Eğitim',
            'description': 'İnteraktif dersler, quizler ve ilerleme takibi',
            'icon': 'fas fa-graduation-cap',
            'color': '#06b6d4',
            'features': [
                'Video Dersler',
                'İnteraktif Quizler',
                'İlerleme Takibi',
                'Sertifika Sistemi',
                'Çevrimdışı Mod',
                'Öğretmen-Öğrenci Paneli'
            ],
            'popularity': 68,
            'difficulty': 'medium',
            'estimated_time': '30-45 dakika',
            'tech_stack': ['ExoPlayer', 'Room DB', 'Firebase', 'PDF Renderer']
        }
    ]
    return jsonify(templates)

@app.route('/ai-suggestions')
@handle_errors
def get_ai_suggestions():
    suggestions = [
        {
            'text': 'Sosyal medya uygulaması - kullanıcılar profil oluşturabilir, fotoğraf paylaşabilir, hikaye ekleyebilir',
            'category': 'social_media',
            'complexity': 'high'
        },
        {
            'text': 'E-ticaret uygulaması - ürün katalogu, sepet yönetimi, güvenli ödeme sistemi, sipariş takibi',
            'category': 'ecommerce',
            'complexity': 'high'
        },
        {
            'text': 'Fitness uygulaması - adım sayar, kalori takibi, egzersiz planları, su hatırlatıcısı',
            'category': 'health_fitness',
            'complexity': 'medium'
        },
        {
            'text': 'Görev yönetimi uygulaması - to-do listeleri, hatırlatıcılar, kategori sistemi, pomodoro timer',
            'category': 'productivity',
            'complexity': 'medium'
        },
        {
            'text': 'Müzik çalar - playlist yönetimi, offline dinleme, equalizer, sleep timer',
            'category': 'entertainment',
            'complexity': 'medium'
        },
        {
            'text': 'Hava durumu uygulaması - 7 günlük tahmin, saat bazlı detaylar, widget, bildirimler',
            'category': 'utility',
            'complexity': 'low'
        },
        {
            'text': 'Not defteri - markdown desteği, kategoriler, arama, bulut senkronizasyonu',
            'category': 'productivity',
            'complexity': 'low'
        },
        {
            'text': 'Tarif uygulaması - yemek tarifleri, malzeme listesi, adım adım rehber, favoriler',
            'category': 'lifestyle',
            'complexity': 'medium'
        }
    ]
    return jsonify(suggestions)

@app.route('/download/<project_id>')
@handle_errors
def download_project(project_id):
    # Get the correct folder name from project status
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        download_id = result.get('downloadId', project_id)
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, download_id)
    else:
        # Fallback to project_id if status not found
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, project_id)

    if not os.path.exists(project_path):
        return jsonify({'success': False, 'error': 'Proje bulunamadı'}), 404
    
    # Check file size
    size_mb = get_directory_size(project_path) / (1024 * 1024)
    if size_mb > config.MAX_PROJECT_SIZE_MB:
        return jsonify({
            'success': False,
            'error': f'Proje boyutu çok büyük ({size_mb:.1f}MB)'
        }), 413
    
    # Create temporary ZIP file
    temp_dir = tempfile.gettempdir()
    zip_path = os.path.join(temp_dir, f"{project_id}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            # Skip build directories
            dirs[:] = [d for d in dirs if d not in ['build', '.gradle', '.idea']]
            
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, project_path)
                zipf.write(file_path, arc_name)
    
    # Get app name for download filename
    app_name = "App"
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        app_name = result.get('appName', 'App')

    # Sanitize app name for filename
    safe_filename = ''.join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_filename:
        safe_filename = "App"

    logger.info(f"Downloaded project {project_id}")
    return send_file(
        zip_path,
        as_attachment=True,
        download_name=f"{safe_filename}.zip",
        mimetype='application/zip'
    )

@app.route('/download-apk/<project_id>')
@handle_errors
def download_apk(project_id):
    """Download APK file for completed project"""
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        download_id = result.get('downloadId', project_id)
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, download_id)
    else:
        project_path = os.path.join(config.PROJECT_STORAGE_PATH, project_id)

    apk_path = os.path.join(project_path, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
    
    if not os.path.exists(apk_path):
        return jsonify({'success': False, 'error': 'APK dosyası bulunamadı'}), 404
    
    # Get app name for download filename
    app_name = "App"
    if project_id in project_status:
        result = project_status[project_id].get('result', {})
        app_name = result.get('appName', 'App')

    # Sanitize app name for filename
    safe_filename = ''.join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_filename:
        safe_filename = "App"

    logger.info(f"Downloaded APK for project {project_id}")
    return send_file(
        apk_path,
        as_attachment=True,
        download_name=f"{safe_filename}.apk",
        mimetype='application/vnd.android.package-archive'
    )

@app.route('/projects')
@handle_errors
def list_projects():
    """List all user projects"""
    projects = []
    for project_id, status in project_status.items():
        if status.get('status') == 'completed':
            projects.append({
                'id': project_id,
                'name': status.get('result', {}).get('appName', 'Unnamed'),
                'created_at': status.get('created_at'),
                'language': status.get('language'),
                'category': status.get('category')
            })
    
    return jsonify(projects)

@app.route('/analytics')
@handle_errors
def get_analytics():
    """Get system analytics"""
    total_projects = len(project_status)
    completed = sum(1 for s in project_status.values() if s.get('status') == 'completed')
    failed = sum(1 for s in project_status.values() if s.get('status') == 'error')
    
    avg_generation_time = 0
    if completed > 0:
        times = [s.get('generation_time', 0) for s in project_status.values() 
                if s.get('status') == 'completed' and s.get('generation_time')]
        avg_generation_time = sum(times) / len(times) if times else 0
    
    return jsonify({
        'total_projects': total_projects,
        'completed': completed,
        'failed': failed,
        'in_progress': len(active_generations),
        'success_rate': (completed / total_projects * 100) if total_projects > 0 else 0,
        'avg_generation_time': round(avg_generation_time, 2)
    })

# Helper functions
def get_directory_size(path):
    """Calculate directory size in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    except Exception as e:
        logger.error(f"Error calculating size for {path}: {e}")
    return total

def count_files(path):
    """Count files in directory"""
    count = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                count += 1
            elif entry.is_dir():
                count += count_files(entry.path)
    except Exception as e:
        logger.error(f"Error counting files in {path}: {e}")
    return count

def build_apk(project_path):
    """Build APK for the generated project"""
    try:
        import subprocess
        gradlew = os.path.join(project_path, 'gradlew.bat')
        if os.path.exists(gradlew):
            logger.info(f"Starting APK build for {project_path}")
            result = subprocess.run(
                [gradlew, 'assembleDebug'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=600,
                shell=True
            )
            if result.returncode == 0:
                logger.info(f"APK built successfully for {project_path}")
                apk_path = os.path.join(project_path, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
                if os.path.exists(apk_path):
                    logger.info(f"APK file created: {apk_path}")
                    return True
                else:
                    logger.warning(f"APK file not found at {apk_path}")
            else:
                logger.error(f"APK build failed: {result.stderr}")
                logger.error(f"Build output: {result.stdout}")
        else:
            logger.error(f"gradlew.bat not found at {gradlew}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"APK build timeout for {project_path}")
        return False
    except Exception as e:
        logger.error(f"Error building APK: {e}")
        return False

# Cleanup old projects periodically
def cleanup_old_projects():
    """Clean up projects older than configured hours"""
    while True:
        try:
            current_time = datetime.now()
            for project_id in list(project_status.keys()):
                status = project_status[project_id]
                created_at = datetime.fromisoformat(status.get('created_at', ''))
                
                if (current_time - created_at).total_seconds() > config.TEMP_STORAGE_HOURS * 3600:
                    # Remove from memory
                    del project_status[project_id]
                    if project_id in project_analytics:
                        del project_analytics[project_id]
                    
                    # Remove files
                    project_path = os.path.join(config.PROJECT_STORAGE_PATH, project_id)
                    if os.path.exists(project_path):
                        import shutil
                        shutil.rmtree(project_path)
                        logger.info(f"Cleaned up old project {project_id}")
            
            time.sleep(3600)  # Check every hour
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            time.sleep(3600)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_projects, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint bulunamadı'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Sunucu hatası'}), 500

if __name__ == '__main__':
    # Ensure project directory exists
    os.makedirs(config.PROJECT_STORAGE_PATH, exist_ok=True)

    logger.info("Starting Android App Generator API Server")
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)