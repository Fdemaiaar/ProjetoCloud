#!/bin/bash

set -e

echo "Aguardando o Postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Postgres iniciado"

# Verificar se o diretório migrations existe
if [ ! -d "/app/migrations" ]; then
  echo "Diretório migrations não encontrado. Inicializando migrações..."
  flask db init
  flask db migrate -m "Inicializar banco de dados"
fi

echo "Aplicando migrações..."
flask db upgrade

echo "Iniciando a aplicação..."
exec "$@"
