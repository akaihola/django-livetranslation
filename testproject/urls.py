from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    (r'^admin/', include(admin.site.urls)),
    (r'^livetranslation/', include('livetranslation.urls')),
    (r'^', include('testapp.urls')),
    url(regex=r'^static/(?P<path>.*)$',
        view='django.views.static.serve',
        kwargs={'document_root': settings.STATIC_ROOT})
)
