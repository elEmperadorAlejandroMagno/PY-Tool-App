import tkinter as tk
from tkinter import messagebox
from translations.translations import get_translations as translations
from apps import tictactoe

class TicTacToeGUI:
    def __init__(self, lang="en"):
        self.t = translations.get(lang, translations["en"])["tictactoe"]
        self.logic = tictactoe.TicTacToeLogic()
        self.root = tk.Tk()
        self.root.title(self.t["title"])

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack(pady=10)

        self.reset_scores_button = tk.Button(self.root, text=self.t.get("reset_scores", "Reiniciar puntuaciones"), command=self.reset_scores)
        self.reset_scores_button.pack(pady=5)

        self.turn_label = tk.Label(self.root, text=self.get_turn_text(), font=("Arial", 12))
        self.turn_label.pack(pady=5)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", width=6, height=3, font=("Arial", 18),
                                command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.reset_board_button = tk.Button(self.root, text=self.t.get("reset_board", "Reiniciar tablero"), command=self.reset_board)
        self.reset_board_button.pack(pady=10)

    def get_score_text(self):
        return f"{self.t['player1']} (X): {self.logic.scores['X']}   {self.t['player2']} (O): {self.logic.scores['O']}"

    def get_turn_text(self):
        return f"{self.t['turn']}: {self.logic.current_player}"

    def on_button_click(self, row, col):
        winner, is_full = self.logic.make_move(row, col)
        self.update_board()
        self.score_label.config(text=self.get_score_text())
        self.turn_label.config(text=self.get_turn_text())
        if winner:
            messagebox.showinfo(self.t["winner"], f"{self.t['player1'] if winner == 'X' else self.t['player2']} ({winner}) {self.t['winner']}!")
            self.reset_board()
        elif is_full:
            messagebox.showinfo(self.t["draw"], self.t["draw"])
            self.reset_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.logic.board[i][j], state="disabled" if self.logic.board[i][j] else "normal")

    def reset_board(self):
        self.logic.reset_board()
        self.update_board()
        self.turn_label.config(text=self.get_turn_text())

    def reset_scores(self):
        self.logic.reset_scores()
        self.score_label.config(text=self.get_score_text())
        self.reset_board()

    def run(self):
        self.root.mainloop()
