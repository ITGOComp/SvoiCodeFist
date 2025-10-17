"""
WSGI config for traffic analytics service
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_analytics_service.settings')

application = get_wsgi_application()
