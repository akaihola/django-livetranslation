from mock import Mock, patch
from unittest import TestCase

from livetranslation.views import get_translations


class GetTranslations_GET_Tests(TestCase):
    """Tests for the get_translations view"""

    def setUp(self):
        request = Mock()
        request.method = 'GET'
        request.GET = {'msgid': 'the-msgid'}
        get_all_translations = Mock(return_value={"dummy": "json"})
        with patch('livetranslation.views.get_all_translations',
                   get_all_translations):
            self.response = get_translations(request)

    def test_response_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_json_content(self):
        self.assertEqual(self.response.content, '{"dummy": "json"}')

    def test_content_type(self):
        self.assertEqual(self.response['Content-Type'], 'application/json')


class GetTranslations_POST_Tests(TestCase):
    """Tests for the get_translations view"""

    def setUp(self):
        request = Mock()
        request.method = 'POST'
        request.POST = {'livetranslation-popup-0-msgid': 'the-msgid',
                        'livetranslation-popup-0-en': 'the-msgstr'}
        with patch('livetranslation.views.save_translations') as save:
            self.response = get_translations(request)
        self.save_translations = save

    def test_response_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_json_content(self):
        self.assertEqual(self.response.content, 'OK')

    def test_content_type(self):
        self.assertEqual(self.response['Content-Type'], 'text/plain')

    def test_calls_save_translations(self):
        self.assertTrue(self.save_translations.called)

    def test_save_translations_arguments(self):
        (((data, pof), kwargs),) = self.save_translations.call_args_list
        self.assertEqual(data, {'0': {'msgstrs': [('en', 'the-msgstr')],
                                      'msgid': 'the-msgid'}})
