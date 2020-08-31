import os

from .base import Base


class Prod(Base):
    SECRET_KEY = os.getenv('SECRET_KEY')

    DEBUG = os.getenv('DEBUG')

    ALLOWED_HOSTS = ['newsletters-app.herokuapp.com']

    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ]
    }

    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000',
        'https://awesome-visvesvaraya-2565c3.netlify.app'
    ]
