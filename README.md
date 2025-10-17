# Система мониторинга дорожного движения - Микросервисная архитектура

## Обзор

Этот проект представляет собой систему мониторинга дорожного движения, разбитую на микросервисы с применением принципов Clean Architecture и Domain-Driven Design (DDD).

## Архитектура

### Микросервисы

1. **API Gateway** (порт 8000) - Единая точка входа для всех запросов
2. **User Service** (порт 8001) - Управление пользователями и аутентификация
3. **Incident Service** (порт 8002) - Управление инцидентами и обращениями
4. **Traffic Service** (порт 8003) - Мониторинг дорожного движения
5. **News Service** (порт 8004) - Управление новостями и статьями
6. **Chat Service** (порт 8005) - Система чатов и сообщений
7. **Analytics Service** (порт 8006) - Базовая аналитика ДТП
8. **Traffic Analytics Service** (порт 8007) - Продвинутая аналитика трафика
9. **Schedule Service** (порт 8008) - Управление расписанием
10. **Notification Service** (порт 8009) - Уведомления

### Clean Architecture

Каждый микросервис следует принципам Clean Architecture:

- **Domain Layer** - Бизнес-логика и сущности
- **Application Layer** - Use cases и сценарии использования
- **Infrastructure Layer** - Реализация репозиториев и внешних сервисов
- **Presentation Layer** - Контроллеры и API endpoints

## Технологический стек

- **Backend**: Django + Django REST Framework
- **API Gateway**: FastAPI
- **Database**: PostgreSQL (основная), TimescaleDB (временные ряды), ClickHouse (аналитика)
- **Cache**: Redis
- **Message Broker**: RabbitMQ
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Containerization**: Docker + Docker Compose

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd traffic-monitoring-microservices
   ```

2. **Запуск всех сервисов**
   ```bash
   # На Linux/macOS
   ./scripts/deploy.sh
   
   # На Windows
   docker-compose up -d
   ```

3. **Проверка состояния сервисов**
   ```bash
   # На Linux/macOS
   ./scripts/health-check.sh
   
   # На Windows
   docker-compose ps
   ```

### Доступ к сервисам

- **API Gateway**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Kibana**: http://localhost:5601
- **RabbitMQ Management**: http://localhost:15672 (admin/password)

## Структура проекта

```
├── services/                    # Микросервисы
│   ├── api_gateway/            # API Gateway
│   ├── user_service/           # Сервис пользователей
│   ├── incident_service/       # Сервис инцидентов
│   ├── traffic_service/        # Сервис трафика
│   ├── news_service/           # Сервис новостей
│   ├── chat_service/           # Сервис чатов
│   ├── analytics_service/      # Сервис аналитики
│   ├── traffic_analytics_service/ # Сервис аналитики трафика
│   ├── schedule_service/       # Сервис расписания
│   └── notification_service/   # Сервис уведомлений
├── monitoring/                 # Конфигурации мониторинга
├── scripts/                    # Скрипты развертывания
├── docker-compose.yml          # Оркестрация сервисов
└── README.md                   # Документация
```

## API Endpoints

### User Service
- `POST /api/users/` - Создание пользователя
- `GET /api/users/{id}/` - Получение пользователя
- `PUT /api/users/{id}/` - Обновление пользователя
- `DELETE /api/users/{id}/` - Удаление пользователя
- `POST /api/auth/login/` - Аутентификация

### Incident Service
- `GET /api/incidents/` - Список инцидентов
- `POST /api/incidents/` - Создание инцидента
- `GET /api/incidents/{id}/` - Получение инцидента
- `PUT /api/incidents/{id}/` - Обновление инцидента
- `POST /api/appeals/` - Создание обращения

### Traffic Service
- `GET /api/traffic/` - Данные о пробках
- `GET /api/patrols/` - Список патрулей
- `GET /api/cameras/` - Список камер
- `GET /api/detectors/` - Список детекторов

## Мониторинг и логирование

### Prometheus метрики
- HTTP запросы и время ответа
- Использование ресурсов
- Состояние сервисов
- Бизнес-метрики

### Grafana дашборды
- Обзор микросервисов
- Производительность API
- Использование ресурсов
- Бизнес-аналитика

### Логирование
- Централизованное логирование через ELK Stack
- Структурированные логи в JSON формате
- Корреляция логов между сервисами

## Разработка

### Добавление нового микросервиса

1. Создайте структуру папок в `services/`
2. Реализуйте Clean Architecture слои
3. Добавьте Dockerfile
4. Обновите docker-compose.yml
5. Добавьте маршруты в API Gateway

### Структура микросервиса

```
service_name/
├── domain/              # Доменный слой
│   ├── entities.py      # Сущности
│   ├── repositories.py  # Интерфейсы репозиториев
│   └── services.py      # Доменные сервисы
├── application/         # Слой приложения
│   └── use_cases.py     # Use cases
├── infrastructure/      # Слой инфраструктуры
│   ├── repositories.py  # Реализация репозиториев
│   └── services.py      # Внешние сервисы
├── presentation/        # Слой представления
│   └── controllers.py   # Контроллеры
├── requirements.txt     # Зависимости Python
├── Dockerfile          # Docker образ
└── manage.py           # Django управление
```

## Безопасность

- JWT токены для аутентификации
- HTTPS для всех соединений
- Rate limiting на уровне API Gateway
- Валидация входных данных
- Аудит действий пользователей

## Резервное копирование

### Создание резервной копии
```bash
./scripts/backup.sh
```

### Восстановление из резервной копии
```bash
./scripts/restore.sh backup_20240101_120000.tar.gz
```

## Масштабирование

### Горизонтальное масштабирование
```bash
# Масштабирование сервиса
docker-compose up -d --scale user-service=3
```

### Вертикальное масштабирование
Обновите ресурсы в docker-compose.yml:
```yaml
services:
  user-service:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

## Troubleshooting

### Проблемы с запуском
1. Проверьте, что Docker запущен
2. Проверьте доступность портов
3. Проверьте логи: `docker-compose logs [service-name]`

### Проблемы с базой данных
1. Проверьте подключение к базе данных
2. Выполните миграции: `docker-compose exec [service] python manage.py migrate`
3. Создайте суперпользователя: `docker-compose exec [service] python manage.py createsuperuser`

### Проблемы с производительностью
1. Проверьте метрики в Grafana
2. Увеличьте ресурсы контейнеров
3. Настройте кэширование Redis

## Лицензия

MIT License

## Контрибьюция

1. Fork проекта
2. Создайте feature branch
3. Commit изменения
4. Push в branch
5. Создайте Pull Request

## Поддержка

Для получения поддержки создайте issue в репозитории или обратитесь к команде разработки.

