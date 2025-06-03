from translations.translations import get_translations as translations

class TicTacToe:
    def __init__(self, t):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.t = t

    def print_board(self):
        print(" ")
        for row in self.board:
            print("|".join(row))
            print("-" * 5)

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != " ":
                return row[0]
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]
        return None

    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            return True
        else:
            print(self.t["cell_taken"])
            return False

class GameManager:
    def __init__(self, t, num_games=1):
        self.num_games = num_games
        self.won_games = {"X": 0, "O": 0}
        self.t = t

    def play(self):
        while self.won_games["X"] < (self.num_games // 2) + 1 and self.won_games["O"] < (self.num_games // 2) + 1:
            game = TicTacToe(self.t)
            while True:
                game.print_board()
                print(f"{self.t['best_of']} {self.num_games} {self.t['games']}")
                try:
                    row = int(input(f"{self.t['player']} {game.current_player}, {self.t['enter_row']} (0-2): "))
                    col = int(input(f"{self.t['player']} {game.current_player}, {self.t['enter_col']} (0-2): "))
                except ValueError:
                    print(self.t["valid_numbers"])
                    continue

                if 0 <= row <= 2 and 0 <= col <= 2:
                    if game.make_move(row, col):
                        winner = game.check_winner()
                        if winner:
                            game.print_board()
                            print(f"{self.t['player']} {winner} {self.t['wins_game']}")
                            self.won_games[winner] += 1
                            break
                        if game.is_board_full():
                            game.print_board()
                            print(self.t["draw"])
                            break
                        game.switch_player()
                else:
                    print(self.t["valid_numbers"])

        overall_winner = "X" if self.won_games["X"] > self.won_games["O"] else "O"
        print(f"{self.t['player']} {overall_winner} {self.t['wins_best_of']} {self.num_games} {self.t['games']}!")

def obtener_traducciones_tictactoe(lang):
    t = translations.get(lang, translations["en"])["tictactoe"]
    # Textos adicionales para mensajes
    t.setdefault("player", t.get("player1", "Player"))
    t.setdefault("enter_row", "enter the row")
    t.setdefault("enter_col", "enter the column")
    t.setdefault("valid_numbers", "Please enter valid numbers between 0 and 2.")
    t.setdefault("cell_taken", "Cell already taken, try again.")
    t.setdefault("wins_game", "wins this game!")
    t.setdefault("draw", "It's a draw!")
    t.setdefault("best_of", "Best of:")
    t.setdefault("games", "games")
    t.setdefault("wins_best_of", "wins best of")
    return t

def main(lang):
    t = obtener_traducciones_tictactoe(lang)
    try:
        num_games = int(input(f"{t['best_of']} N: "))
    except ValueError:
        num_games = 1
    manager = GameManager(t, num_games)
    manager.play()

if __name__ == "__main__":
    main()
