"""
Database Models for Android App Generator
Comprehensive data models with relationships, validation, and performance optimizations
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
import json

Base = declarative_base()

class User(Base):
    """User model with authentication and profile management"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(200))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)

    # Relationships
    projects = relationship('Project', back_populates='user', cascade='all, delete-orphan')
    api_keys = relationship('APIKey', back_populates='user', cascade='all, delete-orphan')
    sessions = relationship('UserSession', back_populates='user', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_created', 'created_at'),
    )

    def set_password(self, password: str) -> None:
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def is_locked(self) -> bool:
        """Check if account is locked"""
        return self.locked_until and self.locked_until > datetime.utcnow()

    def increment_login_attempts(self) -> None:
        """Increment failed login attempts"""
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)

    def reset_login_attempts(self) -> None:
        """Reset login attempts on successful login"""
        self.login_attempts = 0
        self.locked_until = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class APIKey(Base):
    """API Key model for external integrations"""
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(256), nullable=False)
    permissions = Column(JSON, default=list)  # List of permissions
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    expires_at = Column(DateTime)

    # Relationships
    user = relationship('User', back_populates='api_keys')

    __table_args__ = (
        Index('idx_api_key_user', 'user_id', 'is_active'),
        Index('idx_api_key_expires', 'expires_at'),
    )

    def is_expired(self) -> bool:
        """Check if API key is expired"""
        return self.expires_at and self.expires_at < datetime.utcnow()

class UserSession(Base):
    """User session tracking"""
    __tablename__ = 'user_sessions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ip_address = Column(String(45))  # IPv6 support
    user_agent = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship('User', back_populates='sessions')

    __table_args__ = (
        Index('idx_session_user', 'user_id', 'is_active'),
        Index('idx_session_expires', 'expires_at'),
    )

    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at

    def update_activity(self) -> None:
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()

class Project(Base):
    """Project model for generated Android applications"""
    __tablename__ = 'projects'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    language = Column(String(20), default='java')  # java, kotlin
    theme = Column(String(20), default='light')  # light, dark, auto
    status = Column(String(20), default='queued')  # queued, processing, completed, failed
    progress = Column(Float, default=0.0)
    app_name = Column(String(200))
    package_name = Column(String(300))
    project_path = Column(String(500))
    download_url = Column(String(500))
    file_size = Column(Integer)  # Size in bytes
    build_time = Column(Float)  # Build time in seconds
    error_message = Column(Text)
    project_metadata = Column(JSON)  # Additional project metadata
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship('User', back_populates='projects')
    features = relationship('ProjectFeature', back_populates='project', cascade='all, delete-orphan')
    activities = relationship('ProjectActivity', back_populates='project', cascade='all, delete-orphan')
    dependencies = relationship('ProjectDependency', back_populates='project', cascade='all, delete-orphan')
    analytics = relationship('ProjectAnalytics', back_populates='project', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_project_user', 'user_id', 'created_at'),
        Index('idx_project_status', 'status', 'created_at'),
        Index('idx_project_category', 'category'),
    )

    @validates('progress')
    def validate_progress(self, key, value):
        """Validate progress is between 0 and 100"""
        if not (0 <= value <= 100):
            raise ValueError('Progress must be between 0 and 100')
        return value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'language': self.language,
            'theme': self.theme,
            'status': self.status,
            'progress': self.progress,
            'app_name': self.app_name,
            'package_name': self.package_name,
            'file_size': self.file_size,
            'build_time': self.build_time,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.project_metadata or {}
        }

