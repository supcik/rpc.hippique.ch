from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'.*', 'register.rpc_handler'),
)
