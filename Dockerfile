# Базовий образ з Python
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /

# Копіюємо requirements та встановлюємо залежності
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт в /src
COPY . /src/

# Встановлюємо PYTHONPATH, щоб Python бачив /src як корінь пакетів
ENV PYTHONPATH=/src

# Запускаємо FastAPI через uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
