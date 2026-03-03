py --version
python3 -m venv venv
rm -rf venv
sudo apt install python3.10-venv
sudo apt install python3-pip
source venv/bin/activate

# Atualizar o pip primeiro
pip install --upgrade pip

# Instalar Django e Django REST Framework
pip install django djangorestframework

# Instalar bibliotecas adicionais que usaremos
pip install django-cors-headers  # Para permitir requisições do frontend
pip install python-dotenv         # Para variáveis de ambiente
pip install psycopg2-binary       # Para PostgreSQL (usaremos depois)
pip install drf-yasg drf-spectacular  # Para documentação Swagger
pip install pytest pytest-django model-bakery  # Para testes (semana 9)
pip install markdown
pip install django-filter


# Listar pacotes instalados
pip list

# Ver versão do Django
python -m django --version

# Congelar as dependências atuais
pip freeze > requirements.txt

# Ver o arquivo criado
cat requirements.txt

## Iniciar projeto Django
# Criar projeto Django
django-admin startproject config .

# Criar app para posts
python manage.py startapp posts

# Criar app para usuários (opcional, pode usar o padrão)
python manage.py startapp usuarios

## Config settings.py
# No final do arquivo, adicione:
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Apps instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceiros
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    # Seus apps
    'posts',
    'usuarios',
]

# Adicionar middleware do CORS (no começo da lista)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Colocar no topo
    'django.middleware.security.SecurityMiddleware',
    # ... resto
]

# Configurar CORS (para desenvolvimento)
CORS_ALLOW_ALL_ORIGINS = True  # Apenas em desenvolvimento!

# Configurar Swagger/OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'API do blog para estudo',
    'VERSION': '1.0.0',
}

## Criar modelos
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    criado_em = models.DateTimeField(auto_now_add=True)
    publicado_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-criado_em']
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor_nome = models.CharField(max_length=100)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criado_em']
    
    def __str__(self):
        return f'Comentário de {self.autor_nome} em {self.post.titulo}'

## Criar e aplicar migrações
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

## Criar superuser
python manage.py createsuperuser

## Settings.py configs para o django framework, exemplo:
adicionar django no core/settings.py ao:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# No final do arquivo, adicione:
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Apps instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceiros
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    # Seus apps
    'posts',
    'usuarios',
]

# Adicionar middleware do CORS (no começo da lista)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Colocar no topo
    'django.middleware.security.SecurityMiddleware',
    # ... resto
]

# Configurar CORS (para desenvolvimento)
CORS_ALLOW_ALL_ORIGINS = True  # Apenas em desenvolvimento!

# Configurar Swagger/OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Blog API',
    'DESCRIPTION': 'API do blog para estudo',
    'VERSION': '1.0.0',
}

se rodar:
python manage.py runserver

vai dar erro e pedir para configurar o banco de dados.

sudo apt install pkg-config python3-dev default-libmysqlclient-dev build-essential

Explicação de cada pacote:

pkg-config: Ferramenta que o mysqlclient usa para localizar as bibliotecas MySQL -7

python3.10-dev: Cabeçalhos de desenvolvimento do Python (versão específica para seu Python 3.10.12) -1

default-libmysqlclient-dev: Bibliotecas cliente do MySQL para desenvolvimento -8

build-essential: Compiladores e ferramentas de build (gcc, make, etc.)

## instalar o MySQL client
pip install mysqlclient

## configurar banco de dados no core/settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

mkdir -p apps/{{core,accounts,customers,professionals,services}}

mkdir -p infrastructure

touch apps/__init__.py

banco de dados postgres comandos uteis:
-- Listar todos os usuários
\du

-- Ver detalhes de um usuário específico
\du salao_user

-- Alterar senha de um usuário
ALTER USER salao_user WITH PASSWORD 'nova_senha';

-- Remover usuário (cuidado!)
DROP USER salao_user;

-- Conceder superusuário (cuidado!)
ALTER USER salao_user WITH SUPERUSER;