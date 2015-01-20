# -*- coding: utf-8 -*-

version_info = (0, 0, 1)

__title__ = 'structures'
__author__ = 'Jon Nappi'
__version__ = [int(x) for x in version_info]
__build__ = 0x000001
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Jonathan Nappi'

try:
    from .maps import *
    from .arrays import *
except ImportError:  # Don't fail if we're grabbing the version for setup.py
    pass
