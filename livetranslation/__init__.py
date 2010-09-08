from django.utils.functional import lazy
from django.utils.translation import (ugettext as django_ugettext,
                                      ungettext as django_ungettext)
from livetranslation.markup import mark_translation


def ugettext(message):
    return mark_translation(message, u'', django_ugettext(message))


def ungettext(singular, plural, number):
    return mark_translation(singular, plural,
                            django_ungettext(singular, plural, number))


ungettext_lazy = lazy(ungettext, unicode)  # pragma: no cover
ugettext_lazy = lazy(ugettext, unicode)    # pragma: no cover
