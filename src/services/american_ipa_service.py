"""
Servicio para transcripción fonética American IPA (American English)
"""

from phonemizer import phonemize
from typing import Optional
import eng_to_ipa as ipa
import re
from .weak_forms_processor import process_weak_forms_in_transcription


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


class AmericanIPAService:
    """Servicio para transcripción fonética American IPA"""
    
    def __init__(self):
        self.backend = 'espeak'
        self.language = 'en-us'  # American English
    
    def transcribe(self, text: str, use_weak_forms: bool = True) -> str:
        """
        Transcribe texto inglés a notación IPA American
        Preserva los saltos de línea del texto original.
        
        Args:
            text (str): Texto en inglés para transcribir
            use_weak_forms (bool): Si aplicar formas débiles
            
        Returns:
            str: Transcripción en notación IPA American
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
                # Usar phonemizer con configuración americana
                result = phonemize(
                    line.strip(),
                    language=self.language,
                    backend=self.backend,
                    strip=True,
                    preserve_punctuation=True,
                    njobs=1
                )
                
                # Limpiar el resultado y aplicar ajustes específicos americanos
                cleaned_result = self._clean_and_americanize_ipa(result)
                transcribed_lines.append(cleaned_result)
                
            except Exception as e:
                # Fallback a eng_to_ipa si phonemizer falla
                try:
                    fallback_result = ipa.convert(line.strip())
                    cleaned_fallback = self._clean_and_americanize_ipa(fallback_result)
                    transcribed_lines.append(cleaned_fallback)
                except Exception as fallback_error:
                    raise Exception(f"Error in American IPA transcription: {str(e)}. Fallback error: {str(fallback_error)}")
        
        # Unir las líneas preservando los saltos de línea originales
        base_transcription = '\n'.join(transcribed_lines)
        
        # Aplicar procesamiento de formas débiles
        final_transcription = process_weak_forms_in_transcription(
            text, base_transcription, "american", use_weak_forms
        )
        
        return final_transcription
    
    def _clean_and_americanize_ipa(self, ipa_text: str) -> str:
        """
        Limpia la salida de IPA, aplica ajustes específicos para pronunciación americana
        y preserva puntuación importante
        
        Args:
            ipa_text (str): Texto IPA sin limpiar
            
        Returns:
            str: Texto IPA limpio con ajustes americanos y puntuación preservada
        """
        if not ipa_text:
            return ""
        
        # Normalizar espacios pero preservar puntuación
        cleaned = re.sub(r'\s+', ' ', ipa_text)
        
        # Aplicar algunas transformaciones específicas para American IPA
        # Estas son reglas comunes de diferencias entre RP y American
        
        # Transformaciones típicas American vs British:
        # /ɑː/ (British) -> /ɑ/ (American) en palabras como "car", "start"
        cleaned = cleaned.replace('ɑː', 'ɑ')
        
        # /ɒ/ (British) -> /ɑ/ (American) en palabras como "hot", "lot"
        cleaned = cleaned.replace('ɒ', 'ɑ')
        
        # /æ/ permanece en American (no cambiar a /ɑː/ como en British)
        
        # R-colored vowels - más prominente en American
        # Esto es aproximado, phonemizer ya debería manejar esto con en-us
        
        # Convertir ɹ a r según convención universitaria
        cleaned = cleaned.replace('ɹ', 'r')
        cleaned = cleaned.replace('bɹ', 'br')  # Para casos como "brown"
        
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
american_ipa_service = AmericanIPAService()


def transcribe_to_american_ipa(text: str, use_weak_forms: bool = True) -> str:
    """
    Función de conveniencia para transcribir texto a American IPA
    
    Args:
        text (str): Texto en inglés para transcribir
        use_weak_forms (bool): Si aplicar formas débiles
        
    Returns:
        str: Transcripción en notación IPA American
    """
    return american_ipa_service.transcribe(text, use_weak_forms)
