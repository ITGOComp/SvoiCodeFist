import requests
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Schedule, Appeal, Incident, TrafficJam, Patrol, Camera, NewsCategory, Article, ChatThread, ChatMessage, AccidentType, AccidentData, AccidentStatistics, WeatherData, TrafficForecast, RoadWorks
from django import forms
from django.utils import timezone
import json
from django.db.models import IntegerField, CharField
from django.db.models.functions import Cast
from django.db import models
from django.shortcuts import render, get_object_or_404
import json

def main(request):
    categories = NewsCategory.objects.all()
    
    # Получаем данные для верхней панели
    weather = WeatherData.objects.first()
    traffic_forecast = TrafficForecast.objects.first()
    road_works = RoadWorks.objects.first()
    
    # Получаем статистику ДТП
    accident_stats = AccidentStatistics.objects.first()
    
    # Получаем данные для графика ДТП
    accident_types = AccidentType.objects.all()
    accident_data = {}
    for accident_type in accident_types:
        data = list(AccidentData.objects.filter(accident_type=accident_type, year=2024).order_by('month').values_list('count', flat=True))
        # Дополняем данные нулями до 12 месяцев, если данных недостаточно
        while len(data) < 12:
            data.append(0)
        accident_data[accident_type.name] = {
            'color': accident_type.color,
            'data': data
        }
    
    context = {
        'categories': categories,
        'weather': weather,
        'traffic_forecast': traffic_forecast,
        'road_works': road_works,
        'accident_stats': accident_stats,
        'accident_data': accident_data,
    }
    return render(request, 'MainHTML/Main.html', context)


class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['name', 'email', 'message']


@csrf_exempt
def appeal_submit(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            form.save()
            # AJAX/JSON response for nicer UX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('accept', '').find('application/json') != -1:
                return JsonResponse({'ok': True})
            return render(request, 'MainHTML/AppealThanks.html')
        # invalid
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('accept', '').find('application/json') != -1:
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        return render(request, 'MainHTML/AppealForm.html', {'form': form})

    form = AppealForm()
    return render(request, 'MainHTML/AppealForm.html', {'form': form})


def incidents_list(request):
    incidents = Incident.objects.all().order_by('-occurred_at')
    return render(request, 'MainHTML/IncidentsList.html', {'incidents': incidents})


def incidents_monitoring(request):
    total = Incident.objects.count()
    by_status = (
        Incident.objects
        .values('status')
        .order_by('status')
        .annotate(count=models.Count('id'))
    )
    by_severity = (
        Incident.objects
        .values('severity')
        .order_by('severity')
        .annotate(count=models.Count('id'))
    )
    last_7_days = Incident.objects.filter(occurred_at__gte=timezone.now()-timezone.timedelta(days=7)).count()
    context = {
        'total': total,
        'by_status': list(by_status),
        'by_severity': list(by_severity),
        'last_7_days': last_7_days,
    }
    return render(request, 'MainHTML/IncidentsMonitoring.html', context)


def incidents_api(request):
    qs = Incident.objects.all().order_by('-occurred_at')
    data = []
    for i in qs:
        data.append({
            'id': i.id,
            'title': i.title,
            'description': i.description,
            'occurred_at': i.occurred_at.isoformat(),
            'status': i.status,
            'severity': i.severity,
            'coordinates': i.coordinates or [],
        })
    return JsonResponse({'incidents': data})


def traffic_api(request):
    qs = TrafficJam.objects.all().order_by('-occurred_at')
    data = []
    for t in qs:
        coords = t.coordinates or []
        if len(coords) >= 2:
            data.append({
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'coordinates': coords,
                'severity': t.severity,
                'occurred_at': t.occurred_at.isoformat(),
            })
    return JsonResponse({'traffic': data})


def patrols_api(request):
    qs = Patrol.objects.all().order_by('-created_at')
    data = []
    for p in qs:
        coords = p.coordinates or []
        if len(coords) >= 2:
            data.append({
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'coordinates': coords,
                'radius_m': p.radius_m,
            })
    return JsonResponse({'patrols': data})


def cameras_api(request):
    qs = Camera.objects.all().order_by('-created_at')
    data = []
    for c in qs:
        coords = c.coordinates or []
        if isinstance(coords, str):
            try:
                coords = json.loads(coords)
            except Exception:
                coords = []
        if len(coords) >= 2:
            data.append({
                'id': c.id,
                'name': c.name,
                'description': c.description,
                'coordinates': coords,
            })
    return JsonResponse({'cameras': data})


def news_categories(request):
    categories = NewsCategory.objects.all()
    return render(request, 'MainHTML/NewsCategories.html', {'categories': categories})


def news_category_articles(request, category_id):
    category = get_object_or_404(NewsCategory, id=category_id)
    articles = Article.objects.filter(category=category).order_by('-created_at')
    return render(request, 'MainHTML/NewsArticles.html', {'category': category, 'articles': articles})


def news_article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'MainHTML/NewsArticleDetail.html', {'article': article})


