"""
Real-time Processing Module
WebSocket support for live updates, notifications, and collaborative features
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from threading import Lock
import logging
from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
import eventlet

logger = logging.getLogger(__name__)

class RealtimeManager:
    """Real-time communication manager using Socket.IO"""

    def __init__(self, app=None, cors_allowed_origins="*"):
        self.app = app
        self.socketio = None
        self.connected_clients: Dict[str, Dict[str, Any]] = {}
        self.project_rooms: Dict[str, List[str]] = {}
        self.client_lock = Lock()

        if app:
            self.init_app(app, cors_allowed_origins)

    def init_app(self, app, cors_allowed_origins="*"):
        """Initialize with Flask app"""
        self.socketio = SocketIO(
            app,
            cors_allowed_origins=cors_allowed_origins,
            async_mode='eventlet',
            logger=True,
            engineio_logger=True
        )

        # Register event handlers
        self._register_handlers()

        logger.info("Real-time manager initialized")

    def _register_handlers(self):
        """Register Socket.IO event handlers"""

        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            try:
                token = request.args.get('token')
                if not token:
                    logger.warning("Connection attempt without token")
                    disconnect()
                    return False

                # Verify JWT token
                try:
                    payload = decode_token(token)
                    user_id = payload['sub']
                except Exception as e:
                    logger.error(f"Invalid token: {str(e)}")
                    disconnect()
                    return False

                client_id = request.sid
                with self.client_lock:
                    self.connected_clients[client_id] = {
                        'user_id': user_id,
                        'connected_at': datetime.utcnow(),
                        'rooms': []
                    }

                logger.info(f"Client {client_id} connected for user {user_id}")
                emit('connected', {'status': 'success', 'client_id': client_id})

            except Exception as e:
                logger.error(f"Connection error: {str(e)}")
                disconnect()
                return False

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            client_id = request.sid
            with self.client_lock:
                if client_id in self.connected_clients:
                    user_id = self.connected_clients[client_id]['user_id']
                    rooms = self.connected_clients[client_id]['rooms']

                    # Leave all rooms
                    for room in rooms:
                        leave_room(room)
                        self._remove_from_room(room, client_id)

                    del self.connected_clients[client_id]

                    logger.info(f"Client {client_id} disconnected (user {user_id})")

        @self.socketio.on('join_project')
        def handle_join_project(data):
            """Join project room for real-time updates"""
            try:
                project_id = data.get('project_id')
                if not project_id:
                    emit('error', {'message': 'Project ID required'})
                    return

                client_id = request.sid
                with self.client_lock:
                    if client_id not in self.connected_clients:
                        emit('error', {'message': 'Not authenticated'})
                        return

                    join_room(project_id)
                    self.connected_clients[client_id]['rooms'].append(project_id)
                    self._add_to_room(project_id, client_id)

                logger.info(f"Client {client_id} joined project {project_id}")
                emit('joined_project', {'project_id': project_id})

            except Exception as e:
                logger.error(f"Join project error: {str(e)}")
                emit('error', {'message': 'Failed to join project'})

        @self.socketio.on('leave_project')
        def handle_leave_project(data):
            """Leave project room"""
            try:
                project_id = data.get('project_id')
                if not project_id:
                    return

                client_id = request.sid
                with self.client_lock:
                    if client_id in self.connected_clients:
                        if project_id in self.connected_clients[client_id]['rooms']:
                            leave_room(project_id)
                            self.connected_clients[client_id]['rooms'].remove(project_id)
                            self._remove_from_room(project_id, client_id)

                logger.info(f"Client {client_id} left project {project_id}")

            except Exception as e:
                logger.error(f"Leave project error: {str(e)}")

        @self.socketio.on('project_update')
        def handle_project_update(data):
            """Handle project update notifications"""
            try:
                project_id = data.get('project_id')
                update_type = data.get('type', 'general')
                update_data = data.get('data', {})

                # Broadcast to project room
                self.broadcast_to_project(project_id, 'project_updated', {
                    'type': update_type,
                    'data': update_data,
                    'timestamp': datetime.utcnow().isoformat()
                })

            except Exception as e:
                logger.error(f"Project update error: {str(e)}")

        @self.socketio.on('ping')
        def handle_ping():
            """Handle ping for connection health check"""
            emit('pong', {'timestamp': datetime.utcnow().isoformat()})

    def _add_to_room(self, room: str, client_id: str):
        """Add client to room tracking"""
        if room not in self.project_rooms:
            self.project_rooms[room] = []
        if client_id not in self.project_rooms[room]:
            self.project_rooms[room].append(client_id)

    def _remove_from_room(self, room: str, client_id: str):
        """Remove client from room tracking"""
        if room in self.project_rooms:
            if client_id in self.project_rooms[room]:
                self.project_rooms[room].remove(client_id)
            if not self.project_rooms[room]:
                del self.project_rooms[room]

    def broadcast_to_project(self, project_id: str, event: str, data: Dict[str, Any]):
        """Broadcast event to all clients in project room"""
        try:
            self.socketio.emit(event, data, room=project_id)
            logger.debug(f"Broadcasted {event} to project {project_id}")
        except Exception as e:
            logger.error(f"Broadcast error: {str(e)}")

    def send_to_user(self, user_id: int, event: str, data: Dict[str, Any]):
        """Send event to specific user"""
        try:
            with self.client_lock:
                for client_id, client_info in self.connected_clients.items():
                    if client_info['user_id'] == user_id:
                        self.socketio.emit(event, data, room=client_id)
                        logger.debug(f"Sent {event} to user {user_id}")
        except Exception as e:
            logger.error(f"Send to user error: {str(e)}")

    def notify_project_progress(self, project_id: str, progress: float, status: str, step: str):
        """Notify project progress to all subscribers"""
        self.broadcast_to_project(project_id, 'progress_update', {
            'progress': progress,
            'status': status,
            'current_step': step,
            'timestamp': datetime.utcnow().isoformat()
        })

    def notify_generation_complete(self, project_id: str, result: Dict[str, Any]):
        """Notify generation completion"""
        self.broadcast_to_project(project_id, 'generation_complete', {
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })

    def get_room_clients(self, room: str) -> List[str]:
        """Get all clients in a room"""
        return self.project_rooms.get(room, [])

    def get_connected_clients_count(self) -> int:
        """Get total connected clients"""
        with self.client_lock:
            return len(self.connected_clients)

    def get_project_subscribers_count(self, project_id: str) -> int:
        """Get number of subscribers for a project"""
        return len(self.get_room_clients(project_id))

class NotificationManager:
    """Notification management system"""

    def __init__(self, realtime_manager: RealtimeManager = None):
        self.realtime = realtime_manager
        self.notifications: Dict[str, List[Dict[str, Any]]] = {}
        self.notification_lock = Lock()

    def create_notification(self, user_id: int, title: str, message: str,
                          notification_type: str = 'info',
                          data: Dict[str, Any] = None) -> str:
        """Create a new notification"""
        notification_id = f"notif_{int(time.time())}_{user_id}"

        notification = {
            'id': notification_id,
            'user_id': user_id,
            'title': title,
            'message': message,
            'type': notification_type,
            'data': data or {},
            'read': False,
            'created_at': datetime.utcnow().isoformat()
        }

        with self.notification_lock:
            if str(user_id) not in self.notifications:
                self.notifications[str(user_id)] = []
            self.notifications[str(user_id)].append(notification)

        # Send real-time notification if manager available
        if self.realtime:
            self.realtime.send_to_user(user_id, 'notification', notification)

        logger.info(f"Created notification for user {user_id}: {title}")
        return notification_id

    def get_user_notifications(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get notifications for user"""
        with self.notification_lock:
            user_notifications = self.notifications.get(str(user_id), [])
            return sorted(user_notifications, key=lambda x: x['created_at'], reverse=True)[:limit]

    def mark_as_read(self, user_id: int, notification_id: str) -> bool:
        """Mark notification as read"""
        with self.notification_lock:
            user_notifications = self.notifications.get(str(user_id), [])
            for notification in user_notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    return True
        return False

    def delete_notification(self, user_id: int, notification_id: str) -> bool:
        """Delete notification"""
        with self.notification_lock:
            user_notifications = self.notifications.get(str(user_id), [])
            for i, notification in enumerate(user_notifications):
                if notification['id'] == notification_id:
                    del user_notifications[i]
                    return True
        return False

    def get_unread_count(self, user_id: int) -> int:
        """Get unread notification count"""
        with self.notification_lock:
            user_notifications = self.notifications.get(str(user_id), [])
            return sum(1 for n in user_notifications if not n['read'])

