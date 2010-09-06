from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import (ugettext as django_ugettext,
                                      ungettext as django_ungettext,
                                      get_language)
from livetranslation.markup import TRANSLATION_ITEM_HTML, get_next_counter_value




def ugettext(message):
    return TRANSLATION_ITEM_HTML % {
        'id': 'livetranslate-%d' % get_next_counter_value(),
        'msgstr': django_ugettext(message),
        'msgid': message,
        'msgid_plural': u''}


def ungettext(singular, plural, number):
    return TRANSLATION_ITEM_HTML % {
        'id': 'livetranslate-%d' % get_next_counter_value(),
        'msgstr': django_ungettext(singular, plural, number),
        'msgid': singular,
        'msgid_plural': plural}


ungettext_lazy = lazy(ungettext, unicode)
ugettext_lazy = lazy(ugettext, unicode)
