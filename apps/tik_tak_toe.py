
def create_board():
    """Create a 3x3 Tic Tac Toe board."""
    return [[" " for _ in range(3)] for _ in range(3)]
def print_board(board):
    """Print the Tic Tac Toe board."""
    print(" ")
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board):
    """Check if there is a winner."""
    # Check rows, columns, and diagonals
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None
def is_board_full(board):
    """Check if the board is full."""
    return all(cell != " " for row in board for cell in row)
def play_game(num_games= 1):
  won_games ={
    "X": 0,
    "O": 0,
  }
  while won_games["X"] < (num_games // 2) + 1 and won_games["O"] < (num_games // 2) + 1:
      board = create_board()
      current_player = "X"
      while True:
          print_board(board)
          print(f"Best of: {num_games} games")
          row = int(input(f"Player {current_player}, enter the row (0-2): "))
          col = int(input(f"Player {current_player}, enter the column (0-2): "))

          if board[row][col] == " ":
              board[row][col] = current_player
              winner = check_winner(board)
              if winner:
                  print_board(board)
                  print(f"Player {winner} wins best of {num_games}!")
                  won_games[winner] += 1
                  break
              if is_board_full(board):
                  print_board(board)
                  print("It's a draw!")
                  break
              current_player = "O" if current_player == "X" else "X"
          else:
              print("Cell already taken, try again.")
if __name__ == "__main__":
    play_game()
