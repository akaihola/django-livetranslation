from django.conf import settings
from django.utils import html
from django.utils.translation import get_language, activate, trans_real
import gettext
import re

from livetranslation.markup import initialize, is_enabled, render_translations


DEFAULT_JQUERY_PATTERN = r'.*/jquery(?:-[\d.]+)?(?:\.min)?\.js'
DEFAULT_JQUERY_URL = ('http://ajax.googleapis.com'
                      '/ajax/libs/jquery/1.4.2/jquery.min.js')
DEFAULT_CSS_URL = '/static/css/livetranslation.css'
DEFAULT_PLUGIN_URL = '/static/js/jquery.livetranslation.js'

SCRIPT_PATTERN_TEMPLATE = r'<script\s[^>]*src="%s"'

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

#def unescape(html):
#    """
#    Returns the given HTML with ampersands, quotes and angle brackets decoded.
#    """
#    return (html
#            .replace('&amp;', '&')
#            .replace('&lt;', '<')
#            .replace('&gt;', '>')
#            .replace('&quot;', '"')
#            .replace('&#39;', "'"))


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


def insert_jquery_link(html, jquery=True):
    """Insert a jQuery <script src=> link into <head> of the HTML code"""
    pattern, jquery_url = process_jquery_setting()
    plugin_url = getattr(settings, 'LIVETRANSLATION_PLUGIN_URL',
                         DEFAULT_PLUGIN_URL)
    css_url = getattr(settings, 'LIVETRANSLATION_CSS_URL',
                      DEFAULT_CSS_URL)
    insert = [
        ('<script type="text/javascript" src="%s"></script>' % jquery_url)
        if jquery else '',
        '<script type="text/javascript" src="%s"></script>' % plugin_url,
        '<link rel="stylesheet" type="text/css" href="%s"/>' % css_url,
        '<head>']
    return re.sub(r'</head>', ''.join(insert), html)


class LiveTranslationMiddleware:

    def is_turned_on(self, request):
        return (getattr(settings, 'LIVETRANSLATION', False)
                and request.session.get('livetranslation-enable'))

    def process_request(self, request):
        initialize(self.is_turned_on(request))
        if is_enabled():
            active_language = get_language()
            trans_real._active.clear()
            trans_real._translations.clear()
            gettext._translations.clear()
            activate(active_language)

    def process_response(self, request, response):
        if (is_enabled() and
            response['Content-Type'].split(';')[0] in _HTML_TYPES):

            jquery_found = find_jquery_link(response.content)
            response.content = insert_jquery_link(response.content,
                                                  not jquery_found)
            response.content = render_translations(
                response.content.decode('UTF-8')).encode('UTF-8')
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)

        return response