@csrf_exempt
def chat_send_message(request):
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

    # Use or create thread for authenticated user; guests get separate thread per session
    thread = None
    if request.user.is_authenticated:
        thread_id = (payload or {}).get('thread_id')
        if thread_id:
            thread = ChatThread.objects.filter(id=thread_id, is_closed=False).first()
        if not thread:
            thread = ChatThread.objects.create(user=request.user, subject=subject)
    else:
        # store thread id in session
        thread_id = request.session.get('guest_thread_id')
        if thread_id:
            thread = ChatThread.objects.filter(id=thread_id, user__isnull=True, is_closed=False).first()
        if not thread:
            thread = ChatThread.objects.create(user=None, subject=subject)
            request.session['guest_thread_id'] = thread.id

    # Определяем отправителя
    if sender_type == 'admin':
        sender = ChatMessage.Sender.ADMIN
    else:
        sender = ChatMessage.Sender.USER

    msg = ChatMessage.objects.create(thread=thread, sender=sender, content=content)
    return JsonResponse({'ok': True, 'thread_id': thread.id, 'message_id': msg.id})


def chat_thread_messages(request):
    thread_id = request.GET.get('thread_id')
    if request.user.is_authenticated:
        thread = ChatThread.objects.filter(id=thread_id, user=request.user).first() if thread_id else ChatThread.objects.filter(user=request.user).order_by('-created_at').first()
    else:
        guest_thread_id = request.session.get('guest_thread_id')
        if not guest_thread_id:
            return JsonResponse({'messages': [], 'thread_id': None})
        thread = ChatThread.objects.filter(id=guest_thread_id, user__isnull=True).first()

    if not thread:
        return JsonResponse({'messages': [], 'thread_id': None})

    messages = list(thread.messages.order_by('created_at').values('id', 'sender', 'content', 'created_at'))
    return JsonResponse({'thread_id': thread.id, 'messages': messages, 'is_authenticated': request.user.is_authenticated})


