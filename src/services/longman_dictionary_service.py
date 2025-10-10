"""
Servicio para obtener transcripciones fonéticas IPA RP auténticas
directamente del Longman Dictionary of Contemporary English (LDOCE).
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Optional, List, Dict, Tuple
import urllib.parse

class LongmanDictionaryService:
    """Servicio para consultar transcripciones fonéticas del diccionario Longman"""
    
    def __init__(self):
        self.base_url = "https://www.ldoceonline.com"
        self.search_url = f"{self.base_url}/search/"
        self.session = requests.Session()
        
        # Headers para simular un navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Cache para evitar consultas repetidas
        self._cache = {}
        
        # Límite de velocidad para ser respetuosos
        self.request_delay = 1.0  # segundos entre requests
        self.last_request_time = 0
    
    def _wait_for_rate_limit(self):
        """Espera el tiempo necesario para respetar el límite de velocidad"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            time.sleep(self.request_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _clean_word(self, word: str) -> str:
        """Limpia la palabra para búsqueda"""
        # Remover puntuación y convertir a minúsculas
        cleaned = re.sub(r'[^\w\'-]', '', word.lower().strip())
        return cleaned
    
    def _extract_pronunciation_from_html(self, html: str, word: str) -> Optional[str]:
        """
        Extrae la transcripción fonética del HTML del diccionario Longman
        
        Args:
            html (str): Contenido HTML de la página
            word (str): Palabra buscada
        
        Returns:
            Optional[str]: Transcripción IPA o None si no se encuentra
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscar diferentes patrones donde aparece la transcripción fonética
        pronunciation_selectors = [
            '.PRON',  # Clase común para pronunciación
            '.pron',  # Variante en minúsculas
            'span[class*="pron"]',  # Cualquier clase que contenga "pron"
            '.pronunciation',
            '[data-src-mp3]',  # Elementos con audio que suelen tener transcripción
            '.sound',  # Elementos de sonido
            '.phon',  # Phonetic
        ]
        
        for selector in pronunciation_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Buscar texto que parece una transcripción IPA
                text = element.get_text().strip()
                if self._looks_like_ipa(text):
                    # Limpiar la transcripción
                    cleaned = self._clean_ipa_transcription(text)
                    if cleaned:
                        return cleaned
        
        # Buscar en el texto completo patrones que parecen IPA
        full_text = soup.get_text()
        ipa_pattern = r'/([^/]+)/'  # Buscar contenido entre barras /.../ 
        matches = re.findall(ipa_pattern, full_text)
        
        for match in matches:
            if self._looks_like_ipa(match):
                cleaned = self._clean_ipa_transcription(match)
                if cleaned:
                    return cleaned
        
        return None
    
    def _looks_like_ipa(self, text: str) -> bool:
        """
        Verifica si el texto parece una transcripción IPA
        
        Args:
            text (str): Texto a verificar
        
        Returns:
            bool: True si parece IPA
        """
        if not text or len(text) < 2:
            return False
        
        # Caracteres comunes en IPA
        ipa_chars = set('ɑɒɔɜɛɪʊʌæəɪeɔːɑːɜːiːuːɪəeəʊəɔɪaɪaʊθðʃʒŋʤʧɹjwlmnpbtdkgfvszh')
        
        # Contar caracteres IPA en el texto
        ipa_count = sum(1 for char in text.lower() if char in ipa_chars)
        total_chars = len([c for c in text if c.isalpha() or c in ipa_chars])
        
        # Si más del 30% son caracteres IPA, probablemente es una transcripción
        if total_chars > 0:
            ipa_ratio = ipa_count / total_chars
            return ipa_ratio > 0.3
        
        return False
    
    def _clean_ipa_transcription(self, text: str) -> Optional[str]:
        """
        Limpia la transcripción IPA extraída
        
        Args:
            text (str): Transcripción cruda
        
        Returns:
            Optional[str]: Transcripción limpia o None si no es válida
        """
        if not text:
            return None
        
        # Remover barras de delimitación y espacios extra
        cleaned = text.strip(' /')
        
        # Remover caracteres no deseados pero mantener IPA válidos
        # Mantener letras, símbolos IPA, acentos, espacios y guiones
        cleaned = re.sub(r'[^\w\s\-ɑɒɔɜɛɪʊʌæəɪeɔːɑːɜːiːuːɪəeəʊəɔɪaɪaʊθðʃʒŋʤʧɹjwlmnpbtdkgfvszh\'ˈˌ]', '', cleaned)
        
        # Limpiar espacios múltiples
        cleaned = re.sub(r'\s+', ' ', cleaned.strip())
        
        if len(cleaned) < 2:
            return None
        
        return cleaned
    
    def get_word_pronunciation(self, word: str) -> Optional[str]:
        """
        Obtiene la transcripción fonética de una palabra del diccionario Longman
        
        Args:
            word (str): Palabra a buscar
        
        Returns:
            Optional[str]: Transcripción IPA RP o None si no se encuentra
        """
        cleaned_word = self._clean_word(word)
        
        if not cleaned_word:
            return None
        
        # Verificar cache primero
        if cleaned_word in self._cache:
            return self._cache[cleaned_word]
        
        try:
            # Respetar límite de velocidad
            self._wait_for_rate_limit()
            
            # Construir URL de búsqueda
            search_query = urllib.parse.quote(cleaned_word)
            search_url = f"{self.search_url}?q={search_query}"
            
            # Realizar solicitud
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Extraer pronunciación
            pronunciation = self._extract_pronunciation_from_html(response.text, cleaned_word)
            
            # Cachear resultado (incluso si es None)
            self._cache[cleaned_word] = pronunciation
            
            return pronunciation
            
        except requests.RequestException as e:
            print(f"Error al consultar Longman para '{word}': {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al procesar '{word}': {e}")
            return None
    
    def get_multiple_pronunciations(self, words: List[str]) -> Dict[str, Optional[str]]:
        """
        Obtiene transcripciones para múltiples palabras
        
        Args:
            words (List[str]): Lista de palabras
        
        Returns:
            Dict[str, Optional[str]]: Diccionario palabra -> transcripción
        """
        results = {}
        
        for word in words:
            pronunciation = self.get_word_pronunciation(word)
            results[word] = pronunciation
            
            # Pequeña pausa adicional entre palabras
            time.sleep(0.5)
        
        return results
    
    def clear_cache(self):
        """Limpia el cache de pronunciaciones"""
        self._cache.clear()
    
    def get_cache_size(self) -> int:
        """Obtiene el número de entradas en el cache"""
        return len(self._cache)

# Instancia global del servicio
_longman_service = None

def get_longman_service() -> LongmanDictionaryService:
    """Obtiene la instancia del servicio Longman (singleton)"""
    global _longman_service
    if _longman_service is None:
        _longman_service = LongmanDictionaryService()
    return _longman_service

def get_longman_pronunciation(word: str) -> Optional[str]:
    """
    Función de conveniencia para obtener pronunciación del Longman
    
    Args:
        word (str): Palabra a buscar
    
    Returns:
        Optional[str]: Transcripción IPA RP o None
    """
    service = get_longman_service()
    return service.get_word_pronunciation(word)

def test_longman_service():
    """Función de prueba del servicio Longman"""
    service = get_longman_service()
    
    test_words = ["hello", "world", "pronunciation", "ask", "dance", "car"]
    
    print("=== Test del servicio Longman Dictionary ===")
    print(f"URL base: {service.base_url}")
    print()
    
    for word in test_words:
        print(f"Buscando '{word}'...")
        pronunciation = service.get_word_pronunciation(word)
        if pronunciation:
            print(f"  ✅ {word} → /{pronunciation}/")
        else:
            print(f"  ❌ {word} → No encontrado")
        print()
    
    print(f"Cache size: {service.get_cache_size()} entradas")

if __name__ == "__main__":
    test_longman_service()