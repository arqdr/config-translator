"""
Конфигурационный транслятор - преобразует учебный конфигурационный язык в TOML.
"""

__version__ = '1.0.0'
__author__ = 'Student'

from .cli import main
from .transformer import ConfigTransformer