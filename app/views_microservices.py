"""
Views that integrate with microservices
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.conf import settings

from app.services.service_manager import service_manager
from app.utils.microservice_decorators import microservice_fallback, require_microservice
from .models import Incident, Appeal, TrafficJam, Patrol, Camera, NewsCategory, Article, ChatThread, ChatMessage
from .views import main as main_view  # Import original views for fallback


# ==================== INCIDENT SERVICE INTEGRATION ====================

@microservice_fallback(fallback_func=lambda request: JsonResponse({'incidents': []}))
def incidents_api_microservice(request):
    """Get incidents from microservice"""
    incidents = service_manager.incident.get_incidents()
    return JsonResponse({'incidents': incidents})


@microservice_fallback(fallback_func=lambda request: render(request, 'MainHTML/IncidentsList.html', {'incidents': []}))
def incidents_list_microservice(request):
    """Get incidents list page with microservice data"""
    incidents = service_manager.incident.get_incidents()
    return render(request, 'MainHTML/IncidentsList.html', {'incidents': incidents})


@microservice_fallback(fallback_func=lambda request: JsonResponse({'ok': False, 'error': 'Service unavailable'}))
@csrf_exempt
def appeal_submit_microservice(request):
    """Submit appeal through microservice"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else request.POST
            appeal_data = {
                'name': data.get('name'),
                'email': data.get('email'),
                'message': data.get('message')
            }
            result = service_manager.incident.create_appeal(appeal_data)
            return JsonResponse({'ok': True, 'id': result.get('id')})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


@microservice_fallback(fallback_func=lambda request: JsonResponse({'appeals': []}))
def appeals_api_microservice(request):
    """Get appeals from microservice"""
    filter_type = request.GET.get('filter', 'all')
    appeals = service_manager.incident.get_appeals(filter_type)
    return JsonResponse({'appeals': appeals})


# ==================== TRAFFIC SERVICE INTEGRATION ====================

@microservice_fallback(fallback_func=lambda request: JsonResponse({'traffic': []}))
def traffic_api_microservice(request):
    """Get traffic data from microservice"""
    traffic = service_manager.traffic.get_traffic_jams()
    return JsonResponse({'traffic': traffic})


@microservice_fallback(fallback_func=lambda request: JsonResponse({'patrols': []}))
def patrols_api_microservice(request):
    """Get patrols from microservice"""
    patrols = service_manager.traffic.get_patrols()
    return JsonResponse({'patrols': patrols})


@microservice_fallback(fallback_func=lambda request: JsonResponse({'cameras': []}))
def cameras_api_microservice(request):
    """Get cameras from microservice"""
    cameras = service_manager.traffic.get_cameras()
    return JsonResponse({'cameras': cameras})


@microservice_fallback(fallback_func=lambda request: JsonResponse({'detectors': []}))
def detectors_api_microservice(request):
    """Get detectors from microservice"""
    detectors = service_manager.traffic.get_detectors()
    return JsonResponse({'detectors': detectors})


# ==================== NEWS SERVICE INTEGRATION ====================

@microservice_fallback(fallback_func=lambda request: render(request, 'MainHTML/NewsCategories.html', {'categories': []}))
def news_categories_microservice(request):
    """Get news categories from microservice"""
    categories = service_manager.news.get_categories()
    return render(request, 'MainHTML/NewsCategories.html', {'categories': categories})


@microservice_fallback(fallback_func=lambda request, category_id: render(request, 'MainHTML/NewsArticles.html', {'category': None, 'articles': []}))
def news_category_articles_microservice(request, category_id):
    """Get articles by category from microservice"""
    try:
        # Get category info - we'll need to add this method to news client
        categories = service_manager.news.get_categories()
        category = next((c for c in categories if c.get('id') == category_id), None)
        articles = service_manager.news.get_articles_by_category(category_id)
        return render(request, 'MainHTML/NewsArticles.html', {'category': category, 'articles': articles})
    except Exception:
        return render(request, 'MainHTML/NewsArticles.html', {'category': None, 'articles': []})


@microservice_fallback(fallback_func=lambda request, article_id: render(request, 'MainHTML/NewsArticleDetail.html', {'article': None}))
def news_article_detail_microservice(request, article_id):
    """Get article detail from microservice"""
    try:
        article = service_manager.news.get_article(article_id)
        return render(request, 'MainHTML/NewsArticleDetail.html', {'article': article})
    except Exception:
        return render(request, 'MainHTML/NewsArticleDetail.html', {'article': None})


