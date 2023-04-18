import os
import redis

class ApplicationConfig:
    SECRET_KEY = os.environ['APP_SECRET_KEY']

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(f'redis://{os.environ["REDIS_URL"]}:6379')