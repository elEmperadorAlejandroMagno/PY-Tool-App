from apps import timer, translator, tik_tak_toe
import argparse
import asyncio

def main():
    parser = argparse.ArgumentParser(description="Selecciona qué aplicación iniciar")
    parser.add_argument("app", choices=["timer", "translator", "tictactoe"], help="Aplicación a ejecutar")
    parser.add_argument("--lang", type=str, default= "", help="Argumentos adicionales para idioma de traducción")
    parser.add_argument("--num", type=int, default= 1, help="Argumentos adicionales para definir las partidas necesarias en el juego de Tic Tac Toe")
    parser.add_argument("--lay", type=str, default= "3x3", help="Argumentos adicionales para generar el algoritmo de mezcla")

    args = parser.parse_args()

    if args.app == "timer":
        start_timer(args.lay)
    elif args.app == "translator":
        start_translator(args.lang)
    elif args.app == "tictactoe":
        start_tictactoe(args.num)

def start_timer(cube_type):
    timer.main()
    # si el usuario aprieta space/enter iniciar/parar tiempo
    # retornar el tiempo final

def start_translator(lang):
    """(str) -> str

    Recibe un argumento que define que idioma utilizar para traducir un text input y
    retorna el text traducido al español

    ### start_translator("English")
    "Hello"
    "Hola"
    """
    str = input("Insert your text to translator: ")
    return print(asyncio.run(translator.translator_text(lang, str)))

def start_tictactoe(num_games):
    tik_tak_toe.play_game(num_games)

if __name__ == '__main__':
    main()
