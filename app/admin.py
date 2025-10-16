from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import IntegerField, CharField
from django.db.models.functions import Cast, Substr
from .models import Schedule, Appeal, Incident, TrafficJam, Patrol, Camera, NewsCategory, Article, ChatThread, ChatMessage, AccidentType, AccidentData, AccidentStatistics, WeatherData, TrafficForecast, RoadWorks

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_name', 'day', 'lesson', 'lesson_order', 'homework')
    list_filter = ('class_name', 'day')
    search_fields = ('class_name', 'lesson', 'homework')
    list_editable = ('class_name', 'day', 'lesson', 'homework', 'lesson_order')
    list_display_links = ('id',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            class_num=Cast(Substr('class_name', 1, 2), IntegerField()),  # Берем первые два символа и делаем int
            class_letter=Substr('class_name', 3, 1)  # Берем 3-й символ (букву)
        ).order_by('-class_num', '-class_letter', 'lesson_order')

admin.site.register(Schedule, ScheduleAdmin)


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_reviewed', 'created_at')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_reviewed',)
    readonly_fields = ('created_at',)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'severity', 'status', 'occurred_at', 'related_appeal', 'created_at')
    list_filter = ('severity', 'status', 'occurred_at', 'created_at')
    search_fields = ('title', 'description')
    autocomplete_fields = ('related_appeal',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'occurred_at', 'coordinates')
        }),
        ('Состояние', {
            'fields': ('status', 'severity')
        }),
        ('Связи', {
            'fields': ('related_appeal',)
        }),
        ('Служебные', {
            'fields': ('created_at', 'updated_at')
        })
    )


@admin.register(TrafficJam)
class TrafficJamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'severity', 'occurred_at', 'created_at')
    list_filter = ('severity', 'occurred_at', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'occurred_at', 'coordinates')
        }),
        ('Состояние', {
            'fields': ('severity',)
        }),
        ('Служебные', {
            'fields': ('created_at',)
        })
    )


@admin.register(Patrol)
class PatrolAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'radius_m', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'coordinates', 'radius_m')
        }),
        ('Служебные', {
            'fields': ('created_at',)
        })
    )


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'coordinates')
        }),
        ('Служебные', {
            'fields': ('created_at',)
        })
    )


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_url')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'author', 'summary', 'content')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'cover_image_url', 'author', 'summary', 'content')
        }),
        ('Служебные', {
            'fields': ('created_at',)
        })
    )


@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'is_closed', 'created_at')
    list_filter = ('is_closed', 'created_at')
    search_fields = ('subject', 'user__username')
    readonly_fields = ('created_at',)
    inlines = []

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('created_at',)

ChatThreadAdmin.inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)


@admin.register(AccidentType)
class AccidentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    search_fields = ('name',)


@admin.register(AccidentData)
class AccidentDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_type', 'month', 'year', 'count')
    list_filter = ('accident_type', 'month', 'year')
    search_fields = ('accident_type__name',)
    list_editable = ('count',)


@admin.register(AccidentStatistics)
class AccidentStatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'total_accidents', 'injured', 'killed', 'updated_at')
    list_filter = ('year', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature', 'description', 'icon', 'updated_at')
    list_editable = ('temperature', 'description', 'icon')
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если нет записей
        return not WeatherData.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление последней записи
        return WeatherData.objects.count() > 1


@admin.register(TrafficForecast)
class TrafficForecastAdmin(admin.ModelAdmin):
    list_display = ('id', 'speed', 'updated_at')
    list_editable = ('speed',)
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если нет записей
        return not TrafficForecast.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление последней записи
        return TrafficForecast.objects.count() > 1


@admin.register(RoadWorks)
class RoadWorksAdmin(admin.ModelAdmin):
    list_display = ('id', 'count', 'updated_at')
    list_editable = ('count',)
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Разрешаем добавление только если нет записей
        return not RoadWorks.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление последней записи
        return RoadWorks.objects.count() > 1


# Регистрируем пользователей в админке
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
