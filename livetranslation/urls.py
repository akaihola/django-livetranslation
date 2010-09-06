from django.conf.urls.defaults import *


urlpatterns = patterns(
    'livetranslation.views',

    url(regex=r'^$',
        view='get_translations',
        name='get-translations')
)
