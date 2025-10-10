"""
Servicio avanzado de transcripción fonética especializado en Received Pronunciation (RP).
Utiliza un diccionario específico de RP y reglas de conversión precisas.
"""

import re
from typing import Dict, Optional, Tuple
import eng_to_ipa as ipa_converter

# Diccionario específico de palabras comunes con transcripción RP
# Basado en el diccionario Longman y otros recursos de RP
RP_WORD_DICTIONARY = {
    # Palabras básicas
    "hello": "həˈləʊ",
    "world": "wɜːld", 
    "the": "ðə",
    "and": "ænd",
    "or": "ɔː",
    "this": "ðɪs",
    "that": "ðæt",
    "is": "ɪz",
    "are": "ɑː",
    "was": "wɒz",
    "were": "wɜː",
    "have": "hæv",
    "has": "hæz",
    "had": "hæd",
    "will": "wɪl",
    "would": "wʊd",
    "could": "kʊd",
    "should": "ʃʊd",
    "can": "kæn",
    "cannot": "ˈkænɒt",
    "can't": "kɑːnt",
    
    # Palabras académicas comunes
    "university": "ˌjuːnɪˈvɜːsəti",
    "pronunciation": "prəˌnʌnsɪˈeɪʃən",
    "phonetic": "fəˈnetɪk",
    "phonetics": "fəˈnetɪks",
    "received": "rɪˈsiːvd",
    "british": "ˈbrɪtɪʃ",
    "english": "ˈɪŋglɪʃ",
    "standard": "ˈstændəd",
    "dictionary": "ˈdɪkʃənri",
    "language": "ˈlæŋgwɪdʒ",
    "linguistics": "lɪŋˈgwɪstɪks",
    "transcription": "trænˈskrɪpʃən",
    "international": "ˌɪntəˈnæʃənəl",
    "alphabet": "ˈælfəbet",
    
    # Palabras con diferencias claras GA vs RP
    "car": "kɑː",
    "park": "pɑːk", 
    "start": "stɑːt",
    "dance": "dɑːns",
    "path": "pɑːθ",
    "ask": "ɑːsk",
    "answer": "ˈɑːnsə",
    "after": "ˈɑːftə",
    "class": "klɑːs",
    "glass": "glɑːs",
    "last": "lɑːst",
    "fast": "fɑːst",
    "past": "pɑːst",
    "castle": "ˈkɑːsəl",
    "laugh": "lɑːf",
    "aunt": "ɑːnt",
    "can't": "kɑːnt",
    
    # Palabras con LOT vowel
    "hot": "hɒt",
    "got": "gɒt",
    "lot": "lɒt",
    "not": "nɒt",
    "top": "tɒp",
    "stop": "stɒp",
    "shop": "ʃɒp",
    "dog": "dɒg",
    "long": "lɒŋ",
    "song": "sɒŋ",
    "wrong": "rɒŋ",
    
    # Palabras con GOAT diphthong
    "go": "gəʊ",
    "no": "nəʊ", 
    "so": "səʊ",
    "show": "ʃəʊ",
    "know": "nəʊ",
    "home": "həʊm",
    "phone": "fəʊn",
    "close": "kləʊs",
    "most": "məʊst",
    "post": "pəʊst",
    
    # Palabras sin R rótica
    "here": "hɪə",
    "there": "ðeə",
    "where": "weə",
    "care": "keə",
    "fair": "feə",
    "hair": "heə",
    "chair": "tʃeə",
    "sure": "ʃʊə",
    "poor": "pʊə",
    "tour": "tʊə",
    "year": "jɪə",
    "near": "nɪə",
    "clear": "klɪə",
    "dear": "dɪə",
    "beer": "bɪə",
    "fear": "fɪə",
    
    # Palabras de prueba adicionales
    "water": "ˈwɔːtə",
    "father": "ˈfɑːðə", 
    "mother": "ˈmʌðə",
    "brother": "ˈbrʌðə",
    "sister": "ˈsɪstə",
    "teacher": "ˈtiːtʃə",
    "student": "ˈstjuːdənt",
    "school": "skuːl",
    "learn": "lɜːn",
    "study": "ˈstʌdi",
    "test": "test",
    "exam": "ɪgˈzæm",
    "book": "bʊk",
    "read": "riːd",  # presente
    "write": "raɪt",
    "speak": "spiːk",
    "listen": "ˈlɪsən",
    "understand": "ˌʌndəˈstænd",
}

def get_rp_transcription_from_dict(word: str) -> Optional[str]:
    """
    Obtiene la transcripción RP de una palabra desde el diccionario especializado.
    
    Args:
        word (str): Palabra a transcribir
    
    Returns:
        Optional[str]: Transcripción RP o None si no está en el diccionario
    """
    word_clean = word.lower().strip()
    # Remover puntuación
    word_clean = re.sub(r'[^\w]', '', word_clean)
    
    return RP_WORD_DICTIONARY.get(word_clean)

