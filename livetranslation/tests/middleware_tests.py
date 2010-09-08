from django.test import TestCase
from mock import Mock, patch

from livetranslation.middleware import (process_jquery_setting,
                                        find_jquery_link,
                                        insert_jquery_link,
                                        DEFAULT_JQUERY_PATTERN,
                                        DEFAULT_JQUERY_URL)
from livetranslation.tests.settings_helpers import patch_settings


NO_JQUERY = u'<html><head></head></html>'
HAS_JQUERY = (u'<html><head>'
              u'<script type="text/javascript" src="/jquery.js" />'
              u'</head></html>')


class ProcessJquerySetting_Tests(TestCase):
    """Tests for middleware.process_jquery_setting()"""

    def test_none_pattern(self):
        """LIVETRANSLATION_JQUERY == None -> pattern == None"""
        with patch_settings(LIVETRANSLATION_JQUERY=None):
            pattern, url = process_jquery_setting()
        self.assertEqual(pattern, None)

    def test_default_url(self):
        """LIVETRANSLATION_JQUERY == None -> default URL"""
        with patch_settings(LIVETRANSLATION_JQUERY=None):
            pattern, url = process_jquery_setting()
        self.assertEqual(
            url,
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js')

    def test_string_pattern(self):
        """LIVETRANSLATION_JQUERY is a string, base pattern on it"""
        with patch_settings(LIVETRANSLATION_JQUERY=u'/jquery.js'):
            pattern, url = process_jquery_setting()
        self.assertEqual(pattern, ur'<script\s[^>]*src="\/jquery\.js"')

    def test_string_url(self):
        """LIVETRANSLATION_JQUERY is a string, use as the jQuery URL"""
        with patch_settings(LIVETRANSLATION_JQUERY=u'/jquery.js'):
            pattern, url = process_jquery_setting()
        self.assertEqual(url, '/jquery.js')


class FindJqueryLink_Tests(TestCase):
    """Tests for middleware.find_jquery_link()"""

    def test_never_load_jquery_setting(self):
        """LIVETRANSLATION_JQUERY == None -> always assume jQuery is loaded"""
        with patch_settings(LIVETRANSLATION_JQUERY=None):
            result = find_jquery_link(NO_JQUERY)
        self.assertEqual(result, True)

    def test_custom_string_match(self):
        """LIVETRANSLATION_JQUERY is a string, match <script> tag"""
        with patch_settings(LIVETRANSLATION_JQUERY=u'/jquery.js'):
            result = find_jquery_link(HAS_JQUERY)
        self.assertEqual(result.start(), 12)
        self.assertEqual(result.end(), 59)

    def test_custom_string_no_match(self):
        """LIVETRANSLATION_JQUERY is a string, no match for <script> tag"""
        with patch_settings(LIVETRANSLATION_JQUERY=u'/jquery.js'):
            result = find_jquery_link(NO_JQUERY)
        self.assertEqual(result, None)

    def test_default_match(self):
        """LIVETRANSLATION_JQUERY is the default, match <script> tag"""
        config = (DEFAULT_JQUERY_PATTERN, 'DUMMY')
        with patch_settings(LIVETRANSLATION_JQUERY=config):
            result = find_jquery_link(HAS_JQUERY)
        self.assertEqual(result.start(), 12)
        self.assertEqual(result.end(), 59)

    def test_default_no_match(self):
        """LIVETRANSLATION_JQUERY is the default, no match for <script> tag"""
        config = (DEFAULT_JQUERY_PATTERN, 'DUMMY')
        with patch_settings(LIVETRANSLATION_JQUERY=config):
            result = find_jquery_link(NO_JQUERY)
        self.assertEqual(result, None)


class InsertJqueryLink_Tests(TestCase):
    """Tests for middleware.find_jquery_link()"""

    def test_default(self):
        """"""
        config = ('DUMMY', DEFAULT_JQUERY_URL)
        with patch_settings(LIVETRANSLATION_JQUERY=config):
            result = insert_jquery_link(NO_JQUERY)
        self.assertEqual(
            result,
            u'<html><head>'
            u'<script type="text/javascript" src="'
            u'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">'
            u'</script>'
            u'<script type="text/javascript"'
            u' src="/static/js/jquery.livetranslation.js"></script>'
            u'<link rel="stylesheet" type="text/css"'
            u' href="/static/css/livetranslation.css"/>'
            u'</head></html>')

    def test_custom(self):
        """"""
        config = ('DUMMY', '/jquery.js')
        with patch_settings(LIVETRANSLATION_JQUERY=config):
            result = insert_jquery_link(NO_JQUERY)
        self.assertEqual(
            result,
            u'<html><head>'
            u'<script type="text/javascript" src="/jquery.js"></script>'
            u'<script type="text/javascript"'
            u' src="/static/js/jquery.livetranslation.js"></script>'
            u'<link rel="stylesheet" type="text/css"'
            u' href="/static/css/livetranslation.css"/>'
            u'</head></html>')
