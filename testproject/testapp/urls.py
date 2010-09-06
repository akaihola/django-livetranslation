from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'testapp.views',

    url(regex=r'^$', view='frontpage'),
)
