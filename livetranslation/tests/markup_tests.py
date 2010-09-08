from mock import Mock, patch
from unittest import TestCase

from livetranslation.markup import (get_translation_item_markup,
                                    mark_translation,
                                    markup_to_regex,
                                    get_attribute_translation_regex,
                                    replace_attribute_translation,
                                    render_attribute_translations,
                                    replace_content_translation,
                                    render_content_translations
                                    )
from livetranslation.tests.settings_helpers import patch_settings


class GetTranslationItemMarkup_Tests(TestCase):
    """Tests for get_translation_item_markup()"""

    def test_substitution(self):
        """substitution"""
        markup = '[%(id)d:%(singular)s:%(plural)s:%(msgstr)s/]'
        with patch_settings(LIVETRANSLATION_INTERMEDIATE_MARKUP=markup):
            markup = get_translation_item_markup(
                1, 'singular', 'plural', 'msgstr')
        self.assertEqual(markup, '[1:singular:plural:msgstr/]')


class MarkTranslation_Tests(TestCase):
    """Tests for mark_translation()"""

    def test_x(self):
        marked = mark_translation('singular', 'plural', 'msgstr')
        self.assertEqual(
            marked,
            '[livetranslation-id 1/]'
            '[livetranslation-singular]singular[/livetranslation-singular]'
            '[livetranslation-plural]plural[/livetranslation-plural]'
            '[livetranslation-msgstr]msgstr[/livetranslation-msgstr]')


class GetAttributeTranslationRegex_Tests(TestCase):
    """Tests for get_attribute_translation_regex()"""

    def test_builds_a_good_regex(self):
        """get_attribute_translation_regex() builds a good regex"""
        with patch('livetranslation.markup.get_translation_item_markup',
                   Mock(return_value=r'[%()%:%()%:%()%:%()%]')):
            regex = get_attribute_translation_regex()
        self.assertEqual(
            regex,
            r'<([a-zA-Z]+)'
            r'(\s+[^>]*?)'
            r'(\b[a-zA-Z]+)'
            r'(\s*=\s*'
            r'(?:[\'\"])?)'
            r'\[(\d+)\:(.*?)\:(.*?)\:(.*?)\]'
            r'([^>]*?)>')


class MarkupToRegex_Tests(TestCase):
    """Tests for markup_to_regex()"""

    def test_escapes_markup_and_replaces_groups(self):
        """markup_to_regex escapes mark-up and replaces groups"""
        with patch('livetranslation.markup.get_translation_item_markup',
                   Mock(return_value='[%()%:%()%:%()%:%()%]')):
            regex = markup_to_regex()
        self.assertEqual(regex, r'\[(\d+)\:(.*?)\:(.*?)\:(.*?)\]')


class ReplaceAttributeTranslation_Tests(TestCase):
    def test_adds_id(self):
        """replace_attribute_translation adds a missing element id"""
        match = Mock()
        match.groups.return_value = (
            'tag',
            ' attr1="val1"',
            'translation',
            '="',
            '0',
            'singular',
            'plural',
            'msgstr',
            '" attr3="val3" /')
        replacement = replace_attribute_translation(match)
        self.assertEqual(
            replacement,
            u'<tag id="livetranslation-0"'
            u' attr1="val1" translation="msgstr" attr3="val3" />'
            u'<script type="text/javascript">'
            u'jQuery("#livetranslation-0").livetranslate('
            u'"singular", "plural", "translation");'
            u'</script>')

    def test_existing_id(self):
        """replace_attribute_translation reuses an existing element id"""
        match = Mock()
        match.groups.return_value = (
            'tag',
            ' id="the-id"',
            'translation',
            '="',
            '0',
            'singular',
            'plural',
            'msgstr',
            '"/')
        replacement = replace_attribute_translation(match)
        self.assertEqual(
            replacement,
            u'<tag id="the-id" translation="msgstr"/>'
            u'<script type="text/javascript">'
            u'jQuery("#the-id").livetranslate('
            u'"singular", "plural", "translation");'
            u'</script>')

    def test_existing_trailing_id(self):
        """replace_attribute_translation reuses trailing existing element id"""
        match = Mock()
        match.groups.return_value = (
            'input',
            '',
            'value',
            '="',
            '0',
            'singular',
            'plural',
            'msgstr',
            '" id="the-id"/')
        replacement = replace_attribute_translation(match)
        self.assertEqual(
            replacement,
            u'<input value="msgstr" id="the-id"/>'
            u'<script type="text/javascript">'
            u'jQuery("#the-id").livetranslate('
            u'"singular", "plural", "value");'
            u'</script>')


class RenderAttributeTranslations_Tests(TestCase):
    regex = (r'<([a-zA-Z]+)'
             r'(\s+[^>]*?)'
             r'(\b[a-zA-Z]+)'
             r'(\s*=\s*'
             r'(?:[\'\"])?)'
             r'\[(\d+)\:(.*?)\:(.*?)\:(.*?)\]'
             r'([^>]*?)>')

    def test_adds_id(self):
        """render_attribute_translations adds a missing element id"""
        html = ('<input'
                ' type="text"'
                ' value="[0:singular:plural:msgstr]"'
                ' size="20" />')
        with patch('livetranslation.markup.get_attribute_translation_regex',
                   Mock(return_value=self.regex)):
            result = render_attribute_translations(html)
        self.assertEqual(
            result,
            u'<input'
            u' id="livetranslation-0"'
            u' type="text" '
            u' value="msgstr"'
            u' size="20" />'
            u'<script type="text/javascript">'
            u'jQuery("#livetranslation-0").livetranslate('
            u'"singular", "plural", "value");'
            u'</script>')

    def test_existing_id(self):
        """render_attribute_translations re-uses an existing element id"""
        html = ('<tag'
                ' id="the-id"'
                ' translation="[0:singular:plural:msgstr]"/>')
        with patch('livetranslation.markup.get_attribute_translation_regex',
                   Mock(return_value=self.regex)):
            result = render_attribute_translations(html)
        self.assertEqual(
            result,
            u'<tag id="the-id"  translation="msgstr"/>'
            u'<script type="text/javascript">'
            u'jQuery("#the-id").livetranslate('
            u'"singular", "plural", "translation");'
            u'</script>')


class ReplaceContentTranslation_Tests(TestCase):
    def test_content(self):
        """replace_content_translation"""
        match = Mock()
        match.groups.return_value = ('0', 'singular', 'plural', 'msgstr')
        replacement = replace_content_translation(match)
        self.assertEqual(
            replacement,
            u'<span id="livetranslation-0">msgstr</span>'
            u'<script type="text/javascript">'
            u'jQuery("#livetranslation-0").livetranslate('
            u'"singular", "plural", "_html");'
            u'</script>')


class RenderContentTranslations_Tests(TestCase):
    regex = r'\[(\d+)\:(.*?)\:(.*?)\:(.*?)\]'

    def test_content(self):
        """render_content_translations renders a translation correctly"""
        html = '<tag>[0:singular:plural:msgstr]</tag>'
        with patch('livetranslation.markup.markup_to_regex',
                   Mock(return_value=self.regex)):
            result = render_content_translations(html)
        self.assertEqual(
            result,
            u'<tag>'
            u'<span id="livetranslation-0">msgstr</span>'
            u'<script type="text/javascript">'
            u'jQuery("#livetranslation-0").livetranslate('
            u'"singular", "plural", "_html");'
            u'</script>'
            u'</tag>')



class RenderTranslations_Tests(TestCase):
    """Tests for middleware translation rendering"""

    def test_x(self):
        """x"""
        pass
