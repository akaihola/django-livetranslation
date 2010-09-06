"""
So you need to change some settings when running an individual test in a test
case. You could just wrap the test between ``old_value = settings.MY_SETTING``
and ``settings.MY_SETTING = old_value``. This snippet provides a helper which
makes this a bit more convenient, since settings are restored to their old
values automatically.

Example usage::

    class MyTestCase(TestCase):

        def test_something(self):
            with patch_settings(MY_SETTING='my value',
                                OTHER_SETTING='other value'):
                do_my_test()

http://djangosnippets.org/snippets/2156/
"""

from contextlib import contextmanager


class SettingDoesNotExist:
    pass


@contextmanager
def patch_settings(**kwargs):
    from django.conf import settings
    old_settings = []
    for key, new_value in kwargs.items():
        old_value = getattr(settings, key, SettingDoesNotExist)
        old_settings.append((key, old_value))
        setattr(settings, key, new_value)
    yield
    for key, old_value in old_settings:
        if old_value is SettingDoesNotExist:
            delattr(settings, key)
        else:
            setattr(settings, key, old_value)
