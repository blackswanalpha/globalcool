# Redis Setup Guide

## Installing Redis

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### macOS:
```bash
brew install redis
brew services start redis
```

### Check Redis is Running:
```bash
redis-cli ping
# Should return: PONG
```

## Switching Back to Redis

If you want to use Redis for better performance, update `config/settings.py`:

```python
# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## Benefits of Redis:
- Faster caching performance
- Better session management
- Supports advanced data structures
- Better for production environments

## Current Database Setup:
- Works perfectly for development
- No additional dependencies
- Easier to set up and maintain
- Good performance for small to medium applications
