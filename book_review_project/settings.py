"""
Django settings for book_review_project project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['intense-beach-72172-d0f0c923b977.herokuapp.com', 'localhost', '127.0.0.1']
# django-debug-toolbar
INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
	'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #local
	'users.apps.UsersConfig',
    'blog.apps.BlogConfig',
    # third party
    'crispy_forms',
	'crispy_bootstrap5',
    'allauth',
    'allauth.account',
	'debug_toolbar',
	'django_bleach',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'book_review_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'book_review_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
ON_HEROKU = 'DYNO' in os.environ

if ON_HEROKU:
	# Heroku PostgreSQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_URL'),
        }
    }

else:	
	# Local development configuration
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': 'Mydb',
			'USER': env('DBUSER'),
			'PASSWORD':env('DBPASSWORD'), 
			'HOST': 'localhost',
			'PORT': 5432
		}
	}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = [
"django.contrib.staticfiles.finders.FileSystemFinder",
"django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'

#LOGOUT_REDIRECT_URL = 'home'

# django-allauth config
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend', 
)

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


DEFAULT_FROM_EMAIL = 'admin@strongbookreviews.com'

#Django bleach settings
BLEACH_ALLOWED_TAGS =['p', 'b', 'i', 'u', 'em','br', 'strong', 'a','img', 'h3', 'h4', 'h5', 'h6']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'style']
BLEACH_ALLOWED_STYLES = ['font-family', 'font-weight', 'text-decoration', 'font-variant']
BLEACH_ALLOWED_PROTOCOLS = ['https']
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True

ENVIRONMENT=env('ENVIRONMENT',default='development')

if ENVIRONMENT == 'production':
	#XSS broswer protection
	SECURE_BROWSER_XSS_FILTER = True
	X_FRAME_OPTIONS = 'DENY'
	SECURE_SSL_REDIRECT = True
	SECURE_HSTS_SECONDS = 3600 
	SECURE_HSTS_INCLUDE_SUBDOMAINS = True 
	SECURE_HSTS_PRELOAD = True 
	SECURE_CONTENT_TYPE_NOSNIFF = True
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Heroku database config from dj_database_url
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)