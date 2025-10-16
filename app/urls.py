from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('appeal/', views.appeal_submit, name='appeal_submit'),
    path('incidents/', views.incidents_list, name='incidents_list'),
    path('monitoring/incidents/', views.incidents_monitoring, name='incidents_monitoring'),
    path('api/incidents/', views.incidents_api, name='incidents_api'),
    path('api/traffic/', views.traffic_api, name='traffic_api'),
    path('api/patrols/', views.patrols_api, name='patrols_api'),
    path('api/cameras/', views.cameras_api, name='cameras_api'),
    path('api/chat/send/', views.chat_send_message, name='chat_send_message'),
    path('api/chat/messages/', views.chat_thread_messages, name='chat_thread_messages'),
    path('news/', views.news_categories, name='news_categories'),
    path('news/category/<int:category_id>/', views.news_category_articles, name='news_category_articles'),
    path('news/article/<int:article_id>/', views.news_article_detail, name='news_article_detail'),
    # Новые API endpoints для управления данными
    path('api/weather/update/', views.update_weather, name='update_weather'),
    path('api/traffic-forecast/update/', views.update_traffic_forecast, name='update_traffic_forecast'),
    path('api/road-works/update/', views.update_road_works, name='update_road_works'),
    path('api/accident-stats/update/', views.update_accident_stats, name='update_accident_stats'),
    path('api/accident-data/update/', views.update_accident_data, name='update_accident_data'),
    path('api/accident-types/', views.accident_types_api, name='accident_types_api'),
    path('api/accident-data/', views.get_accident_data, name='get_accident_data'),
    # API для управления новостями
    path('api/news-categories/', views.news_categories_api, name='news_categories_api'),
    path('api/news-articles/', views.news_articles_api, name='news_articles_api'),
    # API для управления обращениями
    path('api/appeals/', views.appeals_api, name='appeals_api'),
    path('api/appeals/<int:appeal_id>/toggle/', views.appeal_toggle, name='appeal_toggle'),
    # API для управления чатами
    path('api/chat-threads/', views.chat_threads_api, name='chat_threads_api'),
    path('api/chat-threads/<int:thread_id>/toggle/', views.chat_thread_toggle, name='chat_thread_toggle'),
    path('api/admin/chat-threads/', views.admin_chat_threads_api, name='admin_chat_threads_api'),
    
    # Аутентификация
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('api/auth/status/', views.auth_status, name='auth_status'),
    # API для получения статистики ДТП
    path('api/accident-stats/', views.get_accident_stats, name='get_accident_stats'),
    # API для получения данных настроек
    path('api/weather/', views.get_weather_data, name='get_weather_data'),
    path('api/traffic-forecast/', views.get_traffic_forecast, name='get_traffic_forecast'),
    path('api/road-works/', views.get_road_works, name='get_road_works'),
]