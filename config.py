import os

class Config:
    API_KEY = os.getenv("API_KEY", "your_default_api_key")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", 300))
    PORT = int(os.getenv("PORT", 8000))

