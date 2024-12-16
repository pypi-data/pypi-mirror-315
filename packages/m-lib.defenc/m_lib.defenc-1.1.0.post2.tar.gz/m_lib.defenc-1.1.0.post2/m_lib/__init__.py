"""Broytman Library for Python, Copyright (C) 1996-2023 PhiloSoft Design"""

from pkgutil import extend_path
import sys

__path__ = extend_path(__path__, __name__)
if sys.version_info < (3, 7):
    __import__('pkg_resources').declare_namespace(__name__)
