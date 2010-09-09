from livetranslation.tests.settings_helpers import patch_settings
from mock import Mock, patch
import os
from unittest import TestCase

from livetranslation.translation import get_all_translations, PoFileSession


class GetAllTranslations_Tests(TestCase):
    """Tests for livetranslation.translation.get_all_translations()"""

    def test_ugettext_singular(self):
        """get_all_translations() calls ugettext for only-singular msgids"""
        data = {'ugettext_calls': []}

        def activate(langcode, data=data):
            data['langcode'] = langcode

        def ugettext(msgid, data=data):
            data['ugettext_calls'].append((msgid, data['langcode']))
            return '%s in %s' % (msgid, data['langcode'])

        with patch('django.utils.translation.activate', activate):
            with patch('django.utils.translation.ugettext', ugettext):
                with patch_settings(LANGUAGES=(('fi', 'Finnish'),
                                               ('sv', 'Swedish'))):
                    translations = get_all_translations('a message id')
        self.assertEqual(data['ugettext_calls'],
                         [('a message id', 'fi'), ('a message id', 'sv')])

    def test_ungettext_singular(self):
        """get_all_translations() doesn't call ungettext for singular msgids"""
        with patch('django.utils.translation.ungettext') as ungettext:
            with patch_settings(LANGUAGES=(('fi', 'Finnish'),)):
                translations = get_all_translations('a message id')
        self.assertFalse(ungettext.called)

    def test_ungettext_plural(self):
        """get_all_translations() calls ungettext for msgids with plurals"""
        data = {'ungettext_calls': []}

        def activate(langcode, data=data):
            data['langcode'] = langcode

        def ungettext(msgid, msgid_plural, count, data=data):
            data['ungettext_calls'].append(
                (msgid, msgid_plural, count, data['langcode']))
            return '%s/%s(%d) in %s' % (
                msgid, msgid_plural, count, data['langcode'])

        with patch('django.utils.translation.activate', activate):
            with patch('django.utils.translation.ungettext', ungettext):
                with patch_settings(LANGUAGES=(('fi', 'Finnish'),
                                               ('sv', 'Swedish'))):
                    translations = get_all_translations('a message id',
                                                        'plural message id')
        self.assertEqual(data['ungettext_calls'],
                         [('a message id', 'plural message id', 1, 'fi'),
                          ('a message id', 'plural message id', 2, 'fi'),
                          ('a message id', 'plural message id', 1, 'sv'),
                          ('a message id', 'plural message id', 2, 'sv')])

    def test_ugettext_plural(self):
        """get_all_translations() doesn't call ugettext for plural msgids"""
        with patch('django.utils.translation.ugettext') as ugettext:
            with patch_settings(LANGUAGES=(('fi', 'Finnish'),)):
                translations = get_all_translations('a message id',
                                                    'plural message id')
        self.assertFalse(ugettext.called)

    def test_results_singular(self):
        """get_all_translations() gives good translations for singular msgids"""
        get_language = Mock(return_value='en-us')

        data = {}

        def activate(langcode, data=data):
            data['langcode'] = langcode

        def ugettext(msgid, data=data):
            return '%s in %s' % (msgid, data['langcode'])

        with patch('django.utils.translation.activate', activate):
            with patch('django.utils.translation.ugettext', ugettext):
                with patch_settings(LANGUAGES=(('fi', 'Finnish'),
                                               ('sv', 'Swedish'))):
                    translations = get_all_translations('a message id')
        self.assertEqual(translations.keys(), ['singular'])
        self.assertEqual(translations['singular']['msgid'], 'a message id')
        self.assertEqual(translations['singular']['msgstrs'],
                         [('fi', 'a message id in fi'),
                          ('sv', 'a message id in sv')])

    def test_restores_old_language(self):
        """get_all_translations() restores old active language"""
        get_language = Mock(return_value='old language')
        with patch('django.utils.translation.get_language', get_language):
            with patch('django.utils.translation.activate') as activate:
                with patch_settings(LANGUAGES=(('fi', 'Finnish'),)):
                    get_all_translations('a message id')
        self.assertEqual(activate.call_args,
                         (('old language',), {}))


class PoFileSession_Tests(TestCase):
    """Tests for the PoFileSession class"""

    import django
    import livetranslation
    root_directories = {
        # Django root
        'dj': os.path.dirname(django.__file__),
        # django-livetranslation distribution root
        'lt': os.path.abspath(os.path.join(
            os.path.dirname(livetranslation.__file__),
            '..'))}

    def test_path_templates(self):
        """PoFileSession has a complete set of path templates for .po files"""
        session = PoFileSession()
        d = self.root_directories
        self.assertEqual(
            [os.path.abspath(path) for path in session.paths],
            ['%(lt)s/testproject/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(lt)s/testproject/testapp/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(lt)s/livetranslation/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/sessions/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/contenttypes/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/admin/locale/%%s/LC_MESSAGES/django.po' % d,
             '%(dj)s/conf/locale/%%s/LC_MESSAGES/django.po' % d])

    def test_paths_for_language(self):
        """PoFileSession generates a complete set of paths for .po files"""
        session = PoFileSession()
        d = self.root_directories
        files = [os.path.abspath(filepath)
                 for filepath in session.pofile_paths_for_language('xx')]
        self.assertEqual(
            files,
            ['%(lt)s/testproject/locale/xx/LC_MESSAGES/django.po' % d,
             '%(lt)s/testproject/testapp/locale/xx/LC_MESSAGES/django.po' % d,
             '%(lt)s/livetranslation/locale/xx/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/sessions/locale/xx/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/contenttypes/locale/xx/LC_MESSAGES/django.po' % d,
             '%(dj)s/contrib/admin/locale/xx/LC_MESSAGES/django.po' % d,
             '%(dj)s/conf/locale/xx/LC_MESSAGES/django.po' % d])
