import os

from pathlib import Path

from datetime import timedelta

import pymysql


# =====================================
# MYSQL
# =====================================

pymysql.install_as_MySQLdb()


# =====================================
# BASE DIR
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================
# SECURITY
# =====================================

SECRET_KEY = 'django-insecure-6$0262ukx4yktok!b1^azcxoy6+1dtpe!x3k6%c#37sy)u*&v8'

DEBUG = True

ALLOWED_HOSTS = ['*']


# =====================================
# INSTALLED APPS
# =====================================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'corsheaders',

    'ventas',
]


# =====================================
# MIDDLEWARE
# =====================================

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =====================================
# URLS
# =====================================

ROOT_URLCONF = 'ecommerce_rest.urls'


# =====================================
# TEMPLATES
# =====================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =====================================
# WSGI
# =====================================

WSGI_APPLICATION = 'ecommerce_rest.wsgi.application'


# =====================================
# DATABASE MYSQL AWS RDS
# =====================================

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'ecommercedb',

        'USER': 'admin',

        'PASSWORD': 'Inacap16037',

        'HOST': 'db-ecommerce.cofwqqw6kbyn.us-east-1.rds.amazonaws.com',

        'PORT': '3306',

        'OPTIONS': {

            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# =====================================
# PASSWORD VALIDATORS
# =====================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =====================================
# LANGUAGE
# =====================================

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# =====================================
# STATIC FILES
# =====================================

STATIC_URL = 'static/'


# =====================================
# DEFAULT PRIMARY KEY
# =====================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================================
# DJANGO REST FRAMEWORK
# =====================================

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (

        'rest_framework.permissions.IsAuthenticated',
    ),
}


# =====================================
# JWT
# =====================================

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),

    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer',),
}


# =====================================
# CORS
# =====================================

CORS_ALLOW_ALL_ORIGINS = True