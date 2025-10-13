"""
Servicio para transcripción fonética RP IPA (Received Pronunciation - British English)
"""

from phonemizer import phonemize
from typing import Optional
import eng_to_ipa as ipa
import re
from typing import Optional

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
    "thanks": "θænks",
    "really": "rɪali",
    "one": "wʌn",
    "at": "ət",
    "of": "əv",
    "from":	"frəm",
    "and": "ən",
    "grand": "ɡrænd", 
    "ambition": "æmbɪʃən",
    "a": "ə",	
    
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
    
    # Palabras comunes con /e/ (DRESS vowel)
    "red": "red",
    "bed": "bed",
    "ten": "ten",
    "pen": "pen",
    "men": "men",
    "when": "wen",
    "then": "ðen",
    "them": "ðem",
    "get": "get",
    "let": "let",
    "met": "met",
    "set": "set",
    "net": "net",
    "wet": "wet",
    "yet": "jet",
    "yes": "jes",
    "help": "help",
    "tell": "tel",
    "well": "wel",
    "sell": "sel",
    "fell": "fel",
    "bell": "bel",
    "cell": "sel",
    "left": "left",
    "next": "nekst",
    "best": "best",
    "rest": "rest",
    "west": "west",
    "nest": "nest",
    "chest": "tʃest",
    "fresh": "freʃ",
    "dress": "dres",
    "press": "pres",
    "less": "les",
    "mess": "mes",
    "guess": "ges",
    "bless": "bles",
    "stress": "stres",
    "express": "ɪkˈspres",
    "success": "səkˈses",
    "progress": "ˈprəʊgres",  # noun form
    "address": "əˈdres",
    "access": "ˈækses",
    "process": "ˈprəʊses",  # noun form
    "possess": "pəˈzes",
    "assess": "əˈses",
    "unless": "ənˈles",
    "impress": "ɪmˈpres",
    "suppress": "səˈpres",
    "depress": "dɪˈpres",
    "compress": "kəmˈpres",
    
    # Palabras de poesía/literatura comunes
    "roses": "ˈrəʊzez",
    "violets": "ˈvaɪəlets",
    "blue": "bluː",
    "great": "greɪt",
    "you": "juː",
    
    # Palabras adicionales comunes
    "back": "bæk",
    "our": "aʊə",
    "weekly": "ˈwiːkli",
    "time": "taɪm",
    "now": "naʊ",
    "today": "təˈdeɪ",
    "by": "baɪ",
    "young": "jʌŋ",
    "blogger": "ˈblɒɡə",
    "travel": "ˈtrævəl",
    "good": "ɡʊd",
    "hi": "haɪ",
    "justin": "ˈdʒʌstɪn",
    
    # Palabras con TRAP vowel /æ/ que suelen transcribirse mal
    "happy": "ˈhæpi",
    "animal": "ˈænɪməl",
    "cat": "kæt",
    "bad": "bæd",
    "hand": "hænd",
    "man": "mæn",
    "thank": "θæŋk",
    "family": "ˈfæməli",
    "black": "blæk",
    "track": "træk",
    "pack": "pæk",
    "fact": "fækt",
    "act": "ækt",
    "add": "æd",
    "bag": "bæɡ",
    "hat": "hæt",
    "sat": "sæt",
    "ran": "ræn",
    "van": "væn",
    "plan": "plæn",
    "every": "ˈevri",
    "it's": "ɪts",
    "to": "tə",
    "be": "bi",
}

# Diccionario de correcciones específicas para RP IPA (fallback)
RP_CORRECTIONS = {
    # Palabras específicas con problemas
    'hapi': 'ˈhæpi',
    'anɪməl': 'ˈænɪməl',  # Corrección para 'animal'
    
    # Corrección para 'every' - usar 'i' final en lugar de 'ɪ'
    'evrɪ': 'ˈevri',    # Cambiar ɪ final a i y agregar stress mark
    
    # Patrones comunes problemáticos
    'ɐmeɪzɪŋ': 'əˈmeɪzɪŋ',
    'ɐbsəluːtli': 'ˈæbsəluːtli',
    'ɐbaʊt': 'əˈbaʊt',
    'ɐgriː': 'əˈɡriː',
    'ɐnʌðər': 'əˈnʌðə',
}


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


