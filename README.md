# SQL Lab 4 – FastAPI проект

Цей проект демонструє реалізацію REST API з використанням FastAPI, SQLAlchemy та JWT автентифікації. Він підходить для навчання і як база для лабораторних робіт.

---

## Початкова інсталяція

### 1. Створення та налаштування проекту

```bash
# Створіть директорію для проекту
mkdir my-project
cd my-project

# Створіть віртуальне оточення
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Встановіть залежності
pip install -r requirements.txt
```

---

### 2. Структура проекту

```
src/
  ├── auth/           # Модуль автентифікації
  ├── certs/          # Сертифікати (ключі для JWT)
  ├── database.py     # Підключення до БД
  ├── config.py       # Конфігурація
  └── main.py         # Головний файл FastAPI
tests/                # Тести
```

---

### 3. Налаштування секретів

Створіть директорію та ключі для JWT:

```bash
mkdir src/certs

# Приватний ключ
openssl genrsa -out src/certs/jwt-private.pem 2048

# Публічний ключ
openssl rsa -in src/certs/jwt-private.pem -pubout -out src/certs/jwt-public.pem

# Права доступу
chmod 600 src/certs/jwt-private.pem
chmod 644 src/certs/jwt-public.pem
```

> ⚠️ Не додавайте ці файли у git.

---

### 4. Конфігурація проекту

Створіть файл `.env` у корені проекту:

```
DATABASE_URL=sqlite:///./test.db   # або URL вашої БД
SECRET_KEY=ваш_секретний_ключ
```

> FastAPI використовує ці змінні для підключення до бази та генерації токенів.

---

## Запуск проекту

```bash
# Активація віртуального оточення
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Запуск сервера у режимі розробки
uvicorn src.main:app --reload
```

> Сервер буде доступний на `http://127.0.0.1:8000`.

---

## Тестування

```bash
pytest
```

> Тести допомагають перевірити, що код працює правильно після змін.

---

## Основні поради

1. **Безпека**

   * Не комітьте `.env` та файли ключів.
   * Використовуйте змінні оточення.
   * Перевіряйте права доступу до ключів.

2. **Розробка**

   * Пишіть тести для нових функцій.
   * Використовуйте `async def` для асинхронних роутів.
   * Розділяйте код на модулі: `auth`, `database`, `routes`, `models`.
   * Документуйте API: FastAPI автоматично генерує документацію на `/docs`.

3. **FastAPI**

   * Використовуйте `Depends` для залежностей (БД, автентифікація).
   * Використовуйте Pydantic моделі для валідації даних.
   * Використовуйте `HTTPException` для обробки помилок.

---

## Корисні посилання

* [FastAPI документація](https://fastapi.tiangolo.com/)
* [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
* [JWT токени](https://jwt.io/)

---

Якщо хочеш, можу зробити **версію README з додатковими порадами та шаблонами коду**, щоб люди відразу бачили приклад правильного роуту, моделі та використання Depends. Це сильно полегшить їм старт.

Хочеш, щоб я таку версію зробив?
