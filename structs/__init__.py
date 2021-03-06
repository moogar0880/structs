# -*- coding: utf-8 -*-

version_info = (0, 0, 2)

__title__ = 'structs'
__author__ = 'Jon Nappi'
__version__ = '.'.join([str(x) for x in version_info])
__build__ = 0x000002
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Jonathan Nappi'

try:
    from .maps import *
    from .trees import *
    from .arrays import *
except ImportError:  # Don't fail if we're grabbing the version for setup.py
    pass
