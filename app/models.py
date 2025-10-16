from django.db import models
import re


class Schedule(models.Model):
    class_name = models.CharField(max_length=10)
    day = models.CharField(max_length=20)
    lesson = models.CharField(blank=True, default="", max_length=50)
    homework = models.TextField(blank=True, null=True)  # Поле для домашнего задания
    lesson_order = models.IntegerField(blank=True, null=True)  # Поле для порядка урока

    def __str__(self):
        return f"{self.class_name} - {self.day} - {self.lesson} - {self.homework} - {self.lesson_order}"

    @staticmethod
    def extract_number(class_name):
        """Выделяет числовую часть class_name и возвращает её в виде числа"""
        match = re.match(r'(\d+)', class_name)
        return int(match.group(1)) if match else 0  # Если нет числа, возвращаем 0

    @staticmethod
    def extract_letter(class_name):
        """Выделяет буквенную часть class_name"""
        match = re.search(r'([A-Za-zА-Яа-я]+)$', class_name)
        return match.group(1) if match else ''  # Если нет буквы, возвращаем пустую строку


class Appeal(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}> | {'Рассмотрено' if self.is_reviewed else 'Нерассмотрено'}"


class Incident(models.Model):
    class IncidentStatus(models.TextChoices):
        NEW = 'new', 'Новое'
        IN_PROGRESS = 'in_progress', 'В работе'
        RESOLVED = 'resolved', 'Закрыто'

    class IncidentSeverity(models.TextChoices):
        LOW = 'low', 'Низкая'
        MEDIUM = 'medium', 'Средняя'
        HIGH = 'high', 'Высокая'

    title = models.CharField(max_length=200)
    description = models.TextField()
    occurred_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=IncidentStatus.choices, default=IncidentStatus.NEW)
    severity = models.CharField(max_length=10, choices=IncidentSeverity.choices, default=IncidentSeverity.MEDIUM)
    coordinates = models.JSONField(default=list, help_text="Формат: [широта, долгота]")
    related_appeal = models.ForeignKey('Appeal', null=True, blank=True, on_delete=models.SET_NULL, related_name='incidents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title} ({self.get_status_display()})"


class TrafficJam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    occurred_at = models.DateTimeField()
    coordinates = models.JSONField(default=list, help_text="Формат: [широта, долгота]")
    severity = models.CharField(max_length=10, choices=Incident.IncidentSeverity.choices, default=Incident.IncidentSeverity.MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Пробка: {self.title}"


class Patrol(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    coordinates = models.JSONField(default=list, help_text="Формат: [широта, долгота]")
    radius_m = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Патруль: {self.title}"


class Camera(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    coordinates = models.JSONField(default=list, help_text="Формат: [широта, долгота]")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Камера: {self.name}"


class NewsCategory(models.Model):
    name = models.CharField(max_length=150)
    image_url = models.URLField(blank=True, help_text="URL изображения категории")

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    cover_image_url = models.URLField(blank=True)
    author = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatThread(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='chat_threads')
    subject = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        base = self.subject or (self.user.get_username() if self.user else 'Гость')
        return f"Диалог: {base}"


class ChatMessage(models.Model):
    class Sender(models.TextChoices):
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=Sender.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_sender_display()}] {self.content[:30]}..."


class AccidentType(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#36A2EB', help_text="Hex цвет для графика")

    def __str__(self):
        return self.name


class AccidentData(models.Model):
    accident_type = models.ForeignKey(AccidentType, on_delete=models.CASCADE, related_name='accident_data')
    month = models.IntegerField(choices=[
        (1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'),
        (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'),
        (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')
    ])
    year = models.IntegerField(default=2024)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['accident_type', 'month', 'year']

    def __str__(self):
        return f"{self.accident_type.name} - {self.get_month_display()} {self.year}: {self.count}"


class AccidentStatistics(models.Model):
    total_accidents = models.IntegerField(default=0)
    injured = models.IntegerField(default=0)
    killed = models.IntegerField(default=0)
    year = models.IntegerField(default=2024)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Статистика ДТП {self.year}: {self.total_accidents} ДТП, {self.injured} ранено, {self.killed} погибло"


class WeatherData(models.Model):
    temperature = models.IntegerField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fa-sun')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.temperature}°C - {self.description}"


class TrafficForecast(models.Model):
    speed = models.IntegerField(help_text="Скорость в км/ч")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.speed} км/ч"


class RoadWorks(models.Model):
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.count} дорожных работ"


# --- Traffic graph and tracking models ---
class Detector(models.Model):
    """Physical/virtual sensor placed at a graph node.

    coordinates format: [lat, lon]
    """
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True)
    coordinates = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detector {self.external_id}"


class VehiclePass(models.Model):
    """Single detection event: vehicle passed detector at timestamp."""
    detector = models.ForeignKey(Detector, on_delete=models.CASCADE, related_name='passes')
    vehicle_id = models.CharField(max_length=100, db_index=True)
    timestamp = models.DateTimeField(db_index=True)
    speed_kmh = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['vehicle_id', 'timestamp']),
            models.Index(fields=['detector', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.vehicle_id} @ {self.detector_id} at {self.timestamp}"


class RouteCluster(models.Model):
    """Represents a discovered popular route (sequence of detector ids as path)."""
    # Store path as list of detector external_ids or database ids; using ints of Detector pk
    path = models.JSONField(default=list, help_text="Список id детекторов (pk)")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    vehicle_count = models.IntegerField(default=0)
    avg_speed_kmh = models.FloatField(null=True, blank=True)
    avg_travel_seconds = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Маршрут {len(self.path)} узлов, ТС: {self.vehicle_count}"