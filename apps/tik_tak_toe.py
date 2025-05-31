class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

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
            print("Cell already taken, try again.")
            return False

class GameManager:
    def __init__(self, num_games=1):
        self.num_games = num_games
        self.won_games = {"X": 0, "O": 0}

    def play(self):
        while self.won_games["X"] < (self.num_games // 2) + 1 and self.won_games["O"] < (self.num_games // 2) + 1:
            game = TicTacToe()
            while True:
                game.print_board()
                print(f"Best of: {self.num_games} games")
                try:
                    row = int(input(f"Player {game.current_player}, enter the row (0-2): "))
                    col = int(input(f"Player {game.current_player}, enter the column (0-2): "))
                except ValueError:
                    print("Please enter valid numbers between 0 and 2.")
                    continue

                if 0 <= row <= 2 and 0 <= col <= 2:
                    if game.make_move(row, col):
                        winner = game.check_winner()
                        if winner:
                            game.print_board()
                            print(f"Player {winner} wins this game!")
                            self.won_games[winner] += 1
                            break
                        if game.is_board_full():
                            game.print_board()
                            print("It's a draw!")
                            break
                        game.switch_player()
                else:
                    print("Please enter numbers between 0 and 2.")

        overall_winner = "X" if self.won_games["X"] > self.won_games["O"] else "O"
        print(f"Player {overall_winner} wins best of {self.num_games} games!")

if __name__ == "__main__":
    try:
        num_games = int(input("Enter the number of games (best of N): "))
    except ValueError:
        num_games = 1
    manager = GameManager(num_games)
    manager.play()
