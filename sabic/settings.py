"""
Django settings for sabic project.
Configurado para Testagem Local, Produção no Render.com e Domínio Personalizado.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================================
# SEGURANÇA BÁSICA
# ======================================================================
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-mudar-isso-em-producao')

# ======================================================================
# CONFIGURAÇÃO DE HOSTS E DOMÍNIOS (SEGURANÇA AVANÇADA)
# ======================================================================

# 1. Busca os hosts da variável de ambiente no Render (Ex: sabicc.art, www.sabicc.art)
raw_hosts = config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(',') if h.strip()]

# 2. Adiciona o hostname automático do Render se existir
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# 3. Configuração de CSRF (Essencial para não dar erro ao enviar formulários/login)
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    if host:
        CSRF_TRUSTED_ORIGINS.append(f"https://{host}")
        CSRF_TRUSTED_ORIGINS.append(f"http://{host}")

# ======================================================================
# APPS E MIDDLEWARE
# ======================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Gerencia arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sabic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sabic.wsgi.application'

# ======================================================================
# BANCO DE DADOS (DATABASE)
# ======================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3'),
        conn_max_age=600
    )
}

# ======================================================================
# INTERNACIONALIZAÇÃO
# ======================================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'Africa/Luanda'
USE_I18N = True
USE_TZ = True

# ======================================================================
# ARQUIVOS ESTÁTICOS E MEDIA (STATIC & MEDIA)
# ======================================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Otimização de estáticos em produção
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ======================================================================
# CONFIGURAÇÕES GERAIS DO PROJETO
# ======================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.CustomUser'
LOGIN_URL = 'login'

# ======================================================================
# PROTOCOLOS DE SEGURANÇA RIGOROSA (ATIVA EM PRODUÇÃO)
# ======================================================================
if not DEBUG:
    # Força HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookies seguros
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    
    # Proteção contra ataques comuns
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 ano de HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
    