from django.conf.urls.defaults import *
import rcp_hippique.register

urlpatterns = patterns('',
    (r'.*', 'rpc_hippique.register.rpc_handler'),
)
