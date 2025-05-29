from apps import timer, translator, tik_tak_toe
import argparse
import asyncio

def main():
    parser = argparse.ArgumentParser(description="Selecciona qué aplicación iniciar")
    parser.add_argument("app", choices=["timer", "translator", "tictactoe"], help="Aplicación a ejecutar")
    parser.add_argument("--lang", type=str, default="", help="Idioma de traducción")
    parser.add_argument("--num", type=int, default=1, help="Partidas necesarias en Tic Tac Toe")
    parser.add_argument("--lay", type=str, default="3x3", help="Algoritmo de mezcla")
    parser.add_argument("--mode", type=str, choices=["line", "file"], default="line", help="Modo de traducción: 'line' para una línea, 'file' para archivo")
    parser.add_argument("--filepath", type=str, default="", help="Ruta del archivo a traducir (si mode=file)")

    args = parser.parse_args()

    if args.app == "timer":
        start_timer(args.lay)
    elif args.app == "translator":
        start_translator(args.lang, args.mode, args.filepath)
    elif args.app == "tictactoe":
        start_tictactoe(args.num)

def start_timer(cube_type):
    timer.main()
    # si el usuario aprieta space/enter iniciar/parar tiempo
    # retornar el tiempo final

def start_translator(lang, mode, filepath):
    if mode == "line":
        text = input("Insert your text to translate: ")
        return print(asyncio.run(translator.translator_text(lang, text)))
    elif mode == "file":
        if not filepath:
            print("Debes indicar la ruta del archivo con --filepath")
            return
        translator.translate_file(lang, filepath)
    

def start_tictactoe(num_games):
    tik_tak_toe.play_game(num_games)

if __name__ == '__main__':
    main()
