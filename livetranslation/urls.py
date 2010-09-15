from django.conf.urls.defaults import *


urlpatterns = patterns(
    'livetranslation.views',

    url(regex=r'^$',
        view='get_translations',
        name='get-translations'),

    url(regex=r'^on/$',
        view='enable',
        name='enable-translations'),

    url(regex=r'^off/$',
        view='disable',
        name='disable-translations'),
)
