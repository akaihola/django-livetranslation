from setuptools import setup

setup(
    name = 'django-livetranslation',
    version = '0.1',
    packages = ['livetranslation'],
    author = 'Antti Kaihola',
    author_email = 'akaihol+django@ambitone.com',
    description = ('Edit translations of a site UI on the site itself'),
    url = 'http://github.com/akaihola/django-livetranslation/tree/master',
    download_url = ('http://www.github.com/akaihola/django-livetranslation/'
                    'tarball/0.1'),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development'),
)
