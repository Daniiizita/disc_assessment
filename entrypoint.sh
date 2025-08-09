#!/bin/bash

# Aguarda o banco de dados estar disponível
echo "Aguardando banco de dados..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "Banco de dados conectado!"

# Executa migrações
python manage.py migrate

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia o servidor
exec "$@"