class ProjectFeature(Base):
    """Features associated with a project"""
    __tablename__ = 'project_features'

    id = Column(Integer, primary_key=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # ui, backend, security, etc.
    complexity = Column(String(20))  # low, medium, high
    is_implemented = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship('Project', back_populates='features')

    __table_args__ = (
        Index('idx_feature_project', 'project_id', 'is_implemented'),
    )

class ProjectActivity(Base):
    """Activities/screens in the project"""
    __tablename__ = 'project_activities'

    id = Column(Integer, primary_key=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(50))  # activity, fragment, service, etc.
    description = Column(Text)
    layout_file = Column(String(200))
    is_main = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship('Project', back_populates='activities')

    __table_args__ = (
        Index('idx_activity_project', 'project_id', 'type'),
    )

class ProjectDependency(Base):
    """Dependencies/libraries used in the project"""
    __tablename__ = 'project_dependencies'

    id = Column(Integer, primary_key=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    name = Column(String(200), nullable=False)
    version = Column(String(50))
    type = Column(String(50))  # implementation, testImplementation, etc.
    description = Column(Text)
    is_optional = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship('Project', back_populates='dependencies')

    __table_args__ = (
        Index('idx_dependency_project', 'project_id', 'type'),
    )

class ProjectAnalytics(Base):
    """Analytics data for project generation"""
    __tablename__ = 'project_analytics'

    id = Column(Integer, primary_key=True)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    event_type = Column(String(50), nullable=False)  # start, progress, complete, error
    event_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)  # Duration in seconds
    memory_usage = Column(Float)  # Memory usage in MB
    cpu_usage = Column(Float)  # CPU usage percentage

    # Relationships
    project = relationship('Project', back_populates='analytics')

    __table_args__ = (
        Index('idx_analytics_project', 'project_id', 'event_type', 'timestamp'),
    )

class SystemMetrics(Base):
    """System-wide metrics and analytics"""
    __tablename__ = 'system_metrics'

    id = Column(Integer, primary_key=True)
    metric_type = Column(String(50), nullable=False)  # cpu, memory, requests, etc.
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(20))  # %, MB, requests/min, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    metric_metadata = Column(JSON)

    __table_args__ = (
        Index('idx_metrics_type_time', 'metric_type', 'timestamp'),
        Index('idx_metrics_name_time', 'metric_name', 'timestamp'),
    )

class BackgroundTask(Base):
    """Background task tracking"""
    __tablename__ = 'background_tasks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_type = Column(String(50), nullable=False)  # generate_app, cleanup, backup, etc.
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    priority = Column(Integer, default=0)  # Higher number = higher priority
    payload = Column(JSON)  # Task parameters
    result = Column(JSON)  # Task result
    error_message = Column(Text)
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    __table_args__ = (
        Index('idx_task_type_status', 'task_type', 'status'),
        Index('idx_task_priority', 'priority', 'created_at'),
    )

    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries

class AuditLog(Base):
    """Audit logging for security and compliance"""
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)  # create_project, delete_project, login, etc.
    resource_type = Column(String(50))  # project, user, api_key, etc.
    resource_id = Column(String(36))  # ID of the affected resource
    details = Column(JSON)  # Additional details about the action
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)

    # Relationships
    user = relationship('User')

    __table_args__ = (
        Index('idx_audit_user_time', 'user_id', 'timestamp'),
        Index('idx_audit_action_time', 'action', 'timestamp'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )

# Utility functions
def create_tables(engine):
    """Create all database tables"""
    Base.metadata.create_all(engine)

def drop_tables(engine):
    """Drop all database tables"""
    Base.metadata.drop_all(engine)

def get_user_by_email(session, email: str) -> Optional[User]:
    """Get user by email address"""
    return session.query(User).filter_by(email=email, is_active=True).first()

def get_user_by_username(session, username: str) -> Optional[User]:
    """Get user by username"""
    return session.query(User).filter_by(username=username, is_active=True).first()

def get_project_by_id(session, project_id: str) -> Optional[Project]:
    """Get project by ID"""
    return session.query(Project).filter_by(id=project_id).first()

def get_active_sessions_count(session, user_id: int) -> int:
    """Get count of active sessions for user"""
    return session.query(UserSession).filter_by(
        user_id=user_id,
        is_active=True
    ).count()

def cleanup_expired_sessions(session) -> int:
    """Clean up expired sessions, return count of deleted sessions"""
    deleted_count = session.query(UserSession).filter(
        UserSession.expires_at < datetime.utcnow()
    ).delete()
    session.commit()
    return deleted_count