class CollaborativeEditing:
    """Collaborative editing support"""

    def __init__(self, realtime_manager: RealtimeManager = None):
        self.realtime = realtime_manager
        self.active_edits: Dict[str, Dict[str, Any]] = {}
        self.edit_lock = Lock()

    def start_editing(self, project_id: str, user_id: int, file_path: str) -> bool:
        """Start collaborative editing session"""
        edit_key = f"{project_id}:{file_path}"

        with self.edit_lock:
            if edit_key in self.active_edits:
                current_editor = self.active_edits[edit_key]['user_id']
                if current_editor != user_id:
                    return False  # Someone else is editing

            self.active_edits[edit_key] = {
                'user_id': user_id,
                'started_at': datetime.utcnow(),
                'last_activity': datetime.utcnow()
            }

        # Notify other users
        if self.realtime:
            self.realtime.broadcast_to_project(project_id, 'editing_started', {
                'file_path': file_path,
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat()
            })

        return True

    def update_edit(self, project_id: str, user_id: int, file_path: str,
                   changes: Dict[str, Any]):
        """Update collaborative edit"""
        edit_key = f"{project_id}:{file_path}"

        with self.edit_lock:
            if edit_key in self.active_edits:
                self.active_edits[edit_key]['last_activity'] = datetime.utcnow()

        # Broadcast changes to other users
        if self.realtime:
            self.realtime.broadcast_to_project(project_id, 'edit_update', {
                'file_path': file_path,
                'user_id': user_id,
                'changes': changes,
                'timestamp': datetime.utcnow().isoformat()
            })

    def stop_editing(self, project_id: str, user_id: int, file_path: str):
        """Stop collaborative editing session"""
        edit_key = f"{project_id}:{file_path}"

        with self.edit_lock:
            if edit_key in self.active_edits:
                del self.active_edits[edit_key]

        # Notify other users
        if self.realtime:
            self.realtime.broadcast_to_project(project_id, 'editing_stopped', {
                'file_path': file_path,
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat()
            })

    def get_active_editors(self, project_id: str) -> Dict[str, int]:
        """Get active editors for project"""
        active_editors = {}
        with self.edit_lock:
            for edit_key, edit_info in self.active_edits.items():
                if edit_key.startswith(f"{project_id}:"):
                    file_path = edit_key.split(':', 1)[1]
                    active_editors[file_path] = edit_info['user_id']
        return active_editors

# Global instances
realtime_manager = RealtimeManager()
notification_manager = NotificationManager(realtime_manager)
collaborative_editing = CollaborativeEditing(realtime_manager)

# Utility functions
def emit_project_update(project_id: str, update_type: str, data: Dict[str, Any]):
    """Emit project update to all subscribers"""
    if realtime_manager:
        realtime_manager.broadcast_to_project(project_id, 'project_update', {
            'type': update_type,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        })

def emit_user_notification(user_id: int, title: str, message: str,
                          notification_type: str = 'info'):
    """Send notification to user"""
    if notification_manager:
        notification_manager.create_notification(user_id, title, message, notification_type)

def get_connection_stats() -> Dict[str, Any]:
    """Get real-time connection statistics"""
    if realtime_manager:
        return {
            'connected_clients': realtime_manager.get_connected_clients_count(),
            'active_projects': len(realtime_manager.project_rooms),
            'total_subscribers': sum(len(clients) for clients in realtime_manager.project_rooms.values())
        }
    return {'error': 'Real-time manager not initialized'}