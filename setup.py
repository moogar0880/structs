from setuptools import setup, find_packages
from structures import __version__

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license_file = f.read()

setup(
    name='structures',
    version=__version__,
    keywords=['structures', 'data structures'],
    long_description='\n\n'.join([readme, history, license_file]),
    description='Python Data Structures for humans.',
    author='Jon Nappi',
    author_email='moogar0880@gmail.com',
    url='https://github.com/moogar0880/structures',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Utilities :: Configuration',
    ],
)