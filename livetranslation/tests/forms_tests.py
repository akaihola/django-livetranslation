from unittest import TestCase

from livetranslation.forms import extract_form_data


class Forms_Tests(TestCase):
    """Tests for form helpers"""

    def test_msgid(self):
        """extract_form_data gets msgid from POST"""
        post = {'livetranslation-popup-0-msgid': 'msgid-0'}
        data = extract_form_data(post)
        self.assertEqual(data, {'0': {'msgid': 'msgid-0'}})

    def test_multiple_msgid(self):
        """extract_form_data gets multiple msgids from POST"""
        post = {'livetranslation-popup-0-msgid': 'msgid-0',
                'livetranslation-popup-1-msgid': 'msgid-1'}
        data = extract_form_data(post)
        self.assertEqual(data, {'1': {'msgid': 'msgid-1'},
                                '0': {'msgid': 'msgid-0'}})

    def test_msgstrs(self):
        """extract_form_data gets msgstrs from POST"""
        post = {'livetranslation-popup-0-en': 'in English',
                'livetranslation-popup-0-fi': 'in Finnish'}
        data = extract_form_data(post)
        self.assertEqual(
            data,
            {'0': {'msgstrs': [('fi', 'in Finnish'), ('en', 'in English')]}})

    def test_complete(self):
        """extract_form_data gets msgstrs from POST"""
        post = {'livetranslation-popup-0-msgid': 'msgid-0',
                'livetranslation-popup-1-msgid': 'msgid-1',
                'livetranslation-popup-0-en': 'in English',
                'livetranslation-popup-0-fi': 'in Finnish',
                'livetranslation-popup-1-en': 'England',
                'livetranslation-popup-1-fi': 'Finland'}
        data = extract_form_data(post)
        self.assertEqual(
            data,
            {'1': {'msgstrs': [('fi', 'Finland'), ('en', 'England')],
                   'msgid': 'msgid-1'},
             '0': {'msgstrs': [('en', 'in English'), ('fi', 'in Finnish')],
                   'msgid': 'msgid-0'}})

