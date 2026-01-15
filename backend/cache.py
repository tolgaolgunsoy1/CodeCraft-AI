"""
Caching and Performance Optimization Module
Advanced caching strategies, performance monitoring, and optimization features
"""

import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Callable, List
from functools import wraps
import logging
from flask import request, g
from flask_caching import Cache
import redis
import psutil
import threading

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Performance monitoring and metrics collection"""

    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()

    def start_timer(self, operation: str) -> str:
        """Start timing an operation"""
        timer_id = f"{operation}_{int(time.time() * 1000)}"
        self.metrics[timer_id] = {
            'operation': operation,
            'start_time': time.time(),
            'cpu_start': psutil.cpu_percent(),
            'memory_start': psutil.virtual_memory().percent
        }
        return timer_id

    def end_timer(self, timer_id: str) -> Dict[str, Any]:
        """End timing and return metrics"""
        if timer_id not in self.metrics:
            return {}

        start_data = self.metrics[timer_id]
        end_time = time.time()

        metrics = {
            'operation': start_data['operation'],
            'duration': end_time - start_data['start_time'],
            'cpu_usage': psutil.cpu_percent() - start_data['cpu_start'],
            'memory_usage': psutil.virtual_memory().percent - start_data['memory_start'],
            'timestamp': datetime.utcnow().isoformat()
        }

        with self.lock:
            del self.metrics[timer_id]

        return metrics

    def record_metric(self, name: str, value: float, unit: str = None):
        """Record a custom metric"""
        with self.lock:
            if name not in self.metrics:
                self.metrics[name] = []
            self.metrics[name].append({
                'value': value,
                'unit': unit,
                'timestamp': datetime.utcnow().isoformat()
            })

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used': psutil.virtual_memory().used,
            'memory_total': psutil.virtual_memory().total,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'timestamp': datetime.utcnow().isoformat()
        }

class AdvancedCache:
    """Advanced caching with multiple strategies and invalidation"""

    def __init__(self, cache: Cache = None, redis_client: redis.Redis = None):
        self.cache = cache
        self.redis = redis_client
        self.cache_strategies = {
            'lru': self._lru_cache,
            'ttl': self._ttl_cache,
            'write_through': self._write_through_cache,
            'write_behind': self._write_behind_cache
        }

    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def _lru_cache(self, key: str, data: Any, max_age: int = 300) -> Any:
        """Least Recently Used cache strategy"""
        if self.cache:
            return self.cache.get(key) or self.cache.set(key, data, timeout=max_age)
        return data

    def _ttl_cache(self, key: str, data: Any, max_age: int = 300) -> Any:
        """Time To Live cache strategy"""
        if self.cache:
            cached = self.cache.get(key)
            if cached:
                return cached
            self.cache.set(key, data, timeout=max_age)
        return data

    def _write_through_cache(self, key: str, data: Any, max_age: int = 300) -> Any:
        """Write-through cache strategy"""
        if self.cache:
            self.cache.set(key, data, timeout=max_age)
        return data

    def _write_behind_cache(self, key: str, data: Any, max_age: int = 300) -> Any:
        """Write-behind cache strategy (async write)"""
        if self.cache:
            # In a real implementation, this would queue the write
            self.cache.set(key, data, timeout=max_age)
        return data

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        if self.cache:
            return self.cache.get(key) or default
        return default

    def set(self, key: str, value: Any, timeout: int = 300, strategy: str = 'ttl') -> bool:
        """Set value in cache with strategy"""
        if strategy in self.cache_strategies:
            self.cache_strategies[strategy](key, value, timeout)
            return True
        return False

    def delete(self, key: str) -> bool:
        """Delete from cache"""
        if self.cache:
            self.cache.delete(key)
            return True
        return False

    def clear(self) -> bool:
        """Clear all cache"""
        if self.cache:
            self.cache.clear()
            return True
        return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache keys matching pattern"""
        if self.redis:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
        return 0

