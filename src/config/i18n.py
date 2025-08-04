"""
Simplified internationalization (i18n) system for the translator app.
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path

class TranslationManager:
    """Simple translation manager that loads from JSON."""
    
    def __init__(self):
        # Get path to translations.json
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        self.translations_file = str(project_root / "translations" / "translations.json")
        self._cache = None
    
    def load_translations(self) -> Dict[str, Any]:
        """Load translations from JSON file with caching."""
        if self._cache is None:
            try:
                with open(self.translations_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                # Fallback to basic English
                self._cache = {
                    "en": {
                        "title": "Translator",
                        "insert_text": "Insert text",
                        "translation": "Translation",
                        "translate": "Translate",
                        "translate_file": "Translate File",
                        "select_file": "Select File",
                        "output_path": "Translated file saved at"
                    }
                }
        return self._cache
    
    def get_text(self, language: str) -> str:
        """Get translated text for a key and language."""
        translations = self.load_translations()
        
        # Try target language first
        if language in translations:
            return translations[language]
        
        # Fallback to English
        if "en" in translations:
            return translations["en"]
        
        # Last resort: return the key
        raise KeyError(f"Translation for '{language}' not found")
    
    def get_available_languages(self) -> List[str]:
        """Get list of available language codes."""
        return list(self.load_translations().keys())

# Global instance
_translation_manager = TranslationManager()

# Simple functions for easy use
def get_translations() -> Dict[str, Any]:
    """Get all translations."""
    return _translation_manager.load_translations()

def get_text(key: str, language: str) -> str:
    """Get translated text."""
    return _translation_manager.get_text(key, language)

def get_available_languages() -> List[str]:
    """Get available language codes."""
    return _translation_manager.get_available_languages()