def get_rp_transcription_from_dict(word: str) -> Optional[str]:
    """
    Obtiene la transcripción RP de una palabra desde el diccionario especializado.
    
    Args:
        word (str): Palabra a transcribir
    
    Returns:
        Optional[str]: Transcripción RP o None si no está en el diccionario
    """
    word_clean = word.lower().strip()
    # Remover puntuación básica
    word_clean = re.sub(r'[^\w]', '', word_clean)
    
    return RP_WORD_DICTIONARY.get(word_clean)


def fix_rp_ipa_issues(text: str) -> str:
    """
    Corrige problemas específicos del RP IPA generado por espeak
    
    Args:
        text (str): Texto IPA con posibles errores
        
    Returns:
        str: Texto IPA corregido
    """
    if not text:
        return text
    
    fixed = text
    
    # 1. Corregir ɐ -> ə (reemplazar TODAS las ocurrencias de ɐ con ə)
    # Convertir absolutamente todos los casos de ɐ a ə
    fixed = fixed.replace('ɐ', 'ə')
    
    # 2. Aplicar correcciones de palabras específicas
    for incorrect, correct in RP_CORRECTIONS.items():
        fixed = fixed.replace(incorrect, correct)
    
    # 3. Corregir problemas de stress marks faltantes en palabras comunes
    # Happy y variantes (evitar doble stress mark)
    fixed = re.sub(r'\b(?:ˈ)?hæpi\b', 'ˈhæpi', fixed)
    
    # 4. Stress marks y limpieza final ya se maneja en otros pasos
    
    # 5. Limpiar stress marks duplicados
    fixed = re.sub(r'ˈˈ+', 'ˈ', fixed)
    
    return fixed


def transform_symbols(text: str) -> str:
    """
    Transforma símbolos según las reglas específicas:
    - Comas ',' → '/'
    - Puntos '.' → '//'
    - Signos de exclamación '!' → '(!)'
    - Signos de interrogación '?' → '(?)'
    
    Args:
        text (str): Texto con símbolos originales
        
    Returns:
        str: Texto con símbolos transformados
    """
    if not text:
        return text
    
    # Aplicar transformaciones en orden específico
    transformed = text
    
    # Transformar ! a (!)
    transformed = transformed.replace('!', '(!)')
    
    # Transformar ? a (?)
    transformed = transformed.replace('?', '(?)')
    
    # Transformar . a // (hacer esto después de ! y ? para evitar conflictos)
    transformed = transformed.replace('.', ' //')
    
    # Transformar , a /
    transformed = transformed.replace(',', ' /')
    
    return transformed


