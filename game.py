import tkinter as tk
import numpy as np
import random

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.geometry("400x500")
        
        # Initialize the score and tiles array
        self.score = 0
        self.tiles = []
        
        # Create UI elements
        self.create_ui()
        self.start_game()
        
        # Bind keys for movement
        self.window.bind("<Up>", lambda event: self.move("up"))
        self.window.bind("<Down>", lambda event: self.move("down"))
        self.window.bind("<Left>", lambda event: self.move("left"))
        self.window.bind("<Right>", lambda event: self.move("right"))

    def create_ui(self):
        # Display the score
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)
        
        # Create the 4x4 grid of tiles
        for i in range(4):
            row = []
            for j in range(4):
                tile = tk.Label(self.window, text="", font=("Helvetica", 24), width=4, height=2, bg="lightgrey", relief="groove")
                tile.grid(row=i+1, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def start_game(self):
        # Create a 4x4 matrix to represent the game board
        self.board = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        # Update each tile's display according to the board state
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                tile = self.tiles[i][j]
                tile.config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))
        
        # Update score label
        self.score_label.config(text=f"Score: {self.score}")

    def get_tile_color(self, value):
        # Colors for different tile values
        colors = {
            0: "lightgrey", 2: "lightyellow", 4: "lightgoldenrod", 8: "orange", 16: "darkorange",
            32: "coral", 64: "tomato", 128: "salmon", 256: "pink", 512: "violet",
            1024: "orchid", 2048: "purple"
        }
        return colors.get(value, "black")

    def move(self, direction):
        # Perform the move action in the specified direction
        original_board = self.board.copy()
        
        if direction == "up":
            self.board = np.rot90(self.board, -1)
            self.move_left()
            self.board = np.rot90(self.board)
        elif direction == "down":
            self.board = np.rot90(self.board)
            self.move_left()
            self.board = np.rot90(self.board, -1)
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.board = np.fliplr(self.board)
            self.move_left()
            self.board = np.fliplr(self.board)

        if not np.array_equal(original_board, self.board):
            self.add_new_tile()
            self.update_ui()
            if self.is_game_over():
                self.show_game_over()

    def move_left(self):
        # Move and combine tiles to the left
        for i in range(4):
            non_zero = self.board[i][self.board[i] != 0]
            new_row = []
            skip = False
            for j in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(non_zero) and non_zero[j] == non_zero[j + 1]:
                    new_row.append(2 * non_zero[j])
                    self.score += 2 * non_zero[j]
                    skip = True
                else:
                    new_row.append(non_zero[j])
            new_row.extend([0] * (4 - len(new_row)))
            self.board[i] = new_row

    def is_game_over(self):
        # Check if there are no moves left
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if i < 3 and self.board[i][j] == self.board[i+1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j+1]:
                    return False
        return True

    def show_game_over(self):
        game_over_window = tk.Toplevel(self.window)
        game_over_window.title("Game Over")
        game_over_window.geometry("200x100")
        
        tk.Label(game_over_window, text="Game Over", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(game_over_window, text="Play Again", command=lambda: [game_over_window.destroy(), self.start_game()]).pack()
        tk.Button(game_over_window, text="Exit", command=self.window.quit).pack()

# Run the game
if __name__ == "__main__":
    game = Game2048()
    game.window.mainloop()
