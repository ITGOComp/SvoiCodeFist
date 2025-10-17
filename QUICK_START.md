# 🚀 Быстрый запуск SvoiCode

## ⚡ Мгновенный запуск

```bash
# 1. Активируйте виртуальное окружение
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac

# 2. Запустите быстрый старт
python quick_start.py
```

**Или пошагово:**

```bash
# 1. Активируйте виртуальное окружение
venv\Scripts\activate

# 2. Выполните миграции
python manage.py migrate

# 3. Запустите сервер
python manage.py runserver
```

## 🌐 Доступ к сайту

После запуска откройте в браузере:
- **Главная страница:** http://localhost:8000
- **Админ панель:** http://localhost:8000/admin

## 🔧 Режимы работы

### Текущий режим: Локальная база данных
- ✅ Работает без микросервисов
- ✅ Использует SQLite базу данных
- ✅ Все функции доступны

### Переключение на микросервисы:
```bash
# Включить микросервисы
python manage.py toggle_microservices --enable

# Перезапустить сервер
python manage.py runserver
```

### Переключение обратно на локальную БД:
```bash
# Отключить микросервисы
python manage.py toggle_microservices --disable

# Перезапустить сервер
python manage.py runserver
```

## 🚨 Если что-то не работает

### Ошибка "Not Found":
1. Убедитесь, что микросервисы отключены:
   ```bash
   python manage.py toggle_microservices --disable
   ```

2. Перезапустите сервер:
   ```bash
   python manage.py runserver
   ```

### Ошибка "DisallowedHost":
```bash
python fix_django_settings.py
```

### Проблемы с базой данных:
```bash
python manage.py migrate
```

## 📊 Проверка статуса

```bash
# Проверить настройки
python manage.py toggle_microservices --status

# Проверить микросервисы (если включены)
python manage.py microservice_status
```

## 🎯 Что вы увидите

После успешного запуска вы увидите:
- **Главную страницу** с мониторингом трафика
- **Навигационное меню** с разделами
- **Панель управления** для администраторов
- **API endpoints** для разработчиков

---

**Готово! Ваш сайт работает! 🎉**
