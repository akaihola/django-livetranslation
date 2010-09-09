from unittest import TestCase

from livetranslation import ugettext, ungettext, ugettext_lazy, ungettext_lazy
from livetranslation.markup import initialize


class Gettext_Tests(TestCase):
    """Tests for the custom ugettext function"""

    def test_ugettext(self):
        """ugettext marks the translation with intermediate markup"""
        initialize()
        result = ugettext('msgstr')
        self.assertEqual(result, u'[livetranslation-id 0/]')

    def test_ungettext_singular(self):
        """ungettext marks the translation with intermediate markup"""
        initialize()
        result = ungettext('msgstr', 'msgstr_plural', 1)
        self.assertEqual(result, u'[livetranslation-id 0/]')

    def test_ungettext_plural(self):
        """ungettext marks the translation with intermediate markup"""
        initialize()
        result = ungettext('msgstr', 'msgstr_plural', 2)
        self.assertEqual(result, u'[livetranslation-id 0/]')

    def test_ugettext_lazy(self):
        """ugettext_lazy marks the translation with intermediate markup"""
        initialize()
        result = ugettext_lazy('msgstr')
        self.assertEqual(
            result,
            u'[livetranslation-id 0/]')

    def test_ungettext_lazy_singular(self):
        """ungettext_lazy marks the translation with intermediate markup"""
        initialize()
        result = ungettext_lazy('msgstr', 'msgstr_plural', 1)
        self.assertEqual(
            result,
            u'[livetranslation-id 0/]')

    def test_ungettext_lazy_plural(self):
        """ungettext_lazy marks the translation with intermediate markup"""
        initialize()
        result = ungettext_lazy('msgstr', 'msgstr_plural', 2)
        self.assertEqual(
            result,
            u'[livetranslation-id 0/]')

