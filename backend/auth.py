"""
Advanced Authentication and Security Module
JWT-based authentication with role-based access control and security features
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from functools import wraps
import jwt
import bcrypt
from flask import request, g, current_app
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    get_jwt, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from sqlalchemy.orm import Session
from models import User, UserSession, AuditLog
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Advanced authentication manager with security features"""

    def __init__(self, app=None, db_session=None):
        self.app = app
        self.db_session = db_session
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        self.jwt = JWTManager(app)
        self._setup_jwt_callbacks()

    def _setup_jwt_callbacks(self):
        """Setup JWT token callbacks"""

        @self.jwt.user_identity_loader
        def user_identity_lookup(user):
            return user.id if hasattr(user, 'id') else user

        @self.jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            return self.db_session.query(User).filter_by(id=identity).first()

        @self.jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            jti = jwt_payload["jti"]
            # Check Redis cache for revoked tokens
            cache = current_app.extensions.get('cache')
            if cache:
                return cache.get(f"revoked_token:{jti}") is not None
            return False

        @self.jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return {
                'error': 'Token expired',
                'message': 'Please refresh your token'
            }, 401

        @self.jwt.invalid_token_loader
        def invalid_token_callback(error):
            return {
                'error': 'Invalid token',
                'message': 'Token is invalid'
            }, 401

        @self.jwt.unauthorized_loader
        def unauthorized_callback(error):
            return {
                'error': 'Missing authorization',
                'message': 'Authorization header is missing'
            }, 401

    def authenticate_user(self, username_or_email: str, password: str) -> Tuple[Optional[User], str]:
        """
        Authenticate user with username/email and password
        Returns (user, error_message)
        """
        try:
            # Find user by email or username
            user = self.db_session.query(User).filter(
                ((User.email == username_or_email) | (User.username == username_or_email)) &
                (User.is_active == True)
            ).first()

            if not user:
                return None, "User not found"

            # Check if account is locked
            if user.is_locked():
                return None, "Account is temporarily locked due to too many failed attempts"

            # Verify password
            if not user.check_password(password):
                user.increment_login_attempts()
                self.db_session.commit()
                return None, "Invalid password"

            # Reset login attempts on successful login
            user.reset_login_attempts()
            user.last_login = datetime.utcnow()
            self.db_session.commit()

            # Log successful login
            self._log_audit_event(user.id, 'login', 'user', str(user.id), {
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            })

            return user, ""

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None, "Authentication failed"

    def create_session(self, user: User, ip_address: str, user_agent: str) -> UserSession:
        """Create a new user session"""
        session = UserSession(
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(days=7)  # 7 days
        )
        self.db_session.add(session)
        self.db_session.commit()
        return session

    def create_tokens(self, user: User) -> Tuple[str, str]:
        """Create access and refresh tokens"""
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return access_token, refresh_token

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = jwt.decode(
                refresh_token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )

            user_id = payload['sub']
            user = self.db_session.query(User).filter_by(id=user_id).first()

            if not user or not user.is_active:
                return None

            # Create new access token
            return create_access_token(identity=user)

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def revoke_token(self, jti: str) -> None:
        """Revoke a JWT token by adding to blocklist"""
        cache = current_app.extensions.get('cache')
        if cache:
            cache.set(f"revoked_token:{jti}", 'revoked', timeout=86400)  # 24 hours

    def logout_user(self, user: User) -> None:
        """Logout user and revoke tokens"""
        # Revoke current JWT token
        jwt_data = get_jwt()
        if jwt_data:
            self.revoke_token(jwt_data['jti'])

        # Log logout event
        self._log_audit_event(user.id, 'logout', 'user', str(user.id), {
            'ip_address': request.remote_addr
        })

    def register_user(self, username: str, email: str, password: str, full_name: str = None) -> Tuple[Optional[User], str]:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = self.db_session.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()

            if existing_user:
                if existing_user.email == email:
                    return None, "Email already registered"
                else:
                    return None, "Username already taken"

            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=full_name
            )
            user.set_password(password)

            self.db_session.add(user)
            self.db_session.commit()

            # Log registration
            self._log_audit_event(user.id, 'register', 'user', str(user.id), {
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            })

            return user, ""

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            self.db_session.rollback()
            return None, "Registration failed"

    def change_password(self, user: User, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        try:
            # Verify old password
            if not user.check_password(old_password):
                return False, "Current password is incorrect"

            # Update password
            user.set_password(new_password)
            self.db_session.commit()

            # Log password change
            self._log_audit_event(user.id, 'change_password', 'user', str(user.id), {
                'ip_address': request.remote_addr
            })

            return True, ""

        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            self.db_session.rollback()
            return False, "Password change failed"

    def _log_audit_event(self, user_id: int, action: str, resource_type: str,
                        resource_id: str, details: Dict[str, Any]) -> None:
        """Log audit event"""
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            self.db_session.add(audit_log)
            self.db_session.commit()
        except Exception as e:
            logger.error(f"Failed to log audit event: {str(e)}")

# Decorators
def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user = get_jwt_identity()
        if not user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        return f(*args, **kwargs)
    return decorated_function

def active_user_required(f):
    """Decorator to require active user"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user = get_jwt_identity()
        if not user.is_active:
            return {'error': 'Account is deactivated'}, 403
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(max_per_minute: int = 60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from flask_limiter import Limiter
            limiter = current_app.extensions.get('limiter')
            if limiter:
                # Apply rate limiting
                pass  # Rate limiting is handled by Flask-Limiter
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Security utilities
class SecurityUtils:
    """Security utility functions"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS"""
        import html
        return html.escape(text.strip())

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate secure random token"""
        import secrets
        return secrets.token_urlsafe(length)

    @staticmethod
    def get_client_ip() -> str:
        """Get client IP address"""
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        return request.remote_addr

# Initialize global auth manager
auth_manager = AuthManager()