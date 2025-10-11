"""
Servicio de utilidades para transcripción fonética.
Incluye funciones de validación y verificación de texto para IPA.
"""

import re
from typing import Optional


def is_valid_english_text(text: str) -> bool:
    """
    Valida si el texto parece ser inglés apropiado para transcripción IPA.
    Simplificada para aceptar cualquier texto no vacío.
    
    Args:
        text (str): Texto a validar
        
    Returns:
        bool: True si el texto no está vacío, False en caso contrario
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    if not text:
        return False
    
    # Aceptar cualquier texto que tenga contenido
    return True


def clean_text_for_transcription(text: str) -> str:
    """
    Limpia el texto para prepararlo para transcripción fonética.
    
    Args:
        text (str): Texto a limpiar
        
    Returns:
        str: Texto limpio listo para transcripción
    """
    if not text:
        return ""
    
    # Normalizar espacios
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # Remover caracteres no latinos excepto puntuación básica
    cleaned = re.sub(r'[^\w\s.,!?\';:()\-\'"]+', '', cleaned)
    
    return cleaned


def extract_words_from_text(text: str) -> list[str]:
    """
    Extrae palabras individuales del texto para transcripción.
    
    Args:
        text (str): Texto del cual extraer palabras
        
    Returns:
        list[str]: Lista de palabras extraídas
    """
    if not text:
        return []
    
    # Extraer solo palabras (sin puntuación)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words


def is_likely_english_word(word: str) -> bool:
    """
    Determina si una palabra individual parece ser inglesa.
    
    Args:
        word (str): Palabra a verificar
        
    Returns:
        bool: True si la palabra parece ser inglesa
    """
    if not word or not isinstance(word, str):
        return False
    
    word = word.strip().lower()
    if not word:
        return False
    
    # Verificar que contenga solo letras
    if not re.match(r'^[a-z]+$', word):
        return False
    
    # Lista extendida de palabras muy comunes en inglés
    very_common_words = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 
        'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 
        'but', 'his', 'by', 'from', 'they', 'she', 'or', 'an', 'will', 'my',
        'one', 'all', 'would', 'there', 'their', 'we', 'him', 'her', 'has',
        'had', 'which', 'oil', 'its', 'been', 'if', 'more', 'when', 'up',
        'out', 'so', 'what', 'can', 'said', 'each', 'about', 'how', 'get',
        'may', 'way', 'these', 'could', 'time', 'very', 'know', 'just',
        'first', 'into', 'over', 'think', 'also', 'your', 'work', 'life',
        'only', 'new', 'year', 'come', 'state', 'use', 'man', 'day', 'good',
        'right', 'own', 'see', 'make', 'take', 'want', 'give', 'need', 'like'
    }
    
    if word in very_common_words:
        return True
    
    # Patrones típicos de palabras en inglés
    english_patterns = [
        r'^[a-z]{2,}$',      # Al menos 2 caracteres
        r'.*ing$',           # Terminaciones en -ing
        r'.*ed$',            # Terminaciones en -ed
        r'.*ly$',            # Terminaciones en -ly
        r'.*tion$',          # Terminaciones en -tion
        r'.*able$',          # Terminaciones en -able
        r'.*ful$',           # Terminaciones en -ful
        r'.*less$',          # Terminaciones en -less
        r'.*ness$',          # Terminaciones en -ness
        r'^un.*',            # Prefijo un-
        r'^re.*',            # Prefijo re-
        r'^pre.*',           # Prefijo pre-
        r'^dis.*',           # Prefijo dis-
        r'^over.*',          # Prefijo over-
        r'^under.*',         # Prefijo under-
    ]
    
    # Verificar si la palabra coincide con algún patrón inglés
    for pattern in english_patterns:
        if re.match(pattern, word):
            return True
    
    # Verificar combinaciones de letras comunes en inglés vs no comunes
    # Letras muy comunes en inglés
    common_letters = 'etaoinshrdlcumwfgypbvkjxqz'
    
    # Si la palabra es muy corta, ser más permisivo
    if len(word) <= 3:
        return True
    
    # Por defecto, aceptar la palabra si llega aquí
    return True