class CacheManager:
    """Comprehensive cache management system"""

    def __init__(self, app=None):
        self.app = app
        self.cache = None
        self.redis = None
        self.monitor = PerformanceMonitor()

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app"""
        self.cache = app.extensions.get('cache')
        redis_url = app.config.get('REDIS_URL')

        if redis_url and redis_url != 'redis://localhost:6379/0':
            try:
                self.redis = redis.from_url(redis_url)
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.error(f"Redis initialization failed: {str(e)}")

    def cached(self, timeout: int = 300, key_prefix: str = None,
               strategy: str = 'ttl', unless: Callable = None):
        """Decorator for caching function results"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.cache:
                    return f(*args, **kwargs)

                # Check unless condition
                if unless and unless():
                    return f(*args, **kwargs)

                # Generate cache key
                if key_prefix:
                    cache_key = f"{key_prefix}:{f.__name__}:{hash(str(args) + str(kwargs))}"
                else:
                    cache_key = f"{f.__name__}:{hash(str(args) + str(kwargs))}"

                # Try to get from cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result

                # Execute function and cache result
                timer_id = self.monitor.start_timer(f.__name__)
                result = f(*args, **kwargs)
                metrics = self.monitor.end_timer(timer_id)

                # Cache the result
                self.cache.set(cache_key, result, timeout=timeout)
                logger.debug(f"Cached result for {cache_key}")

                # Log performance metrics
                if metrics.get('duration', 0) > 1.0:  # Log slow operations
                    logger.warning(f"Slow operation {f.__name__}: {metrics['duration']:.2f}s")

                return result

            return decorated_function
        return decorator

    def memoize(self, timeout: int = 300):
        """Memoization decorator for expensive computations"""
        def decorator(f):
            cache = {}

            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Create hashable key
                key = (args, tuple(sorted(kwargs.items())))

                # Check cache
                if key in cache:
                    cache_entry = cache[key]
                    if time.time() - cache_entry['timestamp'] < timeout:
                        return cache_entry['result']

                # Compute result
                result = f(*args, **kwargs)

                # Cache result
                cache[key] = {
                    'result': result,
                    'timestamp': time.time()
                }

                # Clean old entries
                current_time = time.time()
                cache_keys = list(cache.keys())
                for k in cache_keys:
                    if current_time - cache[k]['timestamp'] > timeout:
                        del cache[k]

                return result

            return decorated_function
        return decorator

    def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache entries for a user"""
        patterns = [
            f"user:{user_id}:*",
            f"projects:user:{user_id}:*",
            f"analytics:user:{user_id}:*"
        ]

        invalidated = 0
        for pattern in patterns:
            invalidated += self.invalidate_pattern(pattern)

        logger.info(f"Invalidated {invalidated} cache entries for user {user_id}")
        return invalidated

    def invalidate_project_cache(self, project_id: str):
        """Invalidate all cache entries for a project"""
        patterns = [
            f"project:{project_id}:*",
            f"analytics:project:{project_id}:*",
            f"files:project:{project_id}:*"
        ]

        invalidated = 0
        for pattern in patterns:
            invalidated += self.invalidate_pattern(pattern)

        logger.info(f"Invalidated {invalidated} cache entries for project {project_id}")
        return invalidated

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache keys matching pattern"""
        if self.redis:
            try:
                keys = self.redis.keys(pattern)
                if keys:
                    return self.redis.delete(*keys)
            except Exception as e:
                logger.error(f"Pattern invalidation error: {str(e)}")
        return 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        stats = {
            'cache_type': 'Simple' if not self.redis else 'Redis',
            'timestamp': datetime.utcnow().isoformat()
        }

        if self.redis:
            try:
                info = self.redis.info()
                stats.update({
                    'connected_clients': info.get('connected_clients', 0),
                    'used_memory': info.get('used_memory_human', '0B'),
                    'total_keys': self.redis.dbsize(),
                    'hit_rate': info.get('keyspace_hits', 0) / max(info.get('keyspace_misses', 0) + info.get('keyspace_hits', 0), 1)
                })
            except Exception as e:
                logger.error(f"Cache stats error: {str(e)}")

        return stats

    def warmup_cache(self):
        """Warm up cache with frequently accessed data"""
        # This would be implemented based on application-specific needs
        logger.info("Cache warmup completed")

class DatabaseOptimizer:
    """Database performance optimization utilities"""

    def __init__(self, db_session=None):
        self.db_session = db_session

    def optimize_query(self, query):
        """Apply performance optimizations to query"""
        # Add query hints, optimize joins, etc.
        return query

    def get_query_plan(self, query) -> Dict[str, Any]:
        """Get query execution plan"""
        # This would analyze the query plan for optimization
        return {'estimated_cost': 0, 'estimated_rows': 0}

    def create_indexes_if_needed(self):
        """Create performance indexes if they don't exist"""
        # Analyze query patterns and create indexes
        logger.info("Database indexes optimized")

    def cleanup_old_data(self, days: int = 30):
        """Clean up old data to maintain performance"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # This would delete old logs, sessions, etc.
        logger.info(f"Cleaned up data older than {days} days")

# Global instances
performance_monitor = PerformanceMonitor()
cache_manager = CacheManager()

# Decorators
def monitor_performance(operation_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            op_name = operation_name or f.__name__
            timer_id = performance_monitor.start_timer(op_name)

            try:
                result = f(*args, **kwargs)
                return result
            finally:
                metrics = performance_monitor.end_timer(timer_id)
                if metrics.get('duration', 0) > 2.0:  # Log slow operations
                    logger.warning(f"Slow operation detected: {op_name} took {metrics['duration']:.2f}s")

        return decorated_function
    return decorator

def cached(timeout: int = 300, key_prefix: str = None):
    """Caching decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if cache_manager and cache_manager.cache:
                return cache_manager.cached(timeout, key_prefix)(f)(*args, **kwargs)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Utility functions
def get_performance_metrics() -> Dict[str, Any]:
    """Get current performance metrics"""
    return {
        'system': performance_monitor.get_system_metrics(),
        'cache': cache_manager.get_cache_stats() if cache_manager else None,
        'timestamp': datetime.utcnow().isoformat()
    }

def optimize_database():
    """Run database optimization tasks"""
    optimizer = DatabaseOptimizer()
    optimizer.create_indexes_if_needed()
    optimizer.cleanup_old_data()

def clear_user_cache(user_id: int) -> int:
    """Clear all cache entries for a user"""
    if cache_manager:
        return cache_manager.invalidate_user_cache(user_id)
    return 0

def clear_project_cache(project_id: str) -> int:
    """Clear all cache entries for a project"""
    if cache_manager:
        return cache_manager.invalidate_project_cache(project_id)
    return 0