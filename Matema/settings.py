from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY')

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = [config('HOST_DEV')]

CSRF_COOKIE_DOMAIN = config('HOST_DEV')

CORS_ORIGIN_WHITELIST = (
    config('HOST_DEV'),
)

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    'corsheaders',
    'djoser',
    'drf_yasg',
    'social_django',
    'django_apscheduler',

    'Statistic',
    'Task',
    'User.apps.UserConfig',
    'Manager'
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'Matema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'Matema.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('SQL_ENGINE'),
        'NAME': config('SQL_NAME'),
        'USER': config('SQL_USER'),
        'PASSWORD': config('SQL_PASSWORD'),
        'HOST': config('SQL_HOST'),
        'PORT': config('SQL_PORT'),
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===     AUTH CREDENTIALS     === #

AUTH_USER_MODEL = 'User.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework.authentication.TokenAuthentication',
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),

    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=3),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
}

DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,  # We use only JWT
    'ACTIVATION_URL': 'auth/verify/{uid}/{token}/',
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['https://matema-dev-ncrzmugb6q-lm.a.run.app/task/all',
                                          'http://127.0.0.1:8000/task/all/',
                                          'http://127.0.0.1:8000/',
                                          'http://127.0.0.1:8000'
                                          ],
    "SERIALIZERS": {
        'user_create': 'User.serializers.CustomUserCreateSerializer',
    },
}
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = [
    'https://matema-dev-ncrzmugb6q-lm.a.run.app/task/all',
    'http://127.0.0.1:8000/task/all/',
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000'
]

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

# ===     EMAIL CREDENTIALS     === #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'matema.group@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# ===     GOOGLE CREDENTIALS     === #

GOOGLE_OAUTH2_CLIENT_ID = (config('GOOGLE_OAUTH2_CLIENT_ID'),)
GOOGLE_OAUTH2_CLIENT_SECRET = (config('GOOGLE_OAUTH2_CLIENT_SECRET'),)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

# ===     GITHUB CREDENTIALS     === #

SOCIAL_AUTH_GITHUB_CLIENT_ID = config('SOCIAL_AUTH_GITHUB_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')