# ==================== CHAT SERVICE INTEGRATION ====================

@microservice_fallback(fallback_func=lambda request: JsonResponse({'ok': False, 'error': 'Service unavailable'}))
@csrf_exempt
def chat_send_message_microservice(request):
    """Send chat message through microservice"""
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        payload = request.POST

    content = (payload or {}).get('content', '').strip()
    subject = (payload or {}).get('subject', '').strip()
    sender_type = (payload or {}).get('sender', 'user')
    
    if not content:
        return JsonResponse({'ok': False, 'error': 'empty content'}, status=400)

    message_data = {
        'content': content,
        'subject': subject,
        'sender': sender_type,
        'thread_id': (payload or {}).get('thread_id')
    }
    
    result = service_manager.chat.send_message(message_data)
    return JsonResponse(result)


@microservice_fallback(fallback_func=lambda request: JsonResponse({'messages': [], 'thread_id': None}))
def chat_thread_messages_microservice(request):
    """Get chat messages from microservice"""
    thread_id = request.GET.get('thread_id')
    result = service_manager.chat.get_messages(thread_id)
    return JsonResponse(result)


# ==================== ANALYTICS SERVICE INTEGRATION ====================

@microservice_fallback(fallback_func=lambda request: JsonResponse({'accident_stats': {'total_accidents': 0, 'injured': 0, 'killed': 0, 'year': 2024}}))
def get_accident_stats_microservice(request):
    """Get accident statistics from microservice"""
    if request.method == 'GET':
        stats = service_manager.analytics.get_accident_statistics()
        return JsonResponse(stats)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@microservice_fallback(fallback_func=lambda request: JsonResponse({'weather': {'temperature': 0, 'description': 'Данные не загружены', 'icon': 'fa-sun'}}))
def get_weather_data_microservice(request):
    """Get weather data from microservice"""
    if request.method == 'GET':
        weather = service_manager.analytics.get_weather_data()
        return JsonResponse(weather)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@microservice_fallback(fallback_func=lambda request: JsonResponse({'traffic_forecast': {'speed': 0}}))
def get_traffic_forecast_microservice(request):
    """Get traffic forecast from microservice"""
    if request.method == 'GET':
        forecast = service_manager.analytics.get_traffic_forecast()
        return JsonResponse(forecast)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@microservice_fallback(fallback_func=lambda request: JsonResponse({'road_works': {'count': 0}}))
def get_road_works_microservice(request):
    """Get road works data from microservice"""
    if request.method == 'GET':
        works = service_manager.analytics.get_road_works()
        return JsonResponse(works)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ==================== MAIN PAGE INTEGRATION ====================

@microservice_fallback(fallback_func=main_view)
def main_microservice(request):
    """Main page with microservice integration"""
    try:
        # Get data from microservices
        categories = service_manager.news.get_categories()
        weather = service_manager.analytics.get_weather_data()
        traffic_forecast = service_manager.analytics.get_traffic_forecast()
        road_works = service_manager.analytics.get_road_works()
        accident_stats = service_manager.analytics.get_accident_statistics()
        accident_types = service_manager.analytics.get_accident_types()
        
        # Process accident data for charts
        accident_data = {}
        for accident_type in accident_types:
            accident_data[accident_type['name']] = {
                'color': accident_type['color'],
                'data': [0] * 12  # Placeholder data
            }
        
        context = {
            'categories': categories,
            'weather': weather.get('weather', {}),
            'traffic_forecast': traffic_forecast.get('traffic_forecast', {}),
            'road_works': road_works.get('road_works', {}),
            'accident_stats': accident_stats.get('accident_stats', {}),
            'accident_data': accident_data,
        }
        return render(request, 'MainHTML/Main.html', context)
    except Exception as e:
        # Fallback to original main view
        return main_view(request)


# ==================== SERVICE STATUS ====================

def service_status(request):
    """Get status of all microservices"""
    status = service_manager.get_service_status()
    return JsonResponse({'services': status})


def health_check(request):
    """Health check for microservices"""
    health = service_manager.health_check_all()
    return JsonResponse({'health': health})


def microservice_admin(request):
    """Microservice administration page"""
    return render(request, 'MainHTML/MicroserviceAdmin.html')
