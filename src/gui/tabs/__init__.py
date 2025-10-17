"""
Módulo de pestañas para la GUI del traductor.

Este módulo contiene las implementaciones de todas las pestañas
de la interfaz gráfica, separadas en archivos individuales para
mejor organización y mantenibilidad.
"""

from .tab_interface import TabInterface
from .text_translator_tab import TextTranslatorTab
from .file_translator_tab import FileTranslatorTab

__all__ = [
    'TabInterface',
    'TextTranslatorTab', 
    'FileTranslatorTab'
]
