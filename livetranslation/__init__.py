from django.utils.functional import lazy
from django.utils.translation import *
from livetranslation.markup import is_enabled, mark_translation


django_ugettext = ugettext

def ugettext(message):
    translation = django_ugettext(message)
    if not is_enabled():
        return translation
    return mark_translation(message, u'', translation)


django_ungettext = ungettext

def ungettext(singular, plural, number):
    translation = django_ungettext(singular, plural, number)
    if not is_enabled():
        return translation
    return mark_translation(singular, plural, translation)


ungettext_lazy = lazy(ungettext, unicode)  # pragma: no cover
ugettext_lazy = lazy(ugettext, unicode)    # pragma: no cover
