import os
import sys

path = '/var/www/hippique.ch'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'rpc_hippique.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()