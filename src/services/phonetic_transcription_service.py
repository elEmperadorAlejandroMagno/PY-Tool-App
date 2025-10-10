"""
Servicio de transcripción fonética para convertir texto inglés a notación IPA.
Especializado en Received Pronunciation (RP) - estándar británico.
"""

import eng_to_ipa as ipa_converter
import re
from typing import Dict, Optional

def clean_text_for_transcription(text: str) -> str:
    """
    Limpia el texto antes de la transcripción fonética.
    
    Args:
        text (str): Texto a limpiar
    
    Returns:
        str: Texto limpio para transcripción
    """
    # Remover caracteres especiales excepto puntuación básica
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def transcribe_text_to_ipa_rp(text: str) -> str:
    """
    Transcribe texto inglés a notación IPA usando Received Pronunciation.
    
    Args:
        text (str): Texto en inglés para transcribir
    
    Returns:
        str: Transcripción IPA del texto
    
    Raises:
        Exception: Si hay error en la transcripción
    """
    try:
        # Limpiar texto
        cleaned_text = clean_text_for_transcription(text)
        
        if not cleaned_text.strip():
            return ""
        
        # Usar eng_to_ipa con configuración para RP
        # La biblioteca eng_to_ipa usa principalmente RP por defecto
        transcription = ipa_converter.convert(cleaned_text)
        
        # Post-procesamiento para mejorar la transcripción RP
        transcription = improve_rp_transcription(transcription)
        
        return transcription
        
    except Exception as e:
        raise Exception(f"Error en transcripción fonética: {str(e)}")

def improve_rp_transcription(transcription: str) -> str:
    """
    Mejora la transcripción IPA para que sea más consistente con RP.
    
    Args:
        transcription (str): Transcripción IPA básica
    
    Returns:
        str: Transcripción IPA mejorada para RP
    """
    # Diccionario de ajustes específicos para RP
    rp_adjustments = {
        # Ajustes comunes para RP vs General American
        'ɑr': 'ɑː',  # car -> /kɑː/
        'ɔr': 'ɔː',  # for -> /fɔː/
        'ər': 'ə',   # better -> /ˈbetə/
        'æ': 'æ',    # cat -> /kæt/ (mantener)
        'ɑ': 'ɑː',   # father -> /ˈfɑːðə/
        'ɔ': 'ɒ',    # got -> /ɡɒt/
    }
    
    # Aplicar ajustes
    improved = transcription
    for american, british in rp_adjustments.items():
        improved = improved.replace(american, british)
    
    return improved

def get_word_transcription(word: str) -> Optional[str]:
    """
    Obtiene la transcripción IPA de una palabra específica.
    
    Args:
        word (str): Palabra a transcribir
    
    Returns:
        Optional[str]: Transcripción IPA de la palabra o None si hay error
    """
    try:
        word = word.strip().lower()
        if not word:
            return None
            
        transcription = ipa_converter.convert(word)
        return improve_rp_transcription(transcription)
    except:
        return None

def is_valid_english_text(text: str) -> bool:
    """
    Verifica si el texto contiene principalmente caracteres válidos para inglés.
    
    Args:
        text (str): Texto a verificar
    
    Returns:
        bool: True si el texto parece ser inglés válido
    """
    # Verificar que el texto contiene principalmente letras del alfabeto inglés
    english_chars = re.findall(r'[a-zA-Z]', text)
    total_chars = re.findall(r'[a-zA-ZÀ-ÿ]', text)  # Incluir caracteres con acentos
    
    if len(total_chars) == 0:
        return False
    
    # Al menos 80% de caracteres deben ser del alfabeto inglés básico
    return len(english_chars) / len(total_chars) >= 0.8