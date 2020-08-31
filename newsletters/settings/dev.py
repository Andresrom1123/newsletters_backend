from .base import Base
from decouple import config


class Dev(Base):
    DEBUG = config('DEBUG')

    SECRET_KEY = config('SECRET_KEY')

    EMAIL_HOST_PASSWORD = config('SECRET_PASSWORD_HOST')
