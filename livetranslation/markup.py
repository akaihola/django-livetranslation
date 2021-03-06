from django.conf import settings
from django.utils import html
import re
import threading


def initialize(enabled=False):
    _thread_locals.livetranslation = {'items': {},
                                      'enabled': enabled}


def is_enabled():
    return (getattr(_thread_locals, 'livetranslation', {})
            .get('enabled', False))


_thread_locals = threading.local()
if not hasattr(_thread_locals, 'livetranslation'):
    initialize()


# the script to insert after each element which contains translated content:
TRANSLATION_ITEM_SCRIPT = (
    u'<script type="text/javascript">'
    u'jQuery("#%(id)s").livetranslate('
    u'"%(msgid)s", "%(msgid_plural)s", "%(attribute)s");'
    u'</script>')

# the intermediate translation mark-up should not contain characters which
# would be escaped by django.utils.html.escape
DEFAULT_INTERMEDIATE_MARKUP = '[livetranslation-id %(id)s/]'


def get_translation_item_markup(counter):
    return (getattr(settings, 'LIVETRANSLATION_INTERMEDIATE_MARKUP',
                    DEFAULT_INTERMEDIATE_MARKUP) % {'id': counter})


def mark_translation(singular, plural, msgstr):
    """Returns intermediate mark-up, puts translation details in threadlocals"""
    items = _thread_locals.livetranslation['items']
    counter = len(items)
    items[str(counter)] = {'singular': singular,
                           'plural': plural,
                           'msgstr': msgstr}
    return get_translation_item_markup(counter)


def get_stored_translations():
    return _thread_locals.livetranslation['items']


def get_stored_translation(counter):
    return get_stored_translations()[str(counter)]


def markup_to_regex():
    delimiter = '%()%'
    translation_markup = get_translation_item_markup(delimiter)
    parts = [re.escape(part) for part in translation_markup.split(delimiter)]
    return r'%s(\d+)%s' % tuple(parts)


ATTRIBUTE_TRANSLATION_REGEX_TEMPLATE = (
    r'<([a-zA-Z]+)'     # tag
    r'(\s+[^>]*?)'      # attrs1
    r'(\b[a-zA-Z]+)'    # attribute
    r'(\s*=\s*'         # assignment
    r'(?:[\'\"])?)'     # quote
    r'%s'               # intermediate mark-up
    r'([^>]*?)>')       # remainder

def get_attribute_translation_regex():
    """Returns the regex for matching translations in HTML tag attributes"""
    return ATTRIBUTE_TRANSLATION_REGEX_TEMPLATE % markup_to_regex()


ID_ATTR_RE = re.compile(r'\bid="(.*?)"')

def get_id_attr(attrs):
    """Returns an id="..." attribute value or None if not found in the string"""
    match = ID_ATTR_RE.search(attrs)
    if match:
        return match.group(1)


def render_translation_item_script(elem_id, singular, plural, attribute):
    return TRANSLATION_ITEM_SCRIPT % {'id': elem_id,
                                      'msgid': singular,
                                      'msgid_plural': plural,
                                      'attribute': attribute}


TRANSLATED_ATTRIBUTE_HTML = ('<%(tag)s'
                             '%(attrs1)s '
                             '%(attribute)s'
                             '%(assignment)s'
                             '%(msgstr)s'
                             '%(attrs2)s>'
                             '%(script)s')

def replace_attribute_translation(match):
    (tag, attrs1, attribute, assignment, counter, attrs2) = match.groups()
    stored_data = get_stored_translation(counter)
    elem_id = get_id_attr(attrs1) or get_id_attr(attrs2)
    if not elem_id:
        elem_id = 'livetranslation-%s' % counter
        attrs1 = ' id="%s"%s' % (elem_id, attrs1)
    script = render_translation_item_script(
        elem_id, stored_data['singular'], stored_data['plural'], attribute)
    msgstr = stored_data['msgstr']
    return TRANSLATED_ATTRIBUTE_HTML % locals()


def render_attribute_translations(html):
    regex = re.compile(get_attribute_translation_regex(), re.S)
    return re.sub(regex, replace_attribute_translation, html)


TRANSLATED_CONTENT_HTML = u'<span id="%(id)s">%(msgstr)s</span>'

def replace_content_translation(match):
    """Replaces a regex match of intermediate markup with HTML+script"""
    counter = match.group(1)
    stored_data = get_stored_translation(counter)
    elem_id = 'livetranslation-%s' % counter
    script = render_translation_item_script(
        elem_id, stored_data['singular'], stored_data['plural'], '_html')
    return '%s%s' % (TRANSLATED_CONTENT_HTML
                     % {'id': elem_id, 'msgstr': stored_data['msgstr']},
                     script)


def render_content_translations(html):
    regex = re.compile(markup_to_regex(), re.S)
    return re.sub(regex, replace_content_translation, html)


def render_translations(html):
    html = render_attribute_translations(html)
    html = render_content_translations(html)
    return html


