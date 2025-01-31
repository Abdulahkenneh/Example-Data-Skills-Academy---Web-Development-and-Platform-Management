"""
Django settings for newblogs project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from dotenv import load_dotenv
from pathlib import Path
import os
import django_heroku
import dj_database_url
from decouple import config
from google.cloud import storage
from google.oauth2 import service_account
from base64 import b64decode
from decouple import config
import comments

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY =config('SECRET_KEY')

# settings.py


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =config('DEBUG') =='True'

# Application definition
# GOOGLE CLOUD STORAGE SETTING
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'data-analytic-bucket'  # Provide your bucket name here
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'demon/demon.json')
)

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'


SITE_ID = 1
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogs',
    'widget_tweaks',
    'django_extensions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'tinymce',
    'pythonIDE',
    'logusers',
    'django_quill',
     'quiz',
    'django_summernote',
    'multichoice',
    'true_false',
    'essay',
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'newblogs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates','static'],
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

WSGI_APPLICATION = 'newblogs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

import django.utils.translation as original_translation
original_translation.ugettext = original_translation.gettext

# db_rom_env = dj_database_url.config('conn_max_age=600')
# DATABASES['default'].update(db_rom_env)

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


STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
#MEDIA_URL ='media/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
X_FRAME_OPTIONS = 'SAMEORIGIN'



SUMMERNOTE_CONFIG = {
    'summernote': {
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            'theme': 'monokai',
        },
        'width': '100%',
        'height': '400',
        'css': (
            '<style>.note-editor .note-editable pre code {'
            'background-color: #000; '
            'color: #fff; '
            'padding: 10px; '
            'border-radius: 5px; '
            'overflow-x: auto; '
            'white-space: pre; '
            'font-family: "Courier New", Courier, monospace;'
            '}</style>',
        ),
    },
    'attachment_require_authentication': False,
    'disable_attachment': False,
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'blogs.backends.EmailOrUsernameModelBackend',  # Ensure this is the correct path
]

# Extend session cookie age to 1 day (86400 seconds)
SESSION_COOKIE_AGE = 86400

# Make sessions expire when the user closes the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGING_URL ='/logusers/login/'



#code mirror ide setting

CODEMIRROR_SETTINGS = {
    'theme':'material',
    'lineNumbers':True,
}


#APPEND_SLASH = False
# Activate Django-Heroku.
django_heroku.settings(locals())