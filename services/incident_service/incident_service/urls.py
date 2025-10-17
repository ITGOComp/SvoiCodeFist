"""
URL configuration for incident service API
"""
from django.urls import path
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'service': 'incident_service'})

def api_root(request):
    """API root endpoint"""
    return JsonResponse({'message': 'Incident Service', 'version': '1.0.0'})

urlpatterns = [
    path('', health_check, name='health_check'),
    path('incidents/', api_root, name='api_root'),
    path('appeals/', api_root, name='api_root'),
]