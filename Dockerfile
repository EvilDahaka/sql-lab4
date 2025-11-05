FROM python:3.12-slim

WORKDIR /src

RUN pip install --no-cache-dir fastapi

COPY . /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
