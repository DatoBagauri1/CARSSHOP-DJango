from pathlib import Path
import os
import dj_database_url
from decouple import config # რეკომენდირებულია .env ფაილისთვის

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# იყენებს გარემოს ცვლადს (Environment Variable)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure--4yrgk@gnu5e3clif*ki9^reqp#jfw)wg=21etf2ultrxeq#o)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS-ის და CSRF_TRUSTED_ORIGINS-ის განახლება
ALLOWED_HOSTS = ['.render.com', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://*.render.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # საჭიროა დეპლოიმენტისთვის სტატიკური ფაილების სამართავად
    'whitenoise.runserver_nostatic', 
    'shop',
    'widget_tweaks',
    'storages', # AWS S3-სთვის
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Whitenoise-ის დამატება Static Files-ის მართვისთვის
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

ROOT_URLCONF = 'ExoticCarsShowroom.urls'

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

WSGI_APPLICATION = 'ExoticCarsShowroom.wsgi.application'


# Database - იყენებს PostgreSQL-ს Render-ზე
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# ლოკალურად გაშვებისას, თუ DATABASE_URL არ არსებობს, გამოიყენებს SQLite-ს
if not os.environ.get('DATABASE_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Static Root-ის დამატება Render-ისთვის
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTHENTICATION SETTINGS
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'


# =========================================================
# 🖼️ MEDIA (AWS S3) SETTINGS
# =========================================================

# S3 Settings გამოიყენება მხოლოდ Production-ში (როდესაც ცვლადები არსებობს)
if os.environ.get('AWS_ACCESS_KEY_ID'):
    
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    
    # Bucket-ის მისამართის ფორმატირება
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Django-ს უთხარი, რომ გამოიყენოს S3 მედია ფაილებისთვის
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# თუ S3 არ არის კონფიგურირებული, გამოიყენე ლოკალური ფაილ სისტემა
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


# =========================================================
# 🔒 PRODUCTION SECURITY SETTINGS
# =========================================================

if not DEBUG:
    # უზრუნველყოფს, რომ HTTP მოთხოვნები გადამისამართდეს HTTPS-ზე
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    
    # უზრუნველყოფს Cookie-ების გაგზავნას მხოლოდ HTTPS-ის მეშვეობით
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True