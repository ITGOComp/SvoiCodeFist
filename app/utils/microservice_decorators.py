"""
Decorators for microservice integration
"""
import logging
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from app.services.service_manager import service_manager
from app.services.base_client import MicroserviceError

logger = logging.getLogger(__name__)


def microservice_fallback(fallback_func=None):
    """
    Decorator to handle microservice failures with fallback to local database
    
    Usage:
    @microservice_fallback(fallback_func=local_get_incidents)
    def get_incidents_from_service():
        return service_manager.incident.get_incidents()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if microservices are enabled
            if not getattr(settings, 'USE_MICROSERVICES', True):
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                return JsonResponse({'error': 'Microservices disabled'}, status=503)
            
            try:
                return func(*args, **kwargs)
            except MicroserviceError as e:
                logger.warning(f"Microservice error in {func.__name__}: {e}")
                if fallback_func:
                    logger.info(f"Falling back to local function: {fallback_func.__name__}")
                    return fallback_func(*args, **kwargs)
                return JsonResponse({'error': 'Service temporarily unavailable'}, status=503)
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                return JsonResponse({'error': 'Internal server error'}, status=500)
        
        return wrapper
    return decorator


def require_microservice(service_name):
    """
    Decorator to require specific microservice to be available
    
    Usage:
    @require_microservice('incident_service')
    def some_function():
        return service_manager.incident.get_incidents()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not service_manager.is_service_available(service_name):
                return JsonResponse({
                    'error': f'Service {service_name} is not available'
                }, status=503)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def microservice_health_check():
    """
    Check health of all microservices
    """
    return service_manager.health_check_all()


def get_service_status():
    """
    Get detailed status of all services
    """
    return service_manager.get_service_status()
