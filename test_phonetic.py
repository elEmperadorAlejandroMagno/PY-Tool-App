#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de transcripción fonética IPA RP.
"""

from src.core.factories.translator_factory import create_translator_app

def test_phonetic_transcription():
    """Prueba la funcionalidad de transcripción fonética"""
    
    print("=== Prueba de Transcripción Fonética IPA RP ===\n")
    
    # Crear la aplicación
    app = create_translator_app("en")
    
    # Verificar que la transcripción fonética esté disponible
    if not app.is_phonetic_transcription_available():
        print("❌ La transcripción fonética no está disponible")
        return
    
    print("✅ Transcripción fonética disponible")
    print(f"🎭 Acentos soportados: {app.get_supported_accents()}")
    print(f"🎯 Acento actual: {app.accent}")
    print()
    
    # Palabras de prueba que son comunes en el diccionario Longman
    test_words = [
        "hello",
        "world", 
        "university",
        "pronunciation",
        "phonetic",
        "received",
        "British",
        "standard",
        "dictionary"
    ]
    
    print("🔤 Probando transcripción de palabras:")
    print("-" * 50)
    
    for word in test_words:
        try:
            transcription = app.transcribe_to_ipa(word)
            print(f"{word:15} → {transcription}")
        except Exception as e:
            print(f"{word:15} → Error: {e}")
    
    print()
    
    # Probar con una frase completa
    test_sentence = "Hello world, this is a phonetic transcription test."
    print("📝 Probando transcripción de frase:")
    print("-" * 50)
    print(f"Original: {test_sentence}")
    
    try:
        sentence_transcription = app.transcribe_to_ipa(test_sentence)
        print(f"IPA (RP): {sentence_transcription}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()
    print("=== Fin de la prueba ===")

if __name__ == "__main__":
    test_phonetic_transcription()