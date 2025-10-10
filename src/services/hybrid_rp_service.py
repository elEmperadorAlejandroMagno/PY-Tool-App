"""
Servicio híbrido que combina el Longman Dictionary Online con nuestro servicio RP local.
Prioriza las transcripciones auténticas del Longman y usa fallback local cuando sea necesario.
"""

from typing import Optional, List, Dict
import re
from src.services.longman_dictionary_service import get_longman_service
from src.services.rp_phonetic_service import transcribe_word_to_rp, get_rp_transcription_from_dict

class HybridRPService:
    """
    Servicio que combina múltiples fuentes para obtener transcripciones RP precisas.
    
    Orden de prioridad:
    1. Longman Dictionary Online (fuente más auténtica)
    2. Diccionario RP local (palabras comunes pre-definidas)
    3. Conversión GA->RP (algoritmo local)
    """
    
    def __init__(self, use_longman: bool = True):
        self.use_longman = use_longman
        self.longman_service = get_longman_service() if use_longman else None
        
        # Estadísticas de uso
        self.stats = {
            'longman_hits': 0,
            'local_dict_hits': 0,
            'conversion_hits': 0,
            'total_requests': 0
        }
    
    def get_pronunciation(self, word: str) -> Optional[str]:
        """
        Obtiene la transcripción RP de una palabra usando el método híbrido.
        
        Args:
            word (str): Palabra a transcribir
            
        Returns:
            Optional[str]: Transcripción IPA RP o None si no se encuentra
        """
        if not word or not word.strip():
            return None
        
        self.stats['total_requests'] += 1
        cleaned_word = word.lower().strip()
        
        # Método 1: Intentar con Longman Dictionary (más auténtico)
        if self.use_longman and self.longman_service:
            try:
                longman_result = self.longman_service.get_word_pronunciation(cleaned_word)
                if longman_result:
                    self.stats['longman_hits'] += 1
                    return longman_result
            except Exception as e:
                print(f"Error consultando Longman para '{word}': {e}")
        
        # Método 2: Diccionario RP local (palabras comunes)
        local_result = get_rp_transcription_from_dict(cleaned_word)
        if local_result:
            self.stats['local_dict_hits'] += 1
            return local_result
        
        # Método 3: Conversión GA->RP (fallback)
        try:
            conversion_result = transcribe_word_to_rp(cleaned_word)
            if conversion_result and conversion_result != cleaned_word:
                self.stats['conversion_hits'] += 1
                return conversion_result
        except Exception as e:
            print(f"Error en conversión RP para '{word}': {e}")
        
        # No se pudo obtener transcripción
        return None
    
    def transcribe_text(self, text: str) -> str:
        """
        Transcribe un texto completo usando el servicio híbrido.
        
        Args:
            text (str): Texto en inglés para transcribir
            
        Returns:
            str: Texto transcrito a IPA RP
        """
        if not text:
            return ""
        
        # Limpiar y dividir texto en palabras
        cleaned_text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
        words = re.findall(r'\b\w+\b|[.,!?;:\'-]', cleaned_text)
        
        transcribed_parts = []
        
        for part in words:
            if re.match(r'[.,!?;:\'-]', part):
                # Es puntuación, mantener como está
                transcribed_parts.append(part)
            else:
                # Es una palabra, transcribir
                pronunciation = self.get_pronunciation(part)
                if pronunciation:
                    transcribed_parts.append(pronunciation)
                else:
                    # Si no se puede transcribir, mantener palabra original
                    transcribed_parts.append(part.lower())
        
        # Unir resultado
        result = ' '.join(transcribed_parts)
        
        # Limpiar espacios extra alrededor de puntuación
        result = re.sub(r'\s+([.,!?;:\'-])', r'\\1', result)
        result = re.sub(r'\s+', ' ', result.strip())
        
        return result
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtiene estadísticas de uso del servicio"""
        return self.stats.copy()
    
    def get_success_rate(self) -> float:
        """Calcula la tasa de éxito de transcripciones"""
        if self.stats['total_requests'] == 0:
            return 0.0
        
        successful = (
            self.stats['longman_hits'] + 
            self.stats['local_dict_hits'] + 
            self.stats['conversion_hits']
        )
        
        return successful / self.stats['total_requests']
    
    def reset_statistics(self):
        """Reinicia las estadísticas"""
        for key in self.stats:
            self.stats[key] = 0
    
    def enable_longman(self, enable: bool = True):
        """Habilita o deshabilita el uso del diccionario Longman"""
        self.use_longman = enable
        if enable and not self.longman_service:
            self.longman_service = get_longman_service()
    
    def print_statistics(self):
        """Imprime estadísticas de uso del servicio"""
        print("=== Estadísticas del Servicio Híbrido RP ===")
        print(f"Total de consultas: {self.stats['total_requests']}")
        print(f"Longman Dictionary: {self.stats['longman_hits']} ({self.stats['longman_hits']/max(1, self.stats['total_requests'])*100:.1f}%)")
        print(f"Diccionario local:  {self.stats['local_dict_hits']} ({self.stats['local_dict_hits']/max(1, self.stats['total_requests'])*100:.1f}%)")
        print(f"Conversión GA->RP:  {self.stats['conversion_hits']} ({self.stats['conversion_hits']/max(1, self.stats['total_requests'])*100:.1f}%)")
        print(f"Tasa de éxito:      {self.get_success_rate()*100:.1f}%")
        print("=" * 50)

# Instancia global del servicio híbrido
_hybrid_service = None

def get_hybrid_rp_service(use_longman: bool = True) -> HybridRPService:
    """Obtiene la instancia del servicio híbrido RP"""
    global _hybrid_service
    if _hybrid_service is None:
        _hybrid_service = HybridRPService(use_longman=use_longman)
    return _hybrid_service

def test_hybrid_service():
    """Función de prueba del servicio híbrido"""
    print("=== Test del Servicio Híbrido RP ===\\n")
    
    service = get_hybrid_rp_service(use_longman=True)
    
    # Palabras de prueba con diferentes fuentes esperadas
    test_cases = [
        ("hello", "Debería venir de Longman o diccionario local"),
        ("world", "Debería venir de diccionario local"),
        ("pronunciation", "Palabra académica común"),
        ("ask", "BATH word - diferencia GA/RP"),
        ("dance", "BATH word - diferencia GA/RP"),
        ("car", "R no rótica"),
        ("beautiful", "Palabra compleja"),
        ("university", "Palabra académica"),
        ("testing", "Palabra de prueba"),
        ("example", "Otra palabra de prueba"),
    ]
    
    print("Palabra".ljust(15) + "Transcripción RP".ljust(25) + "Nota")
    print("=" * 70)
    
    for word, note in test_cases:
        pronunciation = service.get_pronunciation(word)
        if pronunciation:
            print(f"{word:<15} /{pronunciation:<23}/ {note}")
        else:
            print(f"{word:<15} {'No encontrado':<23} {note}")
    
    print()
    service.print_statistics()
    
    # Test de transcripción de texto completo
    print("\\n=== Test de Transcripción de Texto ===")
    test_sentence = "Hello world, this is a pronunciation test with British words like ask, dance and car."
    print(f"Original: {test_sentence}")
    
    transcribed = service.transcribe_text(test_sentence)
    print(f"RP (IPA): {transcribed}")

if __name__ == "__main__":
    test_hybrid_service()