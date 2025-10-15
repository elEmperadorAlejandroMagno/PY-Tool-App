from src.core.interfaces.phonetic_transcription_interface import PhoneticTranscriptionInterface
from src.services.american_ipa_service import transcribe_to_american_ipa
from src.services.rp_ipa_service import transcribe_to_rp_ipa, is_valid_english_text

class PhoneticTranscriptionImplements(PhoneticTranscriptionInterface):
    """
    Implementación del servicio de transcripción fonética IPA.
    Especializado en Received Pronunciation (RP).
    """
    
    def __init__(self):
        # Lista de acentos soportados
        self._supported_accents = ["rp", "american"]  # RP y American IPA
        
    def transcribe_to_ipa(self, text: str, accent: str = "rp", use_weak_forms: bool = True) -> str:
        """
        Transcribe texto inglés a notación IPA.
        
        Args:
            text (str): Texto en inglés para transcribir
            accent (str): Variante de acento ("rp" para Received Pronunciation)
            use_weak_forms (bool): Si aplicar formas débiles
        
        Returns:
            str: Transcripción IPA del texto
        
        Raises:
            ValueError: Si el texto está vacío o el acento no es soportado
            Exception: Si hay error en la transcripción
        """
        try:
            # Validaciones
            if not text or not text.strip():
                return ""
            
            if not self.is_accent_supported(accent):
                raise ValueError(f"Acento '{accent}' no soportado. Acentos disponibles: {self._supported_accents}")
            
            # Verificar que el texto parece ser inglés
            if not is_valid_english_text(text):
                raise ValueError("El texto no parece estar en inglés. La transcripción IPA requiere texto en inglés.")
            
            # Transcribir según el acento usando servicios específicos
            if accent == "rp":
                return transcribe_to_rp_ipa(text, use_weak_forms)
            elif accent == "american":
                return transcribe_to_american_ipa(text, use_weak_forms)
            else:
                raise ValueError(f"Acento '{accent}' no implementado")
                
        except ValueError:
            # Re-raise ValueError tal como está
            raise
        except Exception as e:
            # Envolver otros errores
            raise Exception(f"Error al transcribir texto: {str(e)}")
    
    def is_accent_supported(self, accent: str) -> bool:
        """
        Verifica si el acento especificado es soportado.
        
        Args:
            accent (str): Código de acento a verificar
        
        Returns:
            bool: True si el acento es soportado, False en caso contrario
        """
        return accent.lower() in self._supported_accents
    
    def get_supported_accents(self) -> list[str]:
        """
        Obtiene la lista de variantes de acento soportadas.
        
        Returns:
            list[str]: Lista de códigos de acento soportados
        """
        return self._supported_accents.copy()
    
    def get_accent_description(self, accent: str) -> str:
        """
        Obtiene la descripción de un acento específico.
        
        Args:
            accent (str): Código de acento
        
        Returns:
            str: Descripción del acento
        """
        accent_descriptions = {
            "rp": "Received Pronunciation (British Standard)",
            "american": "General American (American Standard)"
        }
        
        return accent_descriptions.get(accent.lower(), f"Acento desconocido: {accent}")