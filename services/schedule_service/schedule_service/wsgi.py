"""
WSGI config for schedule_service
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schedule_service.settings')

application = get_wsgi_application()
