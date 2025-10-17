"""
URL configuration for traffic service API
"""
from django.urls import path
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'service': 'traffic_service'})

def api_root(request):
    """API root endpoint"""
    return JsonResponse({'message': 'Traffic Service', 'version': '1.0.0'})

urlpatterns = [
    path('', health_check, name='health_check'),
    path('traffic/', api_root, name='api_root'),
    path('patrols/', api_root, name='api_root'),
    path('cameras/', api_root, name='api_root'),
    path('detectors/', api_root, name='api_root'),
]