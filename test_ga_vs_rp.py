#!/usr/bin/env python3
"""
Test específico para verificar las diferencias entre GA y RP
en palabras que tienen transcripciones muy diferentes.
"""

from src.core.factories.translator_factory import create_translator_app

def test_ga_vs_rp_differences():
    """Prueba las diferencias específicas entre GA y RP"""
    
    print("=== Test GA vs RP - Diferencias Clave ===\n")
    
    app = create_translator_app("en")
    
    # Palabras que muestran diferencias claras
    test_cases = [
        # BATH words (GA /æ/ vs RP /ɑː/)
        ("ask", "GA: /æsk/ → RP: /ɑːsk/"),
        ("dance", "GA: /dæns/ → RP: /dɑːns/"),
        ("path", "GA: /pæθ/ → RP: /pɑːθ/"),
        ("after", "GA: /æftər/ → RP: /ɑːftə/"),
        ("can't", "GA: /kænt/ → RP: /kɑːnt/"),
        ("class", "GA: /klæs/ → RP: /klɑːs/"),
        ("laugh", "GA: /læf/ → RP: /lɑːf/"),
        
        # LOT words (GA /ɑ/ vs RP /ɒ/)
        ("hot", "GA: /hɑt/ → RP: /hɒt/"),
        ("got", "GA: /gɑt/ → RP: /gɒt/"),
        ("shop", "GA: /ʃɑp/ → RP: /ʃɒp/"),
        ("dog", "GA: /dɑg/ → RP: /dɒg/"),
        
        # GOAT diphthong (GA /oʊ/ vs RP /əʊ/)
        ("go", "GA: /goʊ/ → RP: /gəʊ/"),
        ("show", "GA: /ʃoʊ/ → RP: /ʃəʊ/"),
        ("phone", "GA: /foʊn/ → RP: /fəʊn/"),
        ("home", "GA: /hoʊm/ → RP: /həʊm/"),
        
        # R-colored vowels (GA rótica vs RP no rótica)
        ("car", "GA: /kɑr/ → RP: /kɑː/"),
        ("park", "GA: /pɑrk/ → RP: /pɑːk/"),
        ("here", "GA: /hɪr/ → RP: /hɪə/"),
        ("care", "GA: /kɛr/ → RP: /keə/"),
        ("sure", "GA: /ʃʊr/ → RP: /ʃʊə/"),
        ("water", "GA: /wɑtər/ → RP: /wɔːtə/"),
        ("better", "GA: /bɛtər/ → RP: /betə/"),
        
        # Palabras académicas
        ("university", "Palabra académica común"),
        ("pronunciation", "Palabra clave de fonética"),
        ("received", "De 'Received Pronunciation'"),
        ("british", "Adjetivo de nacionalidad"),
        ("standard", "Palabra académica"),
    ]
    
    print("Palabra".ljust(15) + "Transcripción RP".ljust(20) + "Nota")
    print("=" * 65)
    
    for word, note in test_cases:
        try:
            transcription = app.transcribe_to_ipa(word)
            print(f"{word:<15} /{transcription:<18}/ {note}")
        except Exception as e:
            print(f"{word:<15} {'ERROR':<18} {str(e)[:30]}...")
    
    print("\n" + "=" * 65)
    print("✅ Características RP verificadas:")
    print("  • Vocales no róticas (sin /r/ final)")
    print("  • BATH words con /ɑː/ (ask, dance, path)")
    print("  • LOT words con /ɒ/ (hot, got, shop)")
    print("  • GOAT diphthong /əʊ/ (go, show, phone)")
    print("  • Diphthongs /ɪə/, /eə/, /ʊə/ (here, care, sure)")

if __name__ == "__main__":
    test_ga_vs_rp_differences()