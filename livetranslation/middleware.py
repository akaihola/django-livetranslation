from django.conf import settings
from django.utils import html
from django.utils.translation import get_language, activate, trans_real
import gettext
import re

from livetranslation.markup import (
    initialize_counter, TRANSLATION_ITEM_ESCAPED_REGEX)


DEFAULT_JQUERY_PATTERN = r'.*/jquery(?:-[\d.]+)?(?:\.min)?\.js'
DEFAULT_JQUERY_URL = ('http://ajax.googleapis.com'
                      '/ajax/libs/jquery/1.4.2/jquery.min.js')
DEFAULT_CSS_URL = '/static/css/livetranslation.css'
DEFAULT_PLUGIN_URL = '/static/js/jquery.livetranslation.js'

SCRIPT_PATTERN_TEMPLATE = r'<script\s[^>]*src="%s"'


def unescape(html):
    """
    Returns the given HTML with ampersands, quotes and angle brackets decoded.
    """
    return (html
            .replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&quot;', '"')
            .replace('&#39;', "'"))


def process_jquery_setting():
    config = getattr(settings, 'LIVETRANSLATION_JQUERY',
                     (DEFAULT_JQUERY_PATTERN, DEFAULT_JQUERY_URL))
    if config is None:
        return None, DEFAULT_JQUERY_URL
    if isinstance(config, basestring):
        pattern = SCRIPT_PATTERN_TEMPLATE % re.escape(config)
        url = config
    else:
        pattern = SCRIPT_PATTERN_TEMPLATE % config[0]
        url = config[1]
    return pattern, url


def find_jquery_link(html):
    """Returns a regex match object for the jQuery <script> tag in the HTML code

    Uses the ``LIVETRANSLATION_JQUERY`` setting for detection rules.

    Returns None if there is no matching ``<script>`` tag.
    """
    pattern, url = process_jquery_setting()
    if pattern is None:
        return True
    return re.search(pattern, html, re.I)


def insert_jquery_link(html):
    """Insert a jQuery <script src=> link into <head> of the HTML code"""
    pattern, jquery_url = process_jquery_setting()
    plugin_url = getattr(settings, 'LIVETRANSLATION_PLUGIN_URL',
                         DEFAULT_PLUGIN_URL)
    css_url = getattr(settings, 'LIVETRANSLATION_CSS_URL',
                      DEFAULT_CSS_URL)
    return re.sub(
        r'<head>',
        '<head>'
        '<script type="text/javascript" src="%s"></script>'
        '<script type="text/javascript" src="%s"></script>'
        '<link rel="stylesheet" type="text/css" href="%s"/>'
        % (jquery_url, plugin_url, css_url),
        html)


class LiveTranslationMiddleware:
    def process_request(self, request):
        if getattr(settings, 'LIVETRANSLATION', False):
            initialize_counter()
            active_language = get_language()
            trans_real._active.clear()
            trans_real._translations.clear()
            gettext._translations.clear()
            activate(active_language)

    def process_response(self, request, response):
        if getattr(settings, 'LIVETRANSLATION', False):
            if not find_jquery_link(response.content):
                response.content = insert_jquery_link(response.content)
            response.content = re.sub(TRANSLATION_ITEM_ESCAPED_REGEX,
                                      lambda match: unescape(match.group()),
                                      response.content)
        return response
