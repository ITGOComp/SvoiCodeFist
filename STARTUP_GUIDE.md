# 🚀 Руководство по запуску проекта SvoiCode

## 📋 Обзор

Теперь ваш проект поддерживает **гибридную архитектуру** с автоматическим переключением между режимами:

1. **Микросервисный режим** (по умолчанию) - Django + микросервисы
2. **Монолитный режим** - только Django с локальной БД
3. **API Gateway** (порт 9000) - для прямого доступа к микросервисам

## 🎯 Вариант 1: Гибридный режим (РЕКОМЕНДУЕТСЯ)

### Быстрый запуск:
```bash
# 1. Активируйте виртуальное окружение
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac

# 2. Запустите Django сервер
python manage.py runserver
```

### Доступ:
- **Главная страница:** http://localhost:8000
- **Админ панель:** http://localhost:8000/admin
- **Управление микросервисами:** http://localhost:8000/admin/microservices/

### Функционал:
- ✅ **Автоматическое переключение** между микросервисами и локальной БД
- ✅ **Fallback система** - если микросервис недоступен, используется локальная БД
- ✅ Полный веб-интерфейс
- ✅ Мониторинг инцидентов
- ✅ Аналитика трафика
- ✅ Новости и статьи
- ✅ Чат поддержки
- ✅ Обращения граждан
- ✅ Статистика ДТП
- ✅ **Панель управления микросервисами**

---

## 🔧 Вариант 2: Полная микросервисная архитектура

### Быстрый запуск:
```bash
# Запуск всех сервисов
make start
# или
docker-compose up -d
```

### Доступ:
- **API Gateway:** http://localhost:9000
- **Grafana (мониторинг):** http://localhost:3000 (admin/admin)
- **Prometheus:** http://localhost:9090
- **Kibana (логи):** http://localhost:5601
- **RabbitMQ:** http://localhost:15672 (admin/password)

### Микросервисы:
- **User Service:** http://localhost:8001
- **Incident Service:** http://localhost:8002
- **Traffic Service:** http://localhost:8003
- **News Service:** http://localhost:8004
- **Chat Service:** http://localhost:8005
- **Analytics Service:** http://localhost:8006
- **Traffic Analytics Service:** http://localhost:8007
- **Schedule Service:** http://localhost:8008
- **Notification Service:** http://localhost:8009

---

## 🎛️ Управление режимами работы

### Переключение между режимами:

```bash
# Включить микросервисы (по умолчанию)
python manage.py toggle_microservices --enable

# Отключить микросервисы (только локальная БД)
python manage.py toggle_microservices --disable

# Проверить текущий статус
python manage.py toggle_microservices --status

# Проверить здоровье микросервисов
python manage.py microservice_status
python manage.py microservice_status --detailed
```

### Веб-интерфейс управления:
- **Панель управления:** http://localhost:8000/admin/microservices/
- **API статуса:** http://localhost:8000/api/services/status/
- **Проверка здоровья:** http://localhost:8000/api/health/

---

## 🛠️ Полезные команды

### Для основного Django сайта:
```bash
# Миграции
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic

# Запуск в режиме разработки
python manage.py runserver 0.0.0.0:8000
```

### Для микросервисов:
```bash
# Просмотр логов
make logs

# Проверка здоровья сервисов
make health-check

# Остановка всех сервисов
make down

# Перезапуск
make restart

# Очистка (удаление всех контейнеров и данных)
make clean
```

---

## 🚨 Решение проблем

### Ошибка DisallowedHost:
```bash
# Если видите ошибку "Invalid HTTP_HOST header: 'localhost:8000'"
python fix_django_settings.py

# Или вручную добавьте в SvoiCode/settings.py:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:8000', 'localhost:9000']
```

### Порт занят:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Проблемы с Docker:
```bash
# Пересборка образов
make build

# Очистка Docker
docker system prune -a
```

### Проблемы с базой данных:
```bash
# Удаление и пересоздание БД
rm db.sqlite3
python manage.py migrate
```

### Проблемы с микросервисами:
```bash
# Проверить статус
python manage.py microservice_status

# Отключить микросервисы (использовать только локальную БД)
python manage.py toggle_microservices --disable

# Включить микросервисы
python manage.py toggle_microservices --enable
```

---

## 📊 Мониторинг

### Основной сайт:
- Логи в консоли Django
- SQLite база данных: `db.sqlite3`

### Микросервисы:
- **Grafana:** http://localhost:3000 - дашборды и метрики
- **Prometheus:** http://localhost:9090 - сбор метрик
- **Kibana:** http://localhost:5601 - анализ логов

---

## 🎯 Рекомендации

1. **Для разработки:** Используйте основной Django сайт (порт 8000)
2. **Для продакшена:** Используйте микросервисную архитектуру
3. **Для тестирования API:** Используйте микросервисы (порт 9000)

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте, что порты 8000 и 9000 свободны
2. Убедитесь, что Docker запущен (для микросервисов)
3. Проверьте логи: `make logs` или в консоли Django
