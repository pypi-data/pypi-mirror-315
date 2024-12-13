import os

import configurations
from celery import Celery

# Setup Django through django-configurations
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wbcore_config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")
configurations.setup()


# Setup Celery
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
