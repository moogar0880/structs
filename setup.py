#!/usr/bin/env python

import os
import sys

import structures

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'structures',
    'structures.maps',
    'structures.arrays',
]

requires = []

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license_file = f.read()

setup(
    name='structures',
    version=structures.__version__,
    keywords=['structures', 'data structures'],
    long_description='\n\n'.join([readme, history, license_file]),
    description='Python Data Structures for humans.',
    author='Jon Nappi',
    author_email='moogar0880@gmail.com',
    url='https://github.com/moogar0880/structures',
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',

    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Utilities :: Configuration',
    ],
)