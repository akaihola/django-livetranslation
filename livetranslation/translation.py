from django.conf import settings
from django.utils.importlib import import_module
from django.utils import translation
import os
import polib
import sys


def get_all_translations(msgid, msgid_plural=None):
    msgstrs = []
    msgstrs_plural = []
    translations = {'singular': {'msgid': msgid,
                                 'msgstrs': msgstrs}}
    if msgid_plural:
        translations['plural'] = {'msgid': msgid_plural,
                                  'msgstrs': msgstrs_plural}
    old_language = translation.get_language()
    for langcode, language_name in settings.LANGUAGES:
        translation.activate(langcode)
        if msgid_plural:
            msgstrs.append(
                (langcode, translation.ungettext(msgid, msgid_plural, 1)))
            msgstrs_plural.append(
                (langcode, translation.ungettext(msgid, msgid_plural, 2)))
        else:
            msgstrs.append((langcode, translation.ugettext(msgid)))
    translation.activate(old_language)
    return translations


class PoFileSession(object):
    def __init__(self):
        self.files = {}
        self.modified_files = {}

        def locale_dir_for_module(module):
            return os.path.join(os.path.dirname(module.__file__), 'locale')

        paths = (
            [locale_dir_for_module(sys.modules[settings.__module__])] +
            list(settings.LOCALE_PATHS) +
            [locale_dir_for_module(import_module(appname))
             for appname in settings.INSTALLED_APPS])

        if settings.SETTINGS_MODULE is not None:
            parts = settings.SETTINGS_MODULE.split('.')
            project = import_module(parts[0])
            projectpath = locale_dir_for_module(project)
            if os.path.isdir(projectpath):
                paths.append(projectpath)

        self.paths = [os.path.join(path, '%s', 'LC_MESSAGES', 'django.po')
                      for path in paths]
        self.paths.reverse()

    def pofile_paths_for_language(self, langcode):
        for path_template in self.paths:
            yield path_template % langcode

    def for_language(self, langcode):
        for path in self.pofile_paths_for_language(langcode):
            if path not in self.files:
                self.files[path] = polib.pofile(path)
            yield self.files[path]

    def mark_modified(self, pofile):
        self.modified_files[pofile.fpath] = pofile

    def save(self):
        files = self.modified_files.values()
        for pofile in files:
            pofile.save()
            pf = os.path.splitext(pofile.fpath)[0]
            # Store the names of the .mo and .po files in an environment
            # variable, rather than doing a string replacement into the
            # command, so that we can take advantage of shell quoting, to
            # quote any malicious characters/escaping.
            # See http://cyberelk.net/tim/articles/cmdline/ar01s02.html
            os.environ['djangocompilemo'] = pf + '.mo'
            os.environ['djangocompilepo'] = pf + '.po'
            if sys.platform == 'win32': # Different shell-variable syntax
                cmd = ('msgfmt'
                       ' --check-format'
                       ' -o "%djangocompilemo%"'
                       ' "%djangocompilepo%"')
            else:
                cmd = ('msgfmt'
                       ' --check-format'
                       ' -o "$djangocompilemo"'
                       ' "$djangocompilepo"')
            os.system(cmd)
        return files


def save_translation(pofiles, msgid, langcode, translation):
    for pofile in pofiles.for_language(langcode):
        for entry in pofile:
            if entry.msgid == msgid:
                if entry.msgstr != translation:
                    entry.msgstr = translation
                    pofiles.mark_modified(pofile)
                return


def save_translations(data, pofiles):
    for number, number_data in data.items():
        msgid = number_data['msgid']

        for langcode, translation in number_data['msgstrs']:
            save_translation(pofiles, msgid, langcode, translation)

        pofiles.save()
