import os
PROJECT_ROOT = os.path.join(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'livetranslation.sqlite'),
    }
}

LANGUAGES = (
    ('en', 'English'),
    ('fi', 'Finnish'),
    ('sv', 'Swedish'),
)

LIVETRANSLATION = True

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, '..', 'livetranslation', 'media')

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'livetranslation.middleware.LiveTranslationMiddleware',
)

ROOT_URLCONF = 'testproject.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'livetranslation',
    'testapp',
    #'django_extensions',  # for development
)
