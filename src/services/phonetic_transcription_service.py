"""
Servicio de transcripción fonética para convertir texto inglés a notación IPA.
Especializado en Received Pronunciation (RP) - estándar británico.
"""

import eng_to_ipa as ipa_converter
import re
from typing import Dict, Optional
from src.services.hybrid_rp_service import get_hybrid_rp_service

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
        
        # Usar el servicio híbrido con prioridad en diccionario local
        # Longman se puede habilitar como opción experimental
        hybrid_service = get_hybrid_rp_service(use_longman=False)  # Por ahora, usar solo local
        transcription = hybrid_service.transcribe_text(cleaned_text)
        
        return transcription
        
    except Exception as e:
        raise Exception(f"Error en transcripción fonética: {str(e)}")

def improve_rp_transcription(transcription: str) -> str:
    """
    Convierte transcripción IPA de General American a Received Pronunciation.
    
    Args:
        transcription (str): Transcripción IPA en General American
    
    Returns:
        str: Transcripción IPA en RP (Received Pronunciation)
    """
    # Mapeo completo de fonemas GA -> RP
    ga_to_rp_mapping = {
        # Vocales róticas (r-colored vowels) -> vocales largas sin r
        'ɑr': 'ɑː',    # car /kɑr/ -> /kɑː/
        'ɔr': 'ɔː',    # for /fɔr/ -> /fɔː/ 
        'ər': 'ə',     # better /ˈbɛtər/ -> /ˈbetə/
        'ɪr': 'ɪə',   # here /hɪr/ -> /hɪə/
        'ɛr': 'eə',   # care /kɛr/ -> /keə/
        'ʊr': 'ʊə',   # sure /ʃʊr/ -> /ʃʊə/
        
        # Vocal LOT (o corta)
        'ɑ': 'ɒ',     # got /ɡɑt/ -> /ɡɒt/
        
        # Vocal CLOTH (también afectada)
        'ɔ': 'ɒ',     # long /lɔŋ/ -> /lɒŋ/ (en algunos casos)
        
        # Diptongo GOAT 
        'oʊ': 'əʊ',   # go /ɡoʊ/ -> /ɡəʊ/
        
        # Diptongo FACE
        'eɪ': 'eɪ',   # same in both (mantener)
        
        # Vocal STRUT vs FOOT distinction
        'ʌ': 'ʌ',     # but /bʌt/ -> /bʌt/ (igual en RP)
        
        # R no rótica - eliminar R final y pre-consonántica
        'r': '',      # eliminar r no rótica
        
        # TRAP vowel (generalmente igual)
        'æ': 'æ',     # cat /kæt/ -> /kæt/
        
        # Algunas palabras específicas que son diferentes
        'ænt': 'ɑːnt', # can't, dance, etc. en RP usan /ɑː/
        'æns': 'ɑːns', # dance /dæns/ -> /dɑːns/
        'æsk': 'ɑːsk', # ask /æsk/ -> /ɑːsk/
        'æf': 'ɑːf',   # after, laugh, etc.
        'æθ': 'ɑːθ',   # path /pæθ/ -> /pɑːθ/
    }
    
    # Aplicar conversiones básicas
    improved = transcription
    
    # Aplicar mapeo en orden específico (más largo primero para evitar conflictos)
    sorted_mappings = sorted(ga_to_rp_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    
    for ga_sound, rp_sound in sorted_mappings:
        improved = improved.replace(ga_sound, rp_sound)
    
    # Post-procesamiento específico para RP
    improved = apply_rp_specific_rules(improved)
    
    return improved

def apply_rp_specific_rules(transcription: str) -> str:
    """
    Aplica reglas específicas adicionales para RP.
    
    Args:
        transcription (str): Transcripción parcialmente convertida
    
    Returns:
        str: Transcripción con reglas RP aplicadas
    """
    import re
    
    # Eliminar R no róticas (r que no va seguida de vocal)
    # R final de palabra
    transcription = re.sub(r'r$', '', transcription)
    # R antes de consonante
    transcription = re.sub(r'r([bcdfghjklmnpqstvwxyz])', r'\1', transcription)
    # R entre consonante y vocal se mantiene
    
    # Ajustar ciertas combinaciones específicas
    specific_adjustments = {
        'hɛˈloʊ': 'həˈləʊ',     # hello
        'wəld': 'wɜːld',         # world (pero sin la r final)
        'wɜːld': 'wɜːld',        # world corrected
        'ˈstændəd': 'ˈstændəd',  # standard (mantener)
    }
    
    for ga_form, rp_form in specific_adjustments.items():
        transcription = transcription.replace(ga_form, rp_form)
    
    # Limpiar dobles espacios o símbolos extraños
    transcription = re.sub(r'\s+', ' ', transcription.strip())
    
    return transcription

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