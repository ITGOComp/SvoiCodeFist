"""
URLs for microservice-integrated views
"""
from django.urls import path
from . import views_microservices

urlpatterns = [
    # Main page with microservice integration
    path('', views_microservices.main_microservice, name='main_microservice'),
    
    # Incident Service URLs
    path('incidents/', views_microservices.incidents_list_microservice, name='incidents_list_microservice'),
    path('api/incidents/', views_microservices.incidents_api_microservice, name='incidents_api_microservice'),
    path('appeal/', views_microservices.appeal_submit_microservice, name='appeal_submit_microservice'),
    path('api/appeals/', views_microservices.appeals_api_microservice, name='appeals_api_microservice'),
    
    # Traffic Service URLs
    path('api/traffic/', views_microservices.traffic_api_microservice, name='traffic_api_microservice'),
    path('api/patrols/', views_microservices.patrols_api_microservice, name='patrols_api_microservice'),
    path('api/cameras/', views_microservices.cameras_api_microservice, name='cameras_api_microservice'),
    path('api/detectors/', views_microservices.detectors_api_microservice, name='detectors_api_microservice'),
    
    # News Service URLs
    path('news/', views_microservices.news_categories_microservice, name='news_categories_microservice'),
    path('news/category/<int:category_id>/', views_microservices.news_category_articles_microservice, name='news_category_articles_microservice'),
    path('news/article/<int:article_id>/', views_microservices.news_article_detail_microservice, name='news_article_detail_microservice'),
    
    # Chat Service URLs
    path('api/chat/send/', views_microservices.chat_send_message_microservice, name='chat_send_message_microservice'),
    path('api/chat/messages/', views_microservices.chat_thread_messages_microservice, name='chat_thread_messages_microservice'),
    
    # Analytics Service URLs
    path('api/accident-stats/', views_microservices.get_accident_stats_microservice, name='get_accident_stats_microservice'),
    path('api/weather/', views_microservices.get_weather_data_microservice, name='get_weather_data_microservice'),
    path('api/traffic-forecast/', views_microservices.get_traffic_forecast_microservice, name='get_traffic_forecast_microservice'),
    path('api/road-works/', views_microservices.get_road_works_microservice, name='get_road_works_microservice'),
    
    # Service Status URLs
    path('api/services/status/', views_microservices.service_status, name='service_status'),
    path('api/health/', views_microservices.health_check, name='health_check'),
    path('admin/microservices/', views_microservices.microservice_admin, name='microservice_admin'),
]
