import os

APPLICATION_NAME = "enterprise-ai-assistant"
APPLICATION_VERSION = "0.1.0"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "insecure-dev-fallback-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30