#!/usr/bin/env python3
"""
Script to create basic service structure for all microservices
"""

import os
import shutil
from pathlib import Path

# Service configurations
SERVICES = {
    'traffic_service': {
        'port': 8003,
        'redis_db': 2,
        'description': 'Traffic monitoring service'
    },
    'news_service': {
        'port': 8004,
        'redis_db': 3,
        'description': 'News and articles service'
    },
    'chat_service': {
        'port': 8005,
        'redis_db': 4,
        'description': 'Chat and messaging service'
    },
    'analytics_service': {
        'port': 8006,
        'redis_db': 5,
        'description': 'Basic analytics service'
    },
    'schedule_service': {
        'port': 8008,
        'redis_db': 7,
        'description': 'Schedule management service'
    },
    'notification_service': {
        'port': 8009,
        'redis_db': 8,
        'description': 'Notification service'
    }
}

def create_service_structure(service_name, config):
    """Create basic service structure"""
    service_dir = Path(f"services/{service_name}")
    service_dir.mkdir(parents=True, exist_ok=True)
    
    # Create Django app structure
    app_dir = service_dir / service_name
    app_dir.mkdir(exist_ok=True)
    
    # Create basic files
    files_to_create = {
        'Dockerfile': f"""FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE {config['port']}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{config['port']}/health || exit 1

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:{config['port']}"]
""",
        
        'requirements.txt': """Django==5.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
PyJWT==2.8.0
python-decouple==3.8
django-environ==0.11.2
prometheus-client==0.19.0
structlog==23.2.0
""",
        
        'manage.py': f"""#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys


def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{service_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
""",
        
        f'{service_name}/__init__.py': f'# {config["description"]} package',
        
        f'{service_name}/settings.py': f'''"""
Django settings for {service_name}
"""
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'django-insecure-change-me'),
    DATABASE_URL=(str, 'sqlite:///db.sqlite3'),
    REDIS_URL=(str, 'redis://localhost:6379/{config["redis_db"]}'),
)

# Read .env file
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    '{service_name}',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{service_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{service_name}.wsgi.application'

# Database
DATABASES = {{
    'default': env.db()
}}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Redis configuration
REDIS_URL = env('REDIS_URL')

# Logging
LOGGING = {{
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {{
        'verbose': {{
            'format': '{{levelname}} {{asctime}} {{module}} {{process:d}} {{thread:d}} {{message}}',
            'style': '{{',
        }},
        'simple': {{
            'format': '{{levelname}} {{message}}',
            'style': '{{',
        }},
    }},
    'handlers': {{
        'console': {{
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }},
    }},
    'root': {{
        'handlers': ['console'],
        'level': 'INFO',
    }},
    'loggers': {{
        'django': {{
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }},
        '{service_name}': {{
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }},
    }},
}}
''',
        
        f'{service_name}/urls.py': f'''"""
URL configuration for {service_name}
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({{'status': 'healthy', 'service': '{service_name}'}})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/', include('{service_name}.urls')),
]
''',
        
        f'{service_name}/wsgi.py': f'''"""
WSGI config for {service_name}
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{service_name}.settings')

application = get_wsgi_application()
''',
        
        f'{service_name}/urls.py': f'''"""
URL configuration for {service_name} API
"""
from django.urls import path
from django.http import JsonResponse

def api_root(request):
    """API root endpoint"""
    return JsonResponse({{'message': '{config["description"]}', 'version': '1.0.0'}})

urlpatterns = [
    path('', api_root, name='api_root'),
]
'''
    }
    
    # Create all files
    for file_path, content in files_to_create.items():
        full_path = service_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Created {service_name} service structure")

def main():
    """Create all service structures"""
    print("🚀 Creating microservices structure...")
    
    for service_name, config in SERVICES.items():
        create_service_structure(service_name, config)
    
    print("✅ All services created successfully!")

if __name__ == '__main__':
    main()
