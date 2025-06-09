class TicTacToeLogic:
    def __init__(self):
        self.reset_board()
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            winner = self.check_winner()
            is_full = self.is_board_full()
            if winner:
                self.scores[winner] += 1
            if not winner and not is_full:
                self.current_player = "O" if self.current_player == "X" else "X"
            return winner, is_full
        return None, None

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

    def is_board_full(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_scores(self):
        self.scores = {"X": 0, "O": 0}
    
def main(lang="en"):
    from apps.guis.tictactoe_gui import TicTacToeGUI
    gui = TicTacToeGUI(lang)
    gui.run()

if __name__ == '__main__':
    main()