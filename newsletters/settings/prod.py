from .base import Base


class Prod(Base):
    DEBUG = True
    ALLOWED_HOSTS = ['newsletters-app.herokuapp.com']

    CORS_ORIGIN_ALLOW_ALL = True

    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ]
    }

    # CORS_ORIGIN_WHITELIST = [
    #  'http://localhost:3000',
    #   'https://awesome-visvesvaraya-2565c3.netlify.app'
    # ]
