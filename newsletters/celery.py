from __future__ import absolute_import, unicode_literals
from configurations import importer

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsletters.settings.dev')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

importer.install()
app = Celery('newsletters')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
