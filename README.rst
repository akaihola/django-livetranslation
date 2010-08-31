========================
 django-livetranslation
========================

This re-usable Django app enables non-technical website owners to translate the
user interface of their site, *on* the site itself.

It works for websites which are created with Django_ and use Django's
`internationalization framework`_.

When a site is in "live translation" mode, a "translate" button and a
translation editor pop-up window are automatically created for each translate
string on a page.  The button appears when the mouse pointer touches the
translated text.  Clicking on the button opens the translation editor pop-up
window, which displays the original string with editable translations in
different languages.

When translations are modified in the pop-up window, the changes are saved back
into the original gettext ``.po`` files on the server.  Any changes to the
translation in the active language are immediately updated on the page.

When in live translation mode, the website re-compiles any changed ``.po``
files and reloads all compiled ``.mo`` files on every request.  This has a
considerable effect on performance, so the live translation mode should only be
used on non-public instances of the site.

If the source code for the website is managed with a version control system on
the server, the changes can be committed to a local branch and pushed to a
remote server.  This is done with a simple "upload changes" link in a
management interface.  Alternatively, the changes can be e-mailed to a
developer as a diff file.

.. _Django: http://djangoproject.com/
.. _internationalization framework: http://docs.djangoproject.com/en/1.2/topics/i18n/


==============
 Installation
==============

Django-livetranslation requires the ``polib`` Python package, which can be
installed from the Python Package Index using ``easy_install``::

    easy_install polib

Clone the django-livetranslation source code from GitHub::

    git clone http://github.com/akaihola/django-livetranslation

Install the app::

    cd django-livetranslation
    python setup.py install

If you have the ``pip`` package installer, you can simply::

    pip install polib
    pip install -e git+git://github.com/akaihola/django-livetranslation.git#livetranslation


===============
 Configuration
===============

You'll need to activate a special middleware, the backend app and the live
translation mode in your ``settings.py``::

    MIDDLEWARE_CLASSES = (
        ...
        'livetranslation.middleware.LiveTranslationMiddleware',
    )

    INSTALLED_APPS = (
        ...
        'livetranslation',
    )

    LIVETRANSLATION = True

<The middleware adds JavaScript on every HTML page and loads the jQuery
library from the Google CDN.  See `Loading jQuery`_ below for customization instructions.

For instructions on how to enable internationalization support in your Django
project, see the Django documentation on

* `Internationalization and localization`_ 
* `Using internationalization in your own projects`_
* `Deployment of translations`_


.. _Internationalization and localization: http://docs.djangoproject.com/en/1.2/topics/i18n/
.. _Using internationalization in your own projects: http://docs.djangoproject.com/en/1.2/howto/i18n/#using-translations-in-your-own-projects
.. _Deployment of translations: http://docs.djangoproject.com/en/1.2/topics/i18n/deployment/


=======
 Usage
=======

In your templates, instead of ``{% load i18n %}`` load the modified
internationalization template tags.  They replace Django's own tags and are
used similarly::

    {% load livetranslation_tags %}

    {% trans "Original string" %}
    {% blocktrans %}Original string{% endblocktrans %}

In your Python code, import the translation functions from
django-livetranslation instead of Django.  An example view::

    from django.shortcuts import render_to_response
    from livetranslation import ugettext as _

    def myview(request):
        return render_to_response('mytemplate.html',
	                          {'myvar': _(u'Original string')})

An example model::

    from django.db import models
    from livetranslation import ugettext_lazy as _

    class MyModel(models.Model):
        myfield = models.TextField(help_text=_(u'Original text'))


================
 Loading jQuery
================

The middleware tries to be smart and detect if jQuery is already being loaded
on the page by looking for a ``<script>`` tag with a familiar-looking ``src=``
URL.  It matches the filename part of the URL in the following forms:

* ``jquery.js``
* ``jquery.min.js``
* ``jquery-<version>.js``
* ``jquery-<version>.min.js``

The match is case insensitive and ``<version>`` can contain digits and periods.

If a matching ``<script>`` tag is not found, one is inserted to load jQuery
1.4.2 from the Google CDN.

If the detection doesn't work correctly for you or you want to customize the
jQuery URL, you can customize the process in ``settings.py``::

    # never load jQuery
    LIVETRANSLATION_JQUERY = None

    # load the provided URL if it isn't already loaded
    LIVETRANSLATION_JQUERY = '/path/jQuery-strangefilename.js'

    # if the regex doesn't match a <script> tag, load the given URL
    LIVETRANSLATION_JQUERY = (r'.*/jquery-1\.4\.2(?:-min)?\.js',  # src= regex
                              '/path/jquery-1.4.2.min.js')        # URL

