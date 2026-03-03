#!/bin/bash

echo "🔄 Resetando banco de dados..."

# Resetar banco
sudo -u postgres psql -d salao_erp -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

echo "✅ Banco resetado"

echo "🔄 Removendo migrações antigas..."
rm -f */migrations/0*.py
rm -rf */migrations/__pycache__

echo "✅ Migrações removidas"

echo "🔄 Criando novas migrações..."
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations customers
python manage.py makemigrations professionals
python manage.py makemigrations services
python manage.py makemigrations scheduling
python manage.py makemigrations financial
python manage.py makemigrations products
python manage.py makemigrations inventory

echo "✅ Migrações criadas"

echo "🔄 Aplicando migrações na ordem correta..."
python manage.py migrate accounts
python manage.py migrate contenttypes
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate sessions
python manage.py migrate

echo "🎉 Banco de dados configurado com sucesso!"
