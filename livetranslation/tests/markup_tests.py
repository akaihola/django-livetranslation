from mock import Mock, patch
import re
from unittest import TestCase

from livetranslation.markup import (initialize,
                                    get_translation_item_markup,
                                    mark_translation,
                                    get_stored_translations,
                                    get_stored_translation,
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
        markup = '[%(id)d/]'
        with patch_settings(LIVETRANSLATION_INTERMEDIATE_MARKUP=markup):
            markup = get_translation_item_markup(1)
        self.assertEqual(markup, '[1/]')


class MarkTranslation_Tests(TestCase):
    """Tests for mark_translation()"""

    def test_returns_correct_markup(self):
        """mark_translation returns correct mark-up"""
        marked = mark_translation('singular', 'plural', 'msgstr')
        self.assertEqual(marked, '[livetranslation-id 1/]')

    def test_stores_details_in_threadlocals(self):
        """mark_translation stores translation details in threadlocals"""
        initialize()
        mark_translation('singular', 'plural', 'msgstr')
        self.assertEqual(get_stored_translations(),
                         {'0': {'msgstr': 'msgstr',
                                'plural': 'plural',
                                'singular': 'singular'}})


class GetAttributeTranslationRegex_Tests(TestCase):
    """Tests for get_attribute_translation_regex()"""

    def test_builds_a_good_regex(self):
        """get_attribute_translation_regex() builds a good regex"""
        with patch('livetranslation.markup.get_translation_item_markup',
                   Mock(return_value=r'[%()%]')):
            regex = get_attribute_translation_regex()
        self.assertEqual(
            regex,
            r'<([a-zA-Z]+)'
            r'(\s+[^>]*?)'
            r'(\b[a-zA-Z]+)'
            r'(\s*=\s*'
            r'(?:[\'\"])?)'
            r'\[(\d+)\]'
            r'([^>]*?)>')


class MarkupToRegex_Tests(TestCase):
    """Tests for markup_to_regex()"""

    def test_escapes_markup_and_replaces_groups(self):
        """markup_to_regex escapes mark-up and replaces groups"""
        with patch('livetranslation.markup.get_translation_item_markup',
                   Mock(return_value='[%()%]')):
            regex = markup_to_regex()
        self.assertEqual(regex, r'\[(\d+)\]')


class MarkupRegex_Tests(TestCase):
    """Tests for the default intermediate mark-up regex"""

    def test_multiline(self):
        """multiline"""
        markup = '[livetranslation-id 9/]'
        regex = re.compile(markup_to_regex(), re.S)
        replaced = re.sub(regex, 'DUMMY', markup)
        self.assertEqual(replaced, 'DUMMY')


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
             r'\[(\d+)\]'
             r'([^>]*?)>')

    def test_adds_id(self):
        """render_attribute_translations adds a missing element id"""
        html = ('<input'
                ' type="text"'
                ' value="[0]"'
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
                ' translation="[0]"/>')
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
        match.group.return_value = '0'
        replacement = replace_content_translation(match)
        self.assertEqual(
            replacement,
            u'<span id="livetranslation-0">msgstr</span>'
            u'<script type="text/javascript">'
            u'jQuery("#livetranslation-0").livetranslate('
            u'"singular", "plural", "_html");'
            u'</script>')


class RenderContentTranslations_Tests(TestCase):
    regex = r'\[(\d+)\]'

    def test_content(self):
        """render_content_translations renders a translation correctly"""
        html = '<tag>[0]</tag>'
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
