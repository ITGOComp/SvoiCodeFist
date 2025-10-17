# API Examples

## User Service

### Создание пользователя
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user"
  }'
```

### Аутентификация
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

### Получение пользователя
```bash
curl -X GET http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Incident Service

### Создание инцидента
```bash
curl -X POST http://localhost:8000/api/incidents/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "ДТП на перекрестке",
    "description": "Столкновение двух автомобилей",
    "occurred_at": "2024-01-15T10:30:00Z",
    "severity": "high",
    "coordinates": [55.7558, 37.6176]
  }'
```

### Создание обращения
```bash
curl -X POST http://localhost:8000/api/appeals/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "email": "ivan@example.com",
    "message": "Проблема с дорожным покрытием на улице Ленина"
  }'
```

## Traffic Service

### Получение данных о пробках
```bash
curl -X GET http://localhost:8000/api/traffic/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Получение списка патрулей
```bash
curl -X GET http://localhost:8000/api/patrols/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Получение списка камер
```bash
curl -X GET http://localhost:8000/api/cameras/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## News Service

### Получение категорий новостей
```bash
curl -X GET http://localhost:8000/api/news/categories/
```

### Получение статей по категории
```bash
curl -X GET http://localhost:8000/api/news/categories/1/articles/
```

### Создание статьи
```bash
curl -X POST http://localhost:8000/api/news/articles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category_id": 1,
    "title": "Новые правила дорожного движения",
    "author": "Редактор",
    "summary": "Краткое описание статьи",
    "content": "Полный текст статьи...",
    "cover_image_url": "https://example.com/image.jpg"
  }'
```

## Chat Service

### Отправка сообщения
```bash
curl -X POST http://localhost:8000/api/chat/send/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "Здравствуйте, у меня вопрос по дорожной ситуации",
    "subject": "Вопрос по дорогам"
  }'
```

### Получение сообщений
```bash
curl -X GET http://localhost:8000/api/chat/messages/?thread_id=1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Analytics Service

### Получение статистики ДТП
```bash
curl -X GET http://localhost:8000/api/analytics/accident-stats/
```

### Обновление статистики ДТП
```bash
curl -X POST http://localhost:8000/api/analytics/accident-stats/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "total_accidents": 150,
    "injured": 45,
    "killed": 3,
    "year": 2024
  }'
```

## Traffic Analytics Service

### Загрузка детекторов
```bash
curl -X POST http://localhost:8000/api/traffic-analytics/ingest/detectors/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@detectors.csv"
```

### Загрузка данных о проездах
```bash
curl -X POST http://localhost:8000/api/traffic-analytics/ingest/passes/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@vehicle_passes.csv"
```

### Анализ сопутствующего движения
```bash
curl -X GET "http://localhost:8000/api/traffic-analytics/comovement/?vehicle_id=ABC123&k=3&dt=300" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Кластеризация маршрутов
```bash
curl -X GET "http://localhost:8000/api/traffic-analytics/cluster-routes/?start=2024-01-01T00:00:00Z&end=2024-01-01T23:59:59Z&top=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Schedule Service

### Получение расписания
```bash
curl -X GET http://localhost:8000/api/schedule/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Создание урока
```bash
curl -X POST http://localhost:8000/api/schedule/lessons/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "class_name": "10А",
    "day": "Понедельник",
    "lesson": "Математика",
    "homework": "Решить задачи 1-10",
    "lesson_order": 1
  }'
```

## Notification Service

### Отправка уведомления
```bash
curl -X POST http://localhost:8000/api/notifications/send/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": 1,
    "type": "email",
    "subject": "Новое сообщение в чате",
    "message": "У вас новое сообщение от администратора"
  }'
```

## Health Checks

### Проверка здоровья API Gateway
```bash
curl -X GET http://localhost:8000/health
```

### Проверка здоровья всех сервисов
```bash
curl -X GET http://localhost:8000/services/health
```

### Проверка здоровья конкретного сервиса
```bash
curl -X GET http://localhost:8001/health  # User Service
curl -X GET http://localhost:8002/health  # Incident Service
curl -X GET http://localhost:8003/health  # Traffic Service
```

## Примеры с использованием Python

### Создание клиента для работы с API
```python
import requests
import json

class TrafficMonitoringClient:
    def __init__(self, base_url="http://localhost:8000", token=None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })
    
    def login(self, username, password):
        response = self.session.post(
            f"{self.base_url}/api/auth/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}'
            })
            return data
        return None
    
    def create_incident(self, title, description, coordinates, severity="medium"):
        response = self.session.post(
            f"{self.base_url}/api/incidents/",
            json={
                "title": title,
                "description": description,
                "coordinates": coordinates,
                "severity": severity,
                "occurred_at": "2024-01-15T10:30:00Z"
            }
        )
        return response.json()
    
    def get_traffic_data(self):
        response = self.session.get(f"{self.base_url}/api/traffic/")
        return response.json()

# Использование
client = TrafficMonitoringClient()
client.login("admin", "password")
incident = client.create_incident(
    "Пробка на МКАД",
    "Затор в районе выезда на Ярославское шоссе",
    [55.7558, 37.6176],
    "high"
)
```

## Примеры с использованием JavaScript

### Создание клиента для работы с API
```javascript
class TrafficMonitoringClient {
    constructor(baseUrl = 'http://localhost:8000', token = null) {
        this.baseUrl = baseUrl;
        this.token = token;
    }
    
    async login(username, password) {
        const response = await fetch(`${this.baseUrl}/api/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.token = data.token;
            return data;
        }
        return null;
    }
    
    async createIncident(title, description, coordinates, severity = 'medium') {
        const response = await fetch(`${this.baseUrl}/api/incidents/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({
                title,
                description,
                coordinates,
                severity,
                occurred_at: new Date().toISOString()
            })
        });
        
        return await response.json();
    }
    
    async getTrafficData() {
        const response = await fetch(`${this.baseUrl}/api/traffic/`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        
        return await response.json();
    }
}

// Использование
const client = new TrafficMonitoringClient();
await client.login('admin', 'password');
const incident = await client.createIncident(
    'Пробка на МКАД',
    'Затор в районе выезда на Ярославское шоссе',
    [55.7558, 37.6176],
    'high'
);
```

