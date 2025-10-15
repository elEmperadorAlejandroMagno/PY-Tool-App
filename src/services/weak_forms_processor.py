"""
Procesador de formas fuertes y débiles para transcripción IPA.

Estrategia:
- Las palabras funcionales usan formas débiles por defecto
- Se aplican formas fuertes según reglas de posición y contexto
- Reglas especiales (to be negativo, final de oración, etc.)
"""

import re
from typing import List, Dict, Any, Optional
from .strong_weak_forms_dictionary import (
    get_word_forms, has_weak_form, get_weak_form, get_strong_form
)


def is_vowel_sound_start(word: str) -> bool:
    """
    Determina si una palabra comienza con sonido vocálico.
    
    Args:
        word (str): Palabra a analizar
    
    Returns:
        bool: True si comienza con sonido vocálico
    """
    if not word:
        return False
    
    word = word.lower().strip()
    
    # Palabras que empiezan con consonante pero suenan como vocal (silent h)
    vowel_sound_exceptions = {
        'hour', 'honest', 'honor', 'honour', 'heir', 'herb'
    }
    
    # Palabras que empiezan con vocal pero suenan como consonante (/juː/ sound)
    consonant_sound_exceptions = {
        'university', 'uniform', 'unique', 'united', 'union', 'unit',
        'european', 'euphoria', 'eucalyptus', 'useful', 'usual', 'use', 'user'
    }
    
    # Verificar excepciones de consonante
    if any(word.startswith(exc) for exc in consonant_sound_exceptions):
        return False
    
    # Verificar excepciones de vocal
    if any(word.startswith(exc) for exc in vowel_sound_exceptions):
        return True
    
    # Regla general: comienza con vocal escrita
    return word[0].lower() in 'aeiou'


def is_sentence_end_position(words: List[str], word_index: int) -> bool:
    """
    Determina si una palabra está en posición de final de oración.
    
    Args:
        words (List[str]): Lista de palabras
        word_index (int): Índice de la palabra
    
    Returns:
        bool: True si está al final de oración
    """
    if word_index >= len(words) - 1:
        return True
    
    # Buscar puntuación de final de oración en las siguientes palabras
    for i in range(word_index + 1, min(len(words), word_index + 3)):
        if re.search(r'[.!?]', words[i]):
            return True
    
    return False


def is_negative_context(words: List[str], word_index: int) -> bool:
    """
    Determina si una palabra está en contexto negativo.
    
    Args:
        words (List[str]): Lista de palabras
        word_index (int): Índice de la palabra
    
    Returns:
        bool: True si está en contexto negativo
    """
    current_word = words[word_index].lower().strip()
    
    # Verificar si la palabra actual es una contracción negativa
    negative_contractions = {
        "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't",
        "won't", "wouldn't", "can't", "couldn't", "shouldn't", "mustn't",
        "haven't", "hasn't", "hadn't"
    }
    
    if current_word in negative_contractions:
        return True
    
    # Verificar si hay "not" cerca (antes o después)
    search_range = range(max(0, word_index - 2), min(len(words), word_index + 3))
    for i in search_range:
        if words[i].lower().strip() in ['not', "n't"]:
            return True
    
    return False


