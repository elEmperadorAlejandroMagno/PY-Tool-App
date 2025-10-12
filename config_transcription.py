#!/usr/bin/env python3
"""
Script de configuración para los modos de transcripción fonética.

Uso:
    python config_transcription.py fast    # Modo rápido (solo local)
    python config_transcription.py hybrid  # Modo híbrido con Longman
    python config_transcription.py status  # Ver configuración actual
"""

import sys
from src.services.hybrid_rp_service import configure_fast_mode, get_hybrid_rp_service

def show_status():
    """Muestra el estado actual de la configuración"""
    service = get_hybrid_rp_service()
    
    print("=== Estado actual de la transcripción fonética ===")
    print(f"Longman habilitado: {'✅ Sí' if service.use_longman else '❌ No'}")
    
    if service.use_longman and service.longman_service:
        print(f"Delay entre requests: {service.longman_service.request_delay}s")
        print(f"Cache de Longman: {service.longman_service.get_cache_size()} entradas")
    
    stats = service.get_statistics()
    if stats['total_requests'] > 0:
        print(f"\nEstadísticas de la sesión actual:")
        print(f"  Total consultas: {stats['total_requests']}")
        print(f"  Longman: {stats['longman_hits']}")
        print(f"  Diccionario local: {stats['local_dict_hits']}")  
        print(f"  Conversión GA->RP: {stats['conversion_hits']}")
        print(f"  Tasa de éxito: {service.get_success_rate()*100:.1f}%")
    
    print("=" * 50)

def configure_mode(mode: str):
    """Configura el modo de transcripción"""
    if mode == "fast":
        configure_fast_mode(True)
    elif mode == "hybrid":
        configure_fast_mode(False)
    else:
        print(f"❌ Modo desconocido: {mode}")
        return False
    return True

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python config_transcription.py fast    # Modo rápido")
        print("  python config_transcription.py hybrid  # Modo híbrido con Longman")
        print("  python config_transcription.py status  # Ver estado actual")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_status()
    elif command in ["fast", "hybrid"]:
        if configure_mode(command):
            show_status()
    else:
        print(f"❌ Comando desconocido: {command}")
        print("Comandos disponibles: fast, hybrid, status")

if __name__ == "__main__":
    main()