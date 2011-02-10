# Django settings for rpc_hippique project.

DEBUG          = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jacques Supcik', 'jacques@supcik.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
    }
}

TIME_ZONE     = 'Europe/Zurich'
LANGUAGE_CODE = 'en-us'
SITE_ID       = 1
USE_I18N      = False
USE_L10N      = False
MEDIA_ROOT    = ''
MEDIA_URL     = ''

ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '+(=ff_&l!4jj8o6sfahwx&&!5^4)_q6m86b6=ayf0^^+#5b-#z'
TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'rpc_hippique.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
#    'django.contrib.messages',
)

MEMCACHED_HOST = '127.0.0.1:11211'
MEMCACHED_TTL = 86400
