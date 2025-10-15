"""
Diccionario completo de formas fuertes y débiles para transcripción IPA.

Este diccionario contiene palabras funcionales del inglés que tienen diferentes
pronunciaciones según el contexto: formas fuertes (stressed) y débiles (unstressed).

Las formas débiles se usan típicamente en:
- Palabras no acentuadas en flujo normal de habla
- Palabras funcionales (preposiciones, conjunciones, artículos, auxiliares)
- Posiciones átonas en la oración

Las formas fuertes se usan en:
- Énfasis contrastivo
- Final de oración
- Cuando la palabra está aislada
- En ciertas construcciones sintácticas específicas
"""

from typing import Dict, Tuple, Optional


# Diccionario principal: palabra -> (forma_fuerte, forma_débil)
STRONG_WEAK_FORMS = {
    # ARTÍCULOS
    # NOTA: "the" NO está aquí porque no tiene formas fuerte/débil
    # sino variación alofónica: /ðə/ antes consonante, /ði/ antes vocal
    "the": ("ði", "ðə"),  # Mantener para compatibilidad pero se maneja especialmente
    "a": ("eɪ", "ə"),
    "an": ("æn", "ən"),
    
    # PRONOMBRES PERSONALES
    "i": ("aɪ", "aɪ"),  # 'I' siempre fuerte, pero incluido para completitud
    "you": ("juː", "jə"),
    "he": ("hiː", "hi"),  # forma débil con /ɪ/
    "she": ("ʃiː", "ʃi"),  # forma débil con /ɪ/
    "it": ("ɪt", "ɪt"),
    "we": ("wiː", "wi"),
    "they": ("ðeɪ", "ðeɪ"),
    "me": ("miː", "mi"),
    "him": ("hɪm", "ɪm"),
    "her": ("hɜː", "hə"),
    "us": ("ʌs", "əs"),
    "them": ("ðem", "ðəm"),
    
    # POSESIVOS
    "my": ("maɪ", "maɪ"),  # Generalmente fuerte
    "your": ("jɔː", "jə"),
    "his": ("hɪz", "ɪz"),
    "its": ("ɪts", "ɪts"),
    "our": ("aʊə", "aʊə"),  # RP: "aʊə", AM: "aʊr"
    "their": ("ðeə", "ðə"),
    
    # AUXILIARES - BE
    "am": ("æm", "əm"),
    "is": ("ɪz", "s"),  # forma débil puede ser "s" o "z"
    "are": ("ɑː", "ə"),
    "was": ("wɒz", "wəz"),
    "were": ("wɜː", "wə"),
    "be": ("biː", "bi"),
    "being": ("biːɪŋ", "biːɪŋ"),
    "been": ("biːn", "bɪn"),
    
    # AUXILIARES - HAVE
    "have": ("hæv", "əv"),
    "has": ("hæz", "əz"),
    "had": ("hæd", "əd"),
    "having": ("hævɪŋ", "hævɪŋ"),
    
    # AUXILIARES - DO
    "do": ("duː", "də"),
    "does": ("dʌz", "dəz"),
    "did": ("dɪd", "dəd"),
    "done": ("dʌn", "dən"),
    
    # AUXILIARES - WILL/WOULD
    "will": ("wɪl", "əl"),  # forma contraída 'll
    "would": ("wʊd", "əd"),  # forma contraída 'd
    "shall": ("ʃæl", "ʃəl"),
    "should": ("ʃʊd", "ʃəd"),
    
    # MODALES
    "can": ("kæn", "kən"),
    "could": ("kʊd", "kəd"),
    "may": ("meɪ", "meɪ"),  # Generalmente fuerte
    "might": ("maɪt", "maɪt"),  # Generalmente fuerte
    "must": ("mʌst", "məst"),
    "ought": ("ɔːt", "ɔːt"),  # Generalmente fuerte
    
    # PREPOSICIONES
    "of": ("ɒv", "əv"),
    "to": ("tuː", "tə"),
    "for": ("fɔː", "fə"),
    "from": ("frɒm", "frəm"),
    "at": ("æt", "ət"),
    "in": ("ɪn", "ɪn"),  # Menos reducción que otras
    "on": ("ɒn", "ən"),
    "with": ("wɪð", "wɪð"),  # Menos común reducir
    "by": ("baɪ", "baɪ"),  # Generalmente fuerte
    "about": ("əbaʊt", "əbət"),
    "into": ("ɪntuː", "ɪntə"),
    "onto": ("ɒntuː", "ɒntə"),
    "upon": ("əpɒn", "əpən"),
    "before": ("bɪfɔː", "bɪfə"),
    "after": ("ɑːftə", "ɑːftə"),  # Menos reducción
    
    # CONJUNCIONES
    "and": ("ænd", "ən"),  # forma débil sin /d/ final
    "or": ("ɔː", "ə"),
    "but": ("bʌt", "bət"),
    "that": ("ðæt", "ðət"),  # como conjunción
    "than": ("ðæn", "ðən"),
    "as": ("æz", "əz"),
    "if": ("ɪf", "ɪf"),  # Menos reducción
    "when": ("wen", "wən"),
    "where": ("weə", "wə"),
    "while": ("waɪl", "waɪl"),  # Generalmente fuerte
    "because": ("bɪkɒz", "bɪkəz"),
    
    # ADVERBIOS Y OTROS
    "there": ("ðeə", "ðə"),  # como adverbio existencial
    "some": ("sʌm", "səm"),
    "any": ("enɪ", "ənɪ"),
    "not": ("nɒt", "nət"),  # también "nt" en contracciones
    "so": ("səʊ", "səʊ"),  # Generalmente fuerte
    "just": ("dʒʌst", "dʒəst"),
    "only": ("əʊnlɪ", "əʊnlɪ"),  # Primera sílaba puede reducirse
    
    # CONTRACCIONES COMUNES (formas ya débiles)
    "i'm": ("aɪm", "aɪm"),
    "you're": ("jʊə", "jə"),
    "he's": ("hiːz", "hiːz"),
    "she's": ("ʃiːz", "ʃiːz"),
    "it's": ("ɪts", "ɪts"),
    "we're": ("wɪə", "wɪə"),
    "they're": ("ðeə", "ðeə"),
    "i've": ("aɪv", "aɪv"),
    "you've": ("juːv", "jəv"),
    "we've": ("wiːv", "wɪv"),
    "they've": ("ðeɪv", "ðeɪv"),
    "i'll": ("aɪl", "aɪl"),
    "you'll": ("juːl", "jəl"),
    "he'll": ("hiːl", "hiːl"),
    "she'll": ("ʃiːl", "ʃiːl"),
    "it'll": ("ɪtəl", "ɪtəl"),
    "we'll": ("wiːl", "wɪl"),
    "they'll": ("ðeɪl", "ðeɪl"),
    "won't": ("wəʊnt", "wəʊnt"),
    "can't": ("kɑːnt", "kænt"),  # RP vs AM
    "couldn't": ("kʊdənt", "kʊdənt"),
    "shouldn't": ("ʃʊdənt", "ʃʊdənt"),
    "wouldn't": ("wʊdənt", "wʊdənt"),
    "don't": ("dəʊnt", "dəʊnt"),
    "doesn't": ("dʌzənt", "dʌzənt"),
    "didn't": ("dɪdənt", "dɪdənt"),
    "haven't": ("hævənt", "hævənt"),
    "hasn't": ("hæzənt", "hæzənt"),
    "hadn't": ("hædənt", "hædənt"),
    "isn't": ("ɪzənt", "ɪzənt"),
    "aren't": ("ɑːnt", "ɑːnt"),
    "wasn't": ("wɒzənt", "wɒzənt"),
    "weren't": ("wɜːnt", "wɜːnt"),
}

