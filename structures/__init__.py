# -*- coding: utf-8 -*-

version_info = (0, 0, 1)
__author__ = 'Jon Nappi'
__version__ = [int(x) for x in version_info]

try:
    from .maps import *
    from .arrays import *
except ImportError:  # Don't fail if we're grabbing the version for setup.py
    pass
