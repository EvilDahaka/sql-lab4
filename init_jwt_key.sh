#!/bin/bash
set -e

# Створити каталог для сертифікатів
mkdir -p src/certs

# Файли ключів
PRIVATE_KEY_FILE="src/certs/jwt-private.pem"
PUBLIC_KEY_FILE="src/certs/jwt-public.pem"

# Генерація приватного ключа
openssl genrsa -out "$PRIVATE_KEY_FILE" 2048

# Генерація публічного ключа
openssl rsa -in "$PRIVATE_KEY_FILE" -pubout -out "$PUBLIC_KEY_FILE"

# Права доступу
chmod 600 "$PRIVATE_KEY_FILE"
chmod 644 "$PUBLIC_KEY_FILE"

echo "Create JWT keys"