# Variaciones especiales para RP vs American
RP_SPECIFIC_FORMS = {
    "our": ("aʊə", "aʊə"),
    "are": ("ɑː", "ə"),
    "were": ("wɜː", "wə"),
    "can't": ("kɑːnt", "kɑːnt"),
    "after": ("ɑːftə", "ɑːftə"),
}

AMERICAN_SPECIFIC_FORMS = {
    "our": ("aʊr", "aʊr"),
    "are": ("ɑr", "ər"),
    "were": ("wɜr", "wər"),
    "can't": ("kænt", "kænt"),
    "after": ("æftər", "æftər"),
}


def get_word_forms(word: str, accent: str = "rp") -> Optional[Tuple[str, str]]:
    """
    Obtiene las formas fuerte y débil de una palabra.
    
    Args:
        word (str): Palabra a buscar (en minúsculas)
        accent (str): Tipo de acento ("rp" o "american")
    
    Returns:
        Optional[Tuple[str, str]]: (forma_fuerte, forma_débil) o None si no existe
    """
    word_lower = word.lower().strip()
    
    # Primero verificar si hay forma específica para el acento
    if accent == "rp" and word_lower in RP_SPECIFIC_FORMS:
        return RP_SPECIFIC_FORMS[word_lower]
    elif accent == "american" and word_lower in AMERICAN_SPECIFIC_FORMS:
        return AMERICAN_SPECIFIC_FORMS[word_lower]
    
    # Si no, usar la forma general
    return STRONG_WEAK_FORMS.get(word_lower)