class RPIPAService:
    """Servicio para transcripción fonética RP IPA"""
    
    def __init__(self):
        self.backend = 'espeak'
        self.language = 'en-gb'  # British English
    
    def transcribe(self, text: str) -> str:
        """
        Transcribe texto inglés a notación IPA RP (British)
        Preserva los saltos de línea del texto original.
        
        Args:
            text (str): Texto en inglés para transcribir
            
        Returns:
            str: Transcripción en notación IPA RP
        """
        if not text or not text.strip():
            return ""
        
        # Procesar línea por línea para preservar formato
        lines = text.splitlines()
        transcribed_lines = []
        
        for line in lines:
            if not line.strip():
                # Línea vacía, preservar
                transcribed_lines.append('')
                continue
                
            try:
                # Primero intentar transcribir palabra por palabra con el diccionario
                transcribed_line = self._transcribe_line_with_dict(line.strip())
                transcribed_lines.append(transcribed_line)
                
            except Exception as e:
                # Fallback a eng_to_ipa si phonemizer falla
                try:
                    fallback_result = ipa.convert(line.strip())
                    cleaned_fallback = self._clean_ipa_output(fallback_result)
                    transcribed_lines.append(cleaned_fallback)
                except Exception as fallback_error:
                    raise Exception(f"Error in RP IPA transcription: {str(e)}. Fallback error: {str(fallback_error)}")
        
        # Unir las líneas preservando los saltos de línea originales
        return '\n'.join(transcribed_lines)
    
    def _transcribe_line_with_dict(self, line: str) -> str:
        """
        Transcribe una línea usando primero el diccionario RP_WORD_DICTIONARY
        y luego phonemizer como fallback para palabras no encontradas.
        
        Args:
            line (str): Línea a transcribir
            
        Returns:
            str: Línea transcrita
        """
        if not line:
            return ""
        
        # Dividir en palabras, preservando puntuación
        words = re.findall(r'\b\w+\b|[.,!?;:\'-]', line)
        transcribed_words = []
        
        for word in words:
            if re.match(r'[.,!?;:\'-]', word):
                # Es puntuación, mantener
                transcribed_words.append(word)
            else:
                # Es palabra, buscar primero en el diccionario
                dict_transcription = get_rp_transcription_from_dict(word)
                if dict_transcription:
                    # Encontrada en el diccionario, usar esa transcripción
                    transcribed_words.append(dict_transcription)
                else:
                    # No encontrada en diccionario, usar phonemizer como fallback
                    try:
                        phonemizer_result = phonemize(
                            word,
                            language=self.language,
                            backend=self.backend,
                            strip=True,
                            preserve_punctuation=False,
                            njobs=1
                        )
                        # Limpiar el resultado de phonemizer
                        cleaned_word = self._clean_ipa_output(phonemizer_result)
                        transcribed_words.append(cleaned_word)
                    except Exception:
                        # Si phonemizer falla, usar eng_to_ipa como último recurso
                        try:
                            fallback_result = ipa.convert(word.lower())
                            cleaned_fallback = self._clean_ipa_output(fallback_result)
                            transcribed_words.append(cleaned_fallback)
                        except Exception:
                            # Si todo falla, mantener la palabra original
                            transcribed_words.append(word)
        
        # Unir resultado de la línea
        line_result = ' '.join(transcribed_words)
        
        # Limpiar espacios extra alrededor de puntuación
        line_result = re.sub(r'\s+([.,!?;:\'-])', r'\1', line_result)
        line_result = re.sub(r'\s{2,}', ' ', line_result.strip())
        
        # Aplicar transformaciones de símbolos finales
        line_result = transform_symbols(line_result)
        
        return line_result
    
    def _clean_ipa_output(self, ipa_text: str) -> str:
        """
        Limpia la salida de IPA preservando puntuación importante
        
        Args:
            ipa_text (str): Texto IPA sin limpiar
            
        Returns:
            str: Texto IPA limpio con puntuación preservada
        """
        if not ipa_text:
            return ""
        
        # Preservar puntuación importante antes de limpiar espacios
        # Normalizar espacios pero preservar puntuación
        cleaned = re.sub(r'\s+', ' ', ipa_text)
        
        # Convertir ɹ a r según convención universitaria
        cleaned = cleaned.replace('ɹ', 'r')
        cleaned = cleaned.replace('bɹ', 'br')  # Para casos como "brown"
        
        # Convertir ɛ a e según convención universitaria para RP
        cleaned = cleaned.replace('ɛ', 'e')
        
        # *** CONVERSIÓN GLOBAL DE SCHWA ***
        # Asegurar que TODAS las ɐ se conviertan a ə (schwa estándar)
        cleaned = cleaned.replace('ɐ', 'ə')
        
        # *** CORRECCIONES ESPECÍFICAS PARA RP IPA ***
        # Corregir problemas de schwa y stress marks
        cleaned = fix_rp_ipa_issues(cleaned)
        
        # Asegurar que la puntuación no tenga espacios extra antes
        cleaned = re.sub(r'\s+([.!?,])', r'\1', cleaned)
        
        # Eliminar espacios dobles
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)
        
        # Aplicar transformaciones de símbolos
        cleaned = transform_symbols(cleaned)
        
        return cleaned.strip()
    
    def is_available(self) -> bool:
        """
        Verifica si el servicio está disponible
        
        Returns:
            bool: True si el servicio puede ser usado
        """
        try:
            test_result = self.transcribe("test")
            return bool(test_result)
        except:
            return False


# Instancia global del servicio
rp_ipa_service = RPIPAService()


def transcribe_to_rp_ipa(text: str) -> str:
    """
    Función de conveniencia para transcribir texto a RP IPA
    
    Args:
        text (str): Texto en inglés para transcribir
        
    Returns:
        str: Transcripción en notación IPA RP
    """
    return rp_ipa_service.transcribe(text)