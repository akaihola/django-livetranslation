from django.utils import html
import re
import threading


_thread_locals = threading.local()


TRANSLATION_ITEM_HTML = (
    u'<span id="%(id)s">%(msgstr)s</span>'
    u'<script type="text/javascript">'
    u'jQuery("#%(id)s").livetranslate("%(msgid)s", "%(msgid_plural)s");'
    u'</script>'
)

TRANSLATION_ITEM_ESCAPED_REGEX = '.*?'.join(
    re.escape(html.escape(part))
    for part in re.split(r'%\(.*?\)s', TRANSLATION_ITEM_HTML))


def initialize_counter():
    _thread_locals.livetranslation_counter = 0


def get_next_counter_value():
    value = getattr(_thread_locals, 'livetranslation_counter', 0)
    _thread_locals.livetranslation_counter = value + 1
    return value
