# Проект кінотеатру - REST API на FastAPI

## Опис проекту
Розробка REST API для системи управління кінотеатром з використанням FastAPI, SQLAlchemy та JWT автентифікації.

## Технічний стек
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- JWT для автентифікації
- Pydantic для валідації
- Базова інтеграція з платіжною системою (mock)

## API Endpoints

### 1. Автентифікація та користувачі
```http
# Реєстрація нового користувача
POST /auth/register
{
    "email": "user@example.com",
    "password": "securepass",
    "full_name": "John Doe"
}

# Логін користувача
POST /auth/login
{
    "email": "user@example.com",
    "password": "securepass"
}

# Отримання профілю
GET /users/me
Authorization: Bearer <jwt_token>

# Оновлення профілю
PATCH /users/me
Authorization: Bearer <jwt_token>
{
    "full_name": "New Name"
}
```

### 2. Події та сеанси
```http
# Отримання списку подій
GET /events?page=1&size=10

# Деталі конкретної події
GET /events/{event_id}

# Створення події (тільки адмін)
POST /events
Authorization: Bearer <jwt_token>
{
    "title": "Avatar 2",
    "description": "...",
    "start_time": "2024-01-01T19:00:00Z",
    "duration_minutes": 180,
    "price": 200.00
}

# Оновлення події (тільки адмін)
PATCH /events/{event_id}

# Видалення події (тільки адмін)
DELETE /events/{event_id}
```

### 3. Місця та бронювання
```http
# План залу з доступними місцями
GET /events/{event_id}/seats

# Резервування місця
POST /events/{event_id}/seats/{seat_id}/reserve
```

### 4. Квитки
```http
# Купівля квитка
POST /tickets/purchase
{
    "event_id": 1,
    "seat_id": 1,
    "payment_method": "card"
}

# Список квитків користувача
GET /tickets/my

# Деталі квитка
GET /tickets/{ticket_id}

# Скасування квитка
POST /tickets/{ticket_id}/cancel
```

### 5. Оплата
```http
# Ініціювання платежу
POST /payments/initiate
{
    "ticket_id": 1,
    "amount": 200.00
}

# Вебхук від платіжної системи
POST /payments/webhook
```

## Структура проекту

```
src/
  ├── auth/              # Автентифікація
  │   ├── service.py     # Бізнес-логіка аутентифікації
  │   ├── router.py      # Роути auth
  │   ├── repository.py  # Робота з БД
  │   └── schemas.py     # Pydantic моделі
  │
  ├── events/            # Управління подіями
  │   ├── service.py     # Бізнес-логіка подій
  │   ├── router.py      # Роути подій
  │   ├── repository.py  # Робота з БД
  │   └── schemas.py     # Pydantic моделі
  │
  ├── tickets/           # Управління квитками
  │   ├── service.py     # Бізнес-логіка квитків
  │   ├── router.py      # Роути квитків
  │   ├── repository.py  # Робота з БД
  │   └── schemas.py     # Pydantic моделі
  │
  ├── payments/          # Платіжна система
  │   ├── service.py     # Бізнес-логіка оплат
  │   ├── router.py      # Платіжні роути
  │   └── schemas.py     # Pydantic моделі
  │
  ├── certs/            # JWT ключі
  ├── database.py       # Налаштування БД
  ├── config.py         # Конфігурація
  └── main.py          # Головний файл FastAPI
```

## Сервіси (бізнес-логіка)

1. **AuthService**
   - Реєстрація користувачів
   - Хешування паролів
   - Логін та генерація JWT
   - Валідація токенів

2. **EventService**
   - Управління подіями
   - Перевірка доступності
   - Фільтрація та пошук

3. **TicketService**
   - Створення квитків
   - Перевірка доступності місць
   - Скасування бронювань

4. **PaymentService**
   - Інтеграція з платіжною системою
   - Обробка платежів
   - Обробка вебхуків

5. **TaskService** (фонові завдання)
   - Очищення прострочених бронювань
   - Відправка нагадувань
   - Генерація звітів

## Критерії оцінювання

1. **Функціональність (40%)**
   - Працююча автентифікація
   - Коректна робота з квитками
   - Інтеграція оплат

2. **Якість коду (30%)**
   - Структура проекту
   - Обробка помилок
   - Документація

3. **Безпека (30%)**
   - Захист від вразливостей
   - Валідація даних
   - Правильна робота з JWT

## Додаткові завдання

1. Додати систему знижок
2. Реалізувати пошук по подіях
3. Додати систему відгуків
4. Налаштувати кешування
5. Додати систему сповіщень
