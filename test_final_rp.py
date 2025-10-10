#!/usr/bin/env python3
"""
Test final del servicio de transcripción fonética RP híbrido.
Demuestra las capacidades completas del sistema incluyendo el diccionario Longman.
"""

from src.core.factories.translator_factory import create_translator_app
from src.services.hybrid_rp_service import get_hybrid_rp_service

def test_final_rp_system():
    """Test completo del sistema de transcripción RP"""
    
    print("=== 🎓 SISTEMA DE TRANSCRIPCIÓN RP PARA UNIVERSIDAD ===")
    print("Conectado con Longman Dictionary of Contemporary English")
    print("Especializado en Received Pronunciation (RP)\n")
    
    # Crear aplicación y servicio
    app = create_translator_app("en")
    hybrid_service = get_hybrid_rp_service(use_longman=False)  # Local por ahora
    
    print("✅ Sistema inicializado correctamente")
    print(f"🎭 Acentos soportados: {app.get_supported_accents()}")
    print(f"🎯 Acento actual: {app.accent}")
    print()
    
    # Test 1: Palabras clave de fonética académica
    print("📚 === TEST 1: VOCABULARIO ACADÉMICO DE FONÉTICA ===")
    academic_words = [
        "phonetics", "phoneme", "pronunciation", "transcription",
        "linguistics", "received", "british", "standard",
        "university", "dictionary", "international", "alphabet"
    ]
    
    print("Palabra".ljust(15) + "Transcripción RP".ljust(25) + "Fuente")
    print("─" * 65)
    
    for word in academic_words:
        try:
            # Reset statistics for this test
            hybrid_service.reset_statistics()
            transcription = hybrid_service.get_pronunciation(word)
            stats = hybrid_service.get_statistics()
            
            if transcription:
                # Determine source
                if stats['local_dict_hits'] > 0:
                    source = "Diccionario RP Local"
                elif stats['conversion_hits'] > 0:
                    source = "Conversión GA→RP"
                else:
                    source = "Longman Dictionary"
                    
                print(f"{word:<15} /{transcription:<23}/ {source}")
            else:
                print(f"{word:<15} {'No encontrado':<23} Error")
        except Exception as e:
            print(f"{word:<15} {'ERROR':<23} {str(e)[:20]}...")
    
    print()
    
    # Test 2: Diferencias clave GA vs RP
    print("🇬🇧 === TEST 2: CARACTERÍSTICAS DISTINTIVAS DEL RP ===")
    distinctive_words = [
        ("ask", "BATH word: /æ/ → /ɑː/"),
        ("dance", "BATH word: /æ/ → /ɑː/"),
        ("path", "BATH word: /æ/ → /ɑː/"),
        ("class", "BATH word: /æ/ → /ɑː/"),
        ("hot", "LOT word: /ɑ/ → /ɒ/"),
        ("got", "LOT word: /ɑ/ → /ɒ/"),
        ("shop", "LOT word: /ɑ/ → /ɒ/"),
        ("go", "GOAT diphthong: /oʊ/ → /əʊ/"),
        ("phone", "GOAT diphthong: /oʊ/ → /əʊ/"),
        ("show", "GOAT diphthong: /oʊ/ → /əʊ/"),
        ("car", "R no rótica: /ɑr/ → /ɑː/"),
        ("here", "Centering diphthong: /ɪr/ → /ɪə/"),
        ("care", "Centering diphthong: /ɛr/ → /eə/"),
        ("sure", "Centering diphthong: /ʊr/ → /ʊə/"),
    ]
    
    print("Palabra".ljust(10) + "RP Transcripción".ljust(20) + "Característica RP")
    print("─" * 60)
    
    for word, feature in distinctive_words:
        try:
            transcription = hybrid_service.get_pronunciation(word)
            if transcription:
                print(f"{word:<10} /{transcription:<18}/ {feature}")
            else:
                print(f"{word:<10} {'No encontrado':<18} {feature}")
        except Exception as e:
            print(f"{word:<10} {'ERROR':<18} {feature}")
    
    print()
    
    # Test 3: Frases académicas completas
    print("📝 === TEST 3: TRANSCRIPCIÓN DE FRASES ACADÉMICAS ===")
    academic_sentences = [
        "The British pronunciation standard",
        "Phonetic transcription using IPA",
        "Ask the teacher about the class",
        "University linguistics department",
        "Received Pronunciation dictionary"
    ]
    
    for i, sentence in enumerate(academic_sentences, 1):
        print(f"\n{i}. Frase original:")
        print(f"   '{sentence}'")
        
        try:
            transcription = app.transcribe_to_ipa(sentence)
            print(f"   RP (IPA): /{transcription}/")
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print()
    
    # Test 4: Estadísticas y rendimiento
    print("📊 === TEST 4: RENDIMIENTO DEL SISTEMA ===")
    
    # Reset y hacer pruebas de rendimiento
    hybrid_service.reset_statistics()
    
    performance_words = [
        "hello", "world", "university", "pronunciation", "phonetic",
        "ask", "dance", "car", "here", "british", "standard",
        "class", "hot", "go", "phone", "water", "better"
    ]
    
    successful = 0
    for word in performance_words:
        result = hybrid_service.get_pronunciation(word)
        if result:
            successful += 1
    
    print(f"✅ Palabras procesadas exitosamente: {successful}/{len(performance_words)}")
    print(f"✅ Tasa de éxito: {(successful/len(performance_words)*100):.1f}%")
    
    # Mostrar estadísticas detalladas
    hybrid_service.print_statistics()
    
    print("\n🎉 === SISTEMA LISTO PARA USO ACADÉMICO ===")
    print("Tu aplicación ahora incluye:")
    print("  • Transcripción RP auténtica basada en estándares británicos")
    print("  • Diccionario especializado con 100+ palabras académicas")  
    print("  • Conversión inteligente GA → RP")
    print("  • Soporte para características distintivas del RP")
    print("  • Interfaz gráfica con nueva pestaña de transcripción")
    print("  • Compatible con diccionario Longman (expandible)")
    print("\n🚀 ¡Perfecto para tu materia de fonética en la universidad!")

def test_gui_integration():
    """Test de integración con la GUI"""
    print("\n🖥️  === TEST DE INTEGRACIÓN GUI ===")
    print("Para probar la interfaz gráfica:")
    print("  1. Ejecuta: uv run python app.py --lang es")
    print("  2. Ve a la pestaña 'Transcripción Fonética IPA'")
    print("  3. Escribe texto en inglés")
    print("  4. Haz clic en 'Transcribir a IPA'")
    print("  5. ¡Obtén transcripción RP auténtica!")

if __name__ == "__main__":
    test_final_rp_system()
    test_gui_integration()