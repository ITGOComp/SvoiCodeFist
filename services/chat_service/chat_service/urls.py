"""
URL configuration for chat_service API
"""
from django.urls import path
from django.http import JsonResponse

def api_root(request):
    """API root endpoint"""
    return JsonResponse({'message': 'Chat and messaging service', 'version': '1.0.0'})

urlpatterns = [
    path('', api_root, name='api_root'),
]
