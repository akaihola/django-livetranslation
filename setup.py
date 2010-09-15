from setuptools import setup

setup(
    name = 'django-livetranslation',
    version = '0.3',
    packages = ['livetranslation', 'livetranslation.templatetags'],
    author = 'Antti Kaihola',
    author_email = 'akaihol+django@ambitone.com',
    description = ('Edit translations of a site UI on the site itself'),
    url = 'http://github.com/akaihola/django-livetranslation/tree/master',
    download_url = (
        'http://github.com/downloads/akaihola/django-livetranslation'),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'),
)