def is_be_verb_in_negative(words: List[str], word_index: int) -> bool:
    """
    Determina si un verbo 'to be' está en construcción negativa.
    
    Args:
        words (List[str]): Lista de palabras
        word_index (int): Índice de la palabra
    
    Returns:
        bool: True si es verbo to be en negativo
    """
    current_word = words[word_index].lower().strip()
    
    # Verificar si es un verbo 'to be'
    be_verbs = {'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    
    if current_word not in be_verbs:
        return False
    
    # Verificar si está en contexto negativo
    return is_negative_context(words, word_index)


def get_the_form(words: List[str], word_index: int) -> str:
    """
    Obtiene la forma correcta de "the" basada en la siguiente palabra.
    
    Args:
        words (List[str]): Lista de palabras
        word_index (int): Índice de "the"
    
    Returns:
        str: /ðə/ antes de consonante, /ði/ antes de vocal
    """
    if word_index + 1 < len(words):
        next_word = words[word_index + 1]
        if is_vowel_sound_start(next_word):
            return 'ði'  # antes de vocal
    
    return 'ðə'  # antes de consonante (por defecto)


def should_use_strong_form(word: str, words: List[str], word_index: int, 
                          use_weak_forms_preference: bool = True) -> bool:
    """
    Determina si una palabra debe usar forma fuerte según las reglas de posición.
    NOTA: "the" se maneja especialmente y no pasa por esta función.
    
    Args:
        word (str): Palabra a analizar
        words (List[str]): Lista de palabras en la oración
        word_index (int): Índice de la palabra
        use_weak_forms_preference (bool): Preferencia del usuario
    
    Returns:
        bool: True si debe usar forma fuerte
    """
    word_lower = word.lower().strip()
    
    # "the" se maneja especialmente, no debe llegar aquí
    if word_lower == "the":
        return False  # No aplicar lógica normal
    
    # Si el usuario prefiere formas fuertes, usar siempre fuertes
    if not use_weak_forms_preference:
        return True
    
    # Regla 1: Final de oración -> forma fuerte
    if is_sentence_end_position(words, word_index):
        return True
    
    # Regla 2: Verbo 'to be' en negativo -> forma fuerte
    if is_be_verb_in_negative(words, word_index):
        return True
    
    # Regla 3: Contracciones negativas -> mantener como están (ya son fuertes en el dict)
    negative_contractions = {
        "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't",
        "won't", "wouldn't", "can't", "couldn't", "shouldn't", "mustn't",
        "haven't", "hasn't", "hadn't"
    }
    if word_lower in negative_contractions:
        return True
    
    # Regla 4: Primera palabra de oración (excepto artículos y preposiciones muy comunes)
    if word_index == 0:
        common_weak_starters = {'a', 'an', 'in', 'on', 'at', 'to', 'for'}  # "the" se maneja especialmente
        if word_lower not in common_weak_starters:
            return True
    
    # Por defecto: usar forma débil
    return False


def apply_the_forms(original_text: str, transcribed_text: str) -> str:
    """
    Aplica las formas correctas de "the" según la palabra siguiente.
    NOTA: Esta función es redundante ya que "the" se maneja en el procesador principal.
    Se mantiene para compatibilidad.
    
    Args:
        original_text (str): Texto original
        transcribed_text (str): Texto transcrito
    
    Returns:
        str: Texto con formas de "the" aplicadas
    """
    # El manejo de "the" ya se hace en _process_line_weak_strong
    return transcribed_text


def _apply_the_to_line(original_line: str, transcribed_line: str) -> str:
    """
    Aplica formas de "the" a una línea específica.
    
    Args:
        original_line (str): Línea original
        transcribed_line (str): Línea transcrita
    
    Returns:
        str: Línea procesada
    """
    # Obtener palabras del original
    original_words = re.findall(r'\b\w+\b', original_line.lower())
    
    result = transcribed_line
    the_count = 0
    
    for i, word in enumerate(original_words):
        if word == 'the' and i + 1 < len(original_words):
            the_count += 1
            next_word = original_words[i + 1]
            
            # Determinar forma correcta
            if is_vowel_sound_start(next_word):
                target_form = 'ði'
            else:
                target_form = 'ðə'
            
            # Reemplazar en la transcripción (solo la ocurrencia correspondiente)
            the_patterns = [r'ðiː', r'ðə', r'ði', r'the']
            
            for pattern in the_patterns:
                pattern_regex = r'\b' + pattern + r'\b'
                if re.search(pattern_regex, result):
                    result = re.sub(pattern_regex, target_form, result, count=1)
                    break
    
    return result


def apply_linking_r(text: str, accent: str = "rp") -> str:
    """
    Aplica linking r en RP.
    
    Args:
        text (str): Texto transcrito
        accent (str): Acento
    
    Returns:
        str: Texto con linking r aplicado
    """
    if accent != "rp":
        return text
    
    # Sonidos que pueden tener linking r
    linking_r_endings = ['ə', 'ɑː', 'ɔː', 'eə', 'ɪə', 'ʊə', 'aʊə']
    
    # Vocales que desencadenan linking r
    vowel_starts = ['ə', 'ɑ', 'æ', 'e', 'ɪ', 'ɒ', 'ʌ', 'ʊ', 'iː', 'uː', 'ɜː', 'ɔː', 'ɑː',
                   'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'əʊ', 'ɪə', 'eə', 'ʊə']
    
    words = text.split()
    result_words = []
    
    for i, word in enumerate(words):
        current_word = word
        
        if i < len(words) - 1:
            next_word = words[i + 1]
            
            # Verificar linking r
            for ending in linking_r_endings:
                if word.endswith(ending):
                    for vowel in vowel_starts:
                        if next_word.startswith(vowel):
                            current_word = word + 'r'
                            break
                    break
        
        result_words.append(current_word)
    
    return ' '.join(result_words)


def process_weak_forms_in_transcription(original_text: str, transcribed_text: str, 
                                       accent: str = "rp", use_weak_forms: bool = True) -> str:
    """
    Procesa transcripción aplicando formas débiles por defecto y reglas de posición para fuertes.
    
    Args:
        original_text (str): Texto original en inglés
        transcribed_text (str): Transcripción IPA base
        accent (str): Acento a usar
        use_weak_forms (bool): Si aplicar sistema de formas débiles
    
    Returns:
        str: Transcripción procesada
    """
    if not transcribed_text:
        return transcribed_text
    
    result = transcribed_text
    
    # 1. Aplicar formas débiles por defecto y reglas de posición
    if use_weak_forms:
        result = _apply_weak_strong_forms(original_text, result, accent, use_weak_forms)
    
    # 2. Aplicar formas de "the" basadas en fonética
    result = apply_the_forms(original_text, result)
    
    # 3. Aplicar linking r (solo RP)
    if accent == "rp":
        result = apply_linking_r(result, accent)
    
    return result


def _apply_weak_strong_forms(original_text: str, transcribed_text: str, 
                            accent: str, use_weak_forms: bool) -> str:
    """
    Aplica formas débiles por defecto y fuertes según reglas de posición.
    
    Args:
        original_text (str): Texto original
        transcribed_text (str): Transcripción
        accent (str): Acento
        use_weak_forms (bool): Si usar formas débiles
    
    Returns:
        str: Texto procesado
    """
    if not original_text:
        return transcribed_text
    
    original_lines = original_text.splitlines()
    transcribed_lines = transcribed_text.splitlines()
    processed_lines = []
    
    for i, transcribed_line in enumerate(transcribed_lines):
        if i >= len(original_lines) or not transcribed_line.strip():
            processed_lines.append(transcribed_line)
            continue
            
        original_line = original_lines[i]
        processed_line = _process_line_weak_strong(original_line, transcribed_line, accent, use_weak_forms)
        processed_lines.append(processed_line)
    
    return '\n'.join(processed_lines)


def _process_line_weak_strong(original_line: str, transcribed_line: str, 
                             accent: str, use_weak_forms: bool) -> str:
    """
    Procesa una línea aplicando formas débiles/fuertes.
    
    Args:
        original_line (str): Línea original
        transcribed_line (str): Línea transcrita
        accent (str): Acento
        use_weak_forms (bool): Si usar formas débiles
    
    Returns:
        str: Línea procesada
    """
    original_words = re.findall(r'\b\w+(?:\'\w+)?\b', original_line.lower())
    if not original_words:
        return transcribed_line
    
    result = transcribed_line
    
    # Para cada palabra, aplicar reglas
    for word_index, word in enumerate(original_words):
        # Manejar "the" especialmente
        if word == "the":
            correct_the_form = get_the_form(original_words, word_index)
            # Reemplazar cualquier forma de "the" por la correcta
            the_patterns = ['ðiː', 'ðə', 'ði', 'the']
            for pattern in the_patterns:
                if pattern in result and pattern != correct_the_form:
                    result = result.replace(pattern, correct_the_form, 1)
                    break
            continue
        
        # Para otras palabras con formas débiles/fuertes
        if not has_weak_form(word):
            continue
        
        # Determinar si debe usar forma fuerte
        use_strong = should_use_strong_form(word, original_words, word_index, use_weak_forms)
        
        # Obtener formas
        strong_form = get_strong_form(word, accent)
        weak_form = get_weak_form(word, accent)
        
        if not strong_form or not weak_form:
            continue
        
        # Determinar forma objetivo
        target_form = strong_form if use_strong else weak_form
        
        # Reemplazar en la transcripción
        # Buscar tanto la forma fuerte como la débil y reemplazar por la objetivo
        for form_to_replace in [strong_form, weak_form]:
            if form_to_replace != target_form and form_to_replace in result:
                result = result.replace(form_to_replace, target_form, 1)
                break
    
    return result