def has_weak_form(word: str) -> bool:
    """
    Verifica si una palabra tiene forma débil disponible.
    
    Args:
        word (str): Palabra a verificar
    
    Returns:
        bool: True si tiene forma débil
    """
    word_lower = word.lower().strip()
    return word_lower in STRONG_WEAK_FORMS


def get_strong_form(word: str, accent: str = "rp") -> Optional[str]:
    """
    Obtiene solo la forma fuerte de una palabra.
    
    Args:
        word (str): Palabra a buscar
        accent (str): Tipo de acento
    
    Returns:
        Optional[str]: Forma fuerte o None
    """
    forms = get_word_forms(word, accent)
    return forms[0] if forms else None


def get_weak_form(word: str, accent: str = "rp") -> Optional[str]:
    """
    Obtiene solo la forma débil de una palabra.
    
    Args:
        word (str): Palabra a buscar
        accent (str): Tipo de acento
    
    Returns:
        Optional[str]: Forma débil o None
    """
    forms = get_word_forms(word, accent)
    return forms[1] if forms else None


# Palabras que típicamente van en forma fuerte incluso en contextos no acentuados
USUALLY_STRONG_WORDS = {
    "i", "my", "may", "might", "ought", "by", "so", "while", 
    "if", "in", "with", "after", "only"
}

# Palabras que casi siempre se reducen (excluyendo "the" que es especial)
USUALLY_WEAK_WORDS = {
    "a", "an", "of", "to", "for", "from", "at", "and", 
    "or", "that", "than", "as", "some", "any"
}


def should_use_weak_form(word: str, context: Dict[str, any]) -> bool:
    """
    Determina si una palabra debería usar su forma débil basado en el contexto.
    
    Args:
        word (str): Palabra a analizar
        context (dict): Información contextual:
            - is_sentence_end: bool - si está al final de oración
            - is_emphasized: bool - si está enfatizada
            - is_isolated: bool - si está aislada
            - previous_word: str - palabra anterior
            - next_word: str - palabra siguiente
            - use_weak_forms_preference: bool - preferencia del usuario
    
    Returns:
        bool: True si debería usar forma débil
    """
    word_lower = word.lower().strip()
    
    # Si no tiene forma débil, no aplica
    if not has_weak_form(word_lower):
        return False
    
    # Si el usuario prefiere formas fuertes, usar esas preferentemente
    if not context.get("use_weak_forms_preference", True):
        return word_lower in USUALLY_WEAK_WORDS
    
    # Casos donde siempre usar forma fuerte
    if (context.get("is_sentence_end", False) or 
        context.get("is_emphasized", False) or
        context.get("is_isolated", False)):
        return False
    
    # Palabras que usualmente van en forma fuerte
    if word_lower in USUALLY_STRONG_WORDS:
        return False
    
    # Palabras que usualmente se reducen
    if word_lower in USUALLY_WEAK_WORDS:
        return True
    
    # Caso por defecto: usar forma débil si está disponible
    # (esto representa el habla natural en contexto no enfático)
    return True


# Lista de todas las palabras con formas débiles para referencia
ALL_FUNCTION_WORDS = list(STRONG_WEAK_FORMS.keys())