# API для управления данными верхней панели
@csrf_exempt
def update_weather(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            weather, created = WeatherData.objects.get_or_create(pk=1)
            weather.temperature = data.get('temperature', 0)
            weather.description = data.get('description', '')
            weather.icon = data.get('icon', 'fa-sun')
            weather.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


@csrf_exempt
def update_traffic_forecast(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            forecast, created = TrafficForecast.objects.get_or_create(pk=1)
            forecast.speed = data.get('speed', 0)
            forecast.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


@csrf_exempt
def update_road_works(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            works, created = RoadWorks.objects.get_or_create(pk=1)
            works.count = data.get('count', 0)
            works.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


# API для управления статистикой ДТП
@csrf_exempt
def update_accident_stats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stats, created = AccidentStatistics.objects.get_or_create(pk=1)
            stats.total_accidents = data.get('total_accidents', 0)
            stats.injured = data.get('injured', 0)
            stats.killed = data.get('killed', 0)
            stats.year = data.get('year', 2024)
            stats.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


@csrf_exempt
def update_accident_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            accident_type_id = data.get('accident_type_id')
            month = data.get('month')
            count = data.get('count', 0)
            year = data.get('year', 2024)
            
            accident_data, created = AccidentData.objects.get_or_create(
                accident_type_id=accident_type_id,
                month=month,
                year=year,
                defaults={'count': count}
            )
            if not created:
                accident_data.count = count
                accident_data.save()
            
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)


def get_accident_types(request):
    types = list(AccidentType.objects.values('id', 'name', 'color'))
    return JsonResponse({'types': types})


@csrf_exempt
def accident_types_api(request):
    if request.method == 'GET':
        types = list(AccidentType.objects.values('id', 'name', 'color'))
        return JsonResponse({'types': types})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            accident_type = AccidentType.objects.create(
                name=data.get('name'),
                color=data.get('color', '#36A2EB')
            )
            return JsonResponse({'ok': True, 'id': accident_type.id})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            accident_type = AccidentType.objects.get(id=data.get('id'))
            accident_type.name = data.get('name', accident_type.name)
            accident_type.color = data.get('color', accident_type.color)
            accident_type.save()
            return JsonResponse({'ok': True})
        except AccidentType.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Accident type not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            accident_type = AccidentType.objects.get(id=data.get('id'))
            accident_type.delete()
            return JsonResponse({'ok': True})
        except AccidentType.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Accident type not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


def get_accident_data(request):
    year = request.GET.get('year', 2024)
    data = {}
    for accident_type in AccidentType.objects.all():
        data[accident_type.name] = {
            'id': accident_type.id,
            'color': accident_type.color,
            'data': list(AccidentData.objects.filter(
                accident_type=accident_type, 
                year=year
            ).order_by('month').values_list('count', flat=True))
        }
    return JsonResponse(data)


# API для управления новостными категориями
@csrf_exempt
def news_categories_api(request):
    if request.method == 'GET':
        categories = list(NewsCategory.objects.values('id', 'name', 'image_url'))
        return JsonResponse({'categories': categories})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = NewsCategory.objects.create(
                name=data.get('name'),
                image_url=data.get('image_url', '')
            )
            return JsonResponse({'ok': True, 'id': category.id})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            category_id = data.get('id')
            category = NewsCategory.objects.get(id=category_id)
            category.name = data.get('name', category.name)
            category.image_url = data.get('image_url', category.image_url)
            category.save()
            return JsonResponse({'ok': True})
        except NewsCategory.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            category_id = data.get('id')
            category = NewsCategory.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'ok': True})
        except NewsCategory.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


# API для управления статьями
@csrf_exempt
def news_articles_api(request):
    if request.method == 'GET':
        articles = list(Article.objects.select_related('category').values(
            'id', 'title', 'author', 'summary', 'content', 'created_at',
            'category__name', 'cover_image_url', 'category_id'
        ))
        return JsonResponse({'articles': articles})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = NewsCategory.objects.get(id=data.get('category_id'))
            article = Article.objects.create(
                category=category,
                title=data.get('title'),
                author=data.get('author', ''),
                summary=data.get('summary', ''),
                content=data.get('content'),
                cover_image_url=data.get('cover_image_url', '')
            )
            return JsonResponse({'ok': True, 'id': article.id})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            article_id = data.get('id')
            article = Article.objects.get(id=article_id)
            article.title = data.get('title', article.title)
            article.author = data.get('author', article.author)
            article.summary = data.get('summary', article.summary)
            article.content = data.get('content', article.content)
            article.cover_image_url = data.get('cover_image_url', article.cover_image_url)
            if data.get('category_id'):
                category = NewsCategory.objects.get(id=data.get('category_id'))
                article.category = category
            article.save()
            return JsonResponse({'ok': True})
        except Article.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Article not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            article_id = data.get('id')
            article = Article.objects.get(id=article_id)
            article.delete()
            return JsonResponse({'ok': True})
        except Article.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Article not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


# API для управления обращениями
@csrf_exempt
def appeals_api(request):
    if request.method == 'GET':
        filter_type = request.GET.get('filter', 'all')
        appeals = Appeal.objects.all()
        
        if filter_type == 'pending':
            appeals = appeals.filter(is_reviewed=False)
        elif filter_type == 'reviewed':
            appeals = appeals.filter(is_reviewed=True)
            
        appeals = list(appeals.values('id', 'name', 'email', 'message', 'is_reviewed', 'created_at'))
        return JsonResponse({'appeals': appeals})
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


@csrf_exempt
def appeal_toggle(request, appeal_id):
    if request.method == 'POST':
        try:
            appeal = Appeal.objects.get(id=appeal_id)
            appeal.is_reviewed = not appeal.is_reviewed
            appeal.save()
            return JsonResponse({'ok': True})
        except Appeal.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Appeal not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


