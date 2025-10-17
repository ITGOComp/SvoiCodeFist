# 🔗 Интеграция микросервисов с Django

## 📋 Обзор

Ваш проект теперь поддерживает **гибридную архитектуру**, которая автоматически переключается между микросервисами и локальной базой данных в зависимости от доступности сервисов.

## 🏗️ Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Django App    │    │  Service Manager │    │  Microservices  │
│   (Port 8000)   │◄──►│                  │◄──►│  (Ports 8001-9) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   Fallback to   │
         └──────────────►│  Local Database │
                        └─────────────────┘
```

## 🔧 Компоненты интеграции

### 1. Service Manager (`app/services/service_manager.py`)
- Центральный менеджер для всех микросервисов
- Автоматическое определение доступности сервисов
- Единая точка входа для всех операций

### 2. Service Clients (`app/services/`)
- `base_client.py` - Базовый клиент для HTTP-коммуникации
- `incident_client.py` - Клиент для Incident Service
- `traffic_client.py` - Клиент для Traffic Service
- `news_client.py` - Клиент для News Service
- `chat_client.py` - Клиент для Chat Service
- `analytics_client.py` - Клиент для Analytics Service

### 3. Fallback Decorators (`app/utils/microservice_decorators.py`)
- `@microservice_fallback` - Автоматический fallback на локальную БД
- `@require_microservice` - Требование доступности сервиса

### 4. Integrated Views (`app/views_microservices.py`)
- Views с интеграцией микросервисов
- Автоматический fallback при недоступности сервисов

## 🚀 Быстрый старт

### 1. Запуск в гибридном режиме (рекомендуется)
```bash
# Активируйте виртуальное окружение
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Запустите Django
python manage.py runserver
```

**Доступ:** http://localhost:8000

### 2. Запуск с полными микросервисами
```bash
# Запустите микросервисы
make start

# В другом терминале запустите Django
python manage.py runserver
```

## 🎛️ Управление режимами

### Команды управления
```bash
# Проверить статус микросервисов
python manage.py microservice_status
python manage.py microservice_status --detailed

# Переключить режимы
python manage.py toggle_microservices --enable   # Включить микросервисы
python manage.py toggle_microservices --disable  # Отключить микросервисы
python manage.py toggle_microservices --status   # Проверить текущий режим
```

### Веб-интерфейс управления
- **Панель управления:** http://localhost:8000/admin/microservices/
- **API статуса:** http://localhost:8000/api/services/status/
- **Проверка здоровья:** http://localhost:8000/api/health/

## 🔄 Fallback механизм

### Как это работает:
1. **Попытка обращения к микросервису** - система пытается получить данные из микросервиса
2. **Проверка доступности** - если сервис недоступен, срабатывает fallback
3. **Переключение на локальную БД** - данные берутся из локальной SQLite базы
4. **Прозрачность для пользователя** - пользователь не замечает переключения

### Пример использования:
```python
@microservice_fallback(fallback_func=local_get_incidents)
def get_incidents_from_service():
    return service_manager.incident.get_incidents()
```

## 📊 Мониторинг

### API endpoints для мониторинга:
- `GET /api/health/` - Общее здоровье системы
- `GET /api/services/status/` - Детальный статус всех сервисов
- `GET /admin/microservices/` - Веб-панель управления

### Логирование:
- Все ошибки микросервисов логируются
- Fallback операции отмечаются в логах
- Статистика доступности сервисов

## 🧪 Тестирование

### Автоматические тесты:
```bash
# Запуск тестов интеграции
python test_microservices_integration.py
```

### Ручное тестирование:
1. Запустите Django: `python manage.py runserver`
2. Откройте http://localhost:8000/admin/microservices/
3. Проверьте статус всех сервисов
4. Протестируйте основные функции сайта

## 🔧 Настройка

### Переменные окружения:
```python
# settings.py
USE_MICROSERVICES = True  # Включить/выключить микросервисы
MICROSERVICE_TIMEOUT = 30  # Таймаут для запросов к сервисам
MICROSERVICES = {
    'incident_service': 'http://localhost:8002',
    'traffic_service': 'http://localhost:8003',
    # ... другие сервисы
}
```

### Настройка URL-ов сервисов:
```python
# В settings.py измените URL-ы сервисов
MICROSERVICES = {
    'incident_service': 'http://your-server:8002',
    'traffic_service': 'http://your-server:8003',
    # ...
}
```

## 🚨 Устранение неполадок

### Проблема: Микросервисы недоступны
**Решение:**
1. Проверьте, запущены ли микросервисы: `make status`
2. Проверьте порты: `netstat -an | grep :800`
3. Временно отключите микросервисы: `python manage.py toggle_microservices --disable`

### Проблема: Ошибки подключения
**Решение:**
1. Проверьте настройки в `settings.py`
2. Убедитесь, что URL-ы сервисов корректны
3. Проверьте сетевую доступность

### Проблема: Fallback не работает
**Решение:**
1. Проверьте, что локальная БД существует
2. Выполните миграции: `python manage.py migrate`
3. Проверьте логи Django

## 📈 Преимущества интеграции

### ✅ Для разработки:
- **Гибкость** - можно работать с микросервисами или без них
- **Отказоустойчивость** - система работает даже при недоступности сервисов
- **Простота тестирования** - легко переключаться между режимами

### ✅ Для продакшена:
- **Масштабируемость** - можно добавлять новые микросервисы
- **Надежность** - fallback обеспечивает непрерывность работы
- **Мониторинг** - встроенные инструменты для отслеживания состояния

## 🔮 Дальнейшее развитие

### Планируемые улучшения:
1. **Кэширование** - Redis для кэширования данных микросервисов
2. **Очереди** - Асинхронная обработка запросов
3. **Метрики** - Детальная аналитика производительности
4. **Автоматическое восстановление** - Автоматическое переподключение к сервисам

---

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте логи Django
2. Используйте команду `python manage.py microservice_status --detailed`
3. Обратитесь к веб-панели управления: http://localhost:8000/admin/microservices/
