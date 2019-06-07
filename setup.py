#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command


NAME = 'njinn-sample-app'
DESCRIPTION = 'Njinn Sample Application'
AUTHOR = 'Njinn Technologies GmbH'
EMAIL = 'contact@njinn.io'
REQUIRES_PYTHON = '>=3.7'
VERSION = '0.1.6'
REQUIRED = []
EXTRAS = {}


here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
        ('username=', None, 'Specify the username for PyPi.'),
        ('password=', None, 'Password to authenticate the user.'),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print(s)

    def initialize_options(self):
        self.username = None
        self.password = None

    def finalize_options(self):
        assert self.username, 'Invalid username!'
        assert self.password, 'Invalid password!'

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload --repository-url https://test.pypi.org/legacy/ -u {0} -p {1} dist/*'.format(self.username, self.password))

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=['app'],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    entry_points={},
    include_package_data=True,
    license='Other/Proprietary License',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
