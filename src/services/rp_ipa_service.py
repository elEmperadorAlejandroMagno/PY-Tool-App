"""
Servicio para transcripción fonética RP IPA (Received Pronunciation - British English)
"""

from phonemizer import phonemize
from typing import Optional
import eng_to_ipa as ipa
import re

# Diccionario de correcciones específicas para RP IPA
RP_CORRECTIONS = {
    # Palabras específicas con problemas
    'hapi': 'ˈhæpi',
    
    # Corrección para 'every' - usar 'i' final en lugar de 'ɪ'
    'evrɪ': 'ˈevri',    # Cambiar ɪ final a i y agregar stress mark
    
    # Patrones comunes problemáticos
    'ɐmeɪzɪŋ': 'əˈmeɪzɪŋ',
    'ɐbsəluːtli': 'ˈæbsəluːtli',
    'ɐbaʊt': 'əˈbaʊt',
    'ɐgriː': 'əˈɡriː',
    'ɐnʌðər': 'əˈnʌðə',
}


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
    
    # 1. Corregir ɐ -> ə (problema principal de la schwa)
    # Solo en contextos donde debería ser schwa
    fixed = re.sub(r'\bɐ\b', 'ə', fixed)  # artículos como "a"
    fixed = re.sub(r'\bɐ([mnlr])', r'ə\1', fixed)  # antes de consonantes como en "amazing"
    
    # 2. Aplicar correcciones de palabras específicas
    for incorrect, correct in RP_CORRECTIONS.items():
        fixed = fixed.replace(incorrect, correct)
    
    # 3. Corregir problemas de stress marks faltantes en palabras comunes
    # Happy y variantes (evitar doble stress mark)
    fixed = re.sub(r'\b(?:ˈ)?hæpi\b', 'ˈhæpi', fixed)
    
    # 4. Asegurar que la schwa esté en posición átona correcta
    # Para palabras que empiezan con vocal átona seguida de consonante+vocal tónica
    fixed = re.sub(r'\bɐ([bcdfghjklmnpqrstvwxyz])([aeiouy])', r'ə\1\2', fixed)
    
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
    transformed = transformed.replace('.', '//')
    
    # Transformar , a /
    transformed = transformed.replace(',', '/')
    
    return transformed


class RPIPAService:
    """Servicio para transcripción fonética RP IPA"""
    
    def __init__(self):
        self.backend = 'espeak'
        self.language = 'en-gb'  # British English
    
    def transcribe(self, text: str) -> str:
        """
        Transcribe texto inglés a notación IPA RP (British)
        
        Args:
            text (str): Texto en inglés para transcribir
            
        Returns:
            str: Transcripción en notación IPA RP
        """
        if not text or not text.strip():
            return ""
        
        try:
            # Usar phonemizer con configuración británica
            result = phonemize(
                text.strip(),
                language=self.language,
                backend=self.backend,
                strip=True,
                preserve_punctuation=True,
                njobs=1
            )
            
            # Limpiar el resultado
            return self._clean_ipa_output(result)
            
        except Exception as e:
            # Fallback a eng_to_ipa si phonemizer falla
            try:
                fallback_result = ipa.convert(text.strip())
                return self._clean_ipa_output(fallback_result)
            except Exception as fallback_error:
                raise Exception(f"Error in RP IPA transcription: {str(e)}. Fallback error: {str(fallback_error)}")
    
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