# API для управления чатами
@csrf_exempt
def chat_threads_api(request):
    if request.method == 'GET':
        threads = []
        # Показываем только чаты текущего пользователя или гостевые чаты
        if request.user.is_authenticated:
            # Для авторизованных пользователей показываем только их чаты
            user_threads = ChatThread.objects.filter(user=request.user)
        else:
            # Для гостей показываем только их чаты по session
            guest_thread_id = request.session.get('guest_thread_id')
            if guest_thread_id:
                user_threads = ChatThread.objects.filter(id=guest_thread_id, user__isnull=True)
            else:
                user_threads = ChatThread.objects.none()
        
        for thread in user_threads:
            threads.append({
                'id': thread.id,
                'subject': thread.subject,
                'user_name': thread.user.get_username() if thread.user else 'Гость',
                'message_count': thread.messages.count(),
                'is_closed': thread.is_closed,
                'created_at': thread.created_at.isoformat()
            })
        return JsonResponse({'threads': threads})
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


@csrf_exempt
def chat_thread_toggle(request, thread_id):
    if request.method == 'POST':
        try:
            thread = ChatThread.objects.get(id=thread_id)
            thread.is_closed = not thread.is_closed
            thread.save()
            return JsonResponse({'ok': True})
        except ChatThread.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Thread not found'}, status=404)
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)


# API для админов - показывает все чаты
@csrf_exempt
def admin_chat_threads_api(request):
    if request.method == 'GET':
        # Проверяем, что пользователь авторизован (в реальном приложении нужно проверить права админа)
        if not request.user.is_authenticated:
            return JsonResponse({'ok': False, 'error': 'Authentication required'}, status=401)
        
        threads = []
        for thread in ChatThread.objects.all().order_by('-created_at'):
            threads.append({
                'id': thread.id,
                'subject': thread.subject,
                'user_name': thread.user.get_username() if thread.user else 'Гость',
                'message_count': thread.messages.count(),
                'is_closed': thread.is_closed,
                'created_at': thread.created_at.isoformat()
            })
        return JsonResponse({'threads': threads})
    return JsonResponse({'ok': False, 'error': 'Method not allowed'}, status=405)

# API для аутентификации
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'role': 'admin' if user.is_superuser else 'editor'
                    }
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST required'})


@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'POST required'})


@csrf_exempt
def auth_status(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'role': 'admin' if request.user.is_superuser else 'editor'
                }
            })
        else:
            return JsonResponse({'authenticated': False})
    
    return JsonResponse({'authenticated': False})


@csrf_exempt
def get_accident_stats(request):
    if request.method == 'GET':
        try:
            accident_stats = AccidentStatistics.objects.first()
            if accident_stats:
                return JsonResponse({
                    'accident_stats': {
                        'total_accidents': accident_stats.total_accidents,
                        'injured': accident_stats.injured,
                        'killed': accident_stats.killed,
                        'year': accident_stats.year
                    }
                })
            else:
                return JsonResponse({
                    'accident_stats': {
                        'total_accidents': 0,
                        'injured': 0,
                        'killed': 0,
                        'year': 2024
                    }
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_weather_data(request):
    if request.method == 'GET':
        try:
            weather = WeatherData.objects.first()
            if weather:
                return JsonResponse({
                    'weather': {
                        'temperature': weather.temperature,
                        'description': weather.description,
                        'icon': weather.icon
                    }
                })
            else:
                return JsonResponse({
                    'weather': {
                        'temperature': 0,
                        'description': 'Данные не загружены',
                        'icon': 'fa-sun'
                    }
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_traffic_forecast(request):
    if request.method == 'GET':
        try:
            traffic = TrafficForecast.objects.first()
            if traffic:
                return JsonResponse({
                    'traffic_forecast': {
                        'speed': traffic.speed
                    }
                })
            else:
                return JsonResponse({
                    'traffic_forecast': {
                        'speed': 0
                    }
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_road_works(request):
    if request.method == 'GET':
        try:
            road_works = RoadWorks.objects.first()
            if road_works:
                return JsonResponse({
                    'road_works': {
                        'count': road_works.count
                    }
                })
            else:
                return JsonResponse({
                    'road_works': {
                        'count': 0
                    }
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