def convert_ga_to_rp_advanced(transcription: str) -> str:
    """
    Conversión avanzada de General American a RP usando reglas fonológicas precisas.
    
    Args:
        transcription (str): Transcripción en GA
    
    Returns:
        str: Transcripción convertida a RP
    """
    
    # Mapeo completo y preciso GA -> RP
    conversions = [
        # R-colored vowels (róticas) -> no róticas
        (r'ɑr', 'ɑː'),      # car, park, start
        (r'ɔr', 'ɔː'),      # for, more, door  
        (r'ɜr', 'ɜː'),      # bird, word, heard
        (r'ər', 'ə'),       # better, water, sister
        (r'ɪr', 'ɪə'),      # here, near, clear
        (r'ɛr', 'eə'),      # care, fair, where
        (r'ʊr', 'ʊə'),      # sure, pure, tour
        
        # LOT vowel: GA /ɑ/ -> RP /ɒ/
        (r'(?<![ɑː])ɑ(?![ːr])', 'ɒ'),  # hot, got, not (pero no car, start)
        
        # GOAT diphthong: GA /oʊ/ -> RP /əʊ/
        (r'oʊ', 'əʊ'),      # go, show, phone
        
        # BATH words: GA /æ/ -> RP /ɑː/ en contextos específicos
        (r'æf(?![ɪei])', 'ɑːf'),   # after, laugh, staff
        (r'æθ', 'ɑːθ'),            # path, bath, math
        (r'æsk', 'ɑːsk'),          # ask, task, mask
        (r'ænt', 'ɑːnt'),          # can't, aunt, plant
        (r'æns', 'ɑːns'),          # dance, chance, france
        (r'æst', 'ɑːst'),          # last, fast, cast
        (r'æs(?=s|t)', 'ɑːs'),     # class, glass, pass
        
        # Eliminar R no rótica
        (r'r(?=[bcdfghjklmnpqstvwxyzθðʃʒŋ])', ''),  # r antes de consonante
        (r'r$', ''),                                  # r final de palabra
        (r'r(?=\s)', ''),                            # r final antes de espacio
        
        # Ajustes específicos de consonantes
        (r't(?=i[ənəm])', 't'),     # mantener /t/ en -tion, -tive (no flapping)
        
        # Ajustes de vocales específicas
        (r'ɛ(?=r)', 'e'),           # preparar para /eə/
        (r'ɪ(?=r)', 'ɪ'),           # preparar para /ɪə/
        
    ]
    
    result = transcription
    
    # Aplicar conversiones en orden
    for pattern, replacement in conversions:
        result = re.sub(pattern, replacement, result)
    
    # Post-procesamiento para limpiar
    result = re.sub(r'\s+', ' ', result.strip())
    
    return result

def transcribe_word_to_rp(word: str) -> str:
    """
    Transcribe una palabra individual a RP.
    
    Args:
        word (str): Palabra a transcribir
    
    Returns:
        str: Transcripción RP de la palabra
    """
    # Primero intentar con el diccionario específico
    rp_from_dict = get_rp_transcription_from_dict(word)
    if rp_from_dict:
        return rp_from_dict
    
    # Si no está en el diccionario, usar eng-to-ipa y convertir
    try:
        ga_transcription = ipa_converter.convert(word.lower())
        rp_transcription = convert_ga_to_rp_advanced(ga_transcription)
        return rp_transcription
    except:
        # Fallback básico
        return word

def transcribe_text_to_rp_advanced(text: str) -> str:
    """
    Transcribe texto completo a RP usando el método avanzado.
    
    Args:
        text (str): Texto en inglés
    
    Returns:
        str: Transcripción RP del texto
    """
    # Limpiar texto
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    text = re.sub(r'\s+', ' ', text.strip())
    
    if not text:
        return ""
    
    # Dividir en palabras, preservando puntuación
    words = re.findall(r'\b\w+\b|[.,!?;:\'-]', text)
    
    transcribed_words = []
    
    for word in words:
        if re.match(r'[.,!?;:\'-]', word):
            # Es puntuación, mantener
            transcribed_words.append(word)
        else:
            # Es palabra, transcribir
            transcribed_word = transcribe_word_to_rp(word)
            transcribed_words.append(transcribed_word)
    
    # Unir resultado
    result = ' '.join(transcribed_words)
    
    # Limpiar espacios extra alrededor de puntuación
    result = re.sub(r'\s+([.,!?;:\'-])', r'\1', result)
    result = re.sub(r'\s+', ' ', result.strip())
    
    return result