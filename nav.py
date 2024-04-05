import tkinter as tk
from tkinter import messagebox
import random
class TicTacToe:
    def _init_(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=('Helvetica', 20), width=5, height=2,
                                                command=lambda i=i, j=j: self.on_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, i, j):
        if self.board[i][j] == "":
            self.buttons[i][j].config(text=self.current_player)
            self.board[i][j] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Draw", "The game is a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True

    def reset_board(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")

class SnakeGame:
    def _init_(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.start_snake_game()

    def start_snake_game(self):
        WIDTH = 500
        HEIGHT = 500
        SPEED = 200
        SPACE_SIZE = 20
        BODY_SIZE = 2
        SNAKE = "#00FF00"
        FOOD = "#FFFFFF"
        BACKGROUND = "#000000"

        class Snake: 

            def _init_(self): 
                self.body_size = BODY_SIZE 
                self.coordinates = [] 
                self.squares = [] 

                for i in range(0, BODY_SIZE): 
                    self.coordinates.append([0, 0]) 

                for x, y in self.coordinates: 
                    square = canvas.create_rectangle( 
                        x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                            fill=SNAKE, tag="snake") 
                    self.squares.append(square) 

        class Food: 

            def _init_(self): 

                x = random.randint(0, 
                        (WIDTH / SPACE_SIZE)-1) * SPACE_SIZE 
                y = random.randint(0, 
                        (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE 

                self.coordinates = [x, y] 

                canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD, tag="food") 

        def next_turn(snake, food): 

            x, y = snake.coordinates[0] 

            if direction == "up": 
                y -= SPACE_SIZE 
            elif direction == "down": 
                y += SPACE_SIZE 
            elif direction == "left": 
                x -= SPACE_SIZE 
            elif direction == "right": 
                x += SPACE_SIZE 

            snake.coordinates.insert(0, (x, y)) 

            square = canvas.create_rectangle( 
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE) 

            snake.squares.insert(0, square) 

            if x == food.coordinates[0] and y == food.coordinates[1]: 

                global score 

                score += 1

                label.config(text="Points:{}".format(score)) 

                canvas.delete("food") 

                food = Food() 

            else: 

                del snake.coordinates[-1] 

                canvas.delete(snake.squares[-1]) 

                del snake.squares[-1] 

            if check_collisions(snake): 
                game_over() 

            else: 
                window.after(SPEED, next_turn, snake, food) 

        def change_direction(new_direction): 

            global direction 

            if new_direction == 'left': 
                if direction != 'right': 
                    direction = new_direction 
            elif new_direction == 'right': 
                 if direction != 'left': 
                    direction = new_direction 
            elif new_direction == 'up': 
                if direction != 'down': 
                    direction = new_direction 
            elif new_direction == 'down': 
                if direction != 'up': 
                    direction = new_direction 

        def check_collisions(snake): 

            x, y = snake.coordinates[0] 

            if x < 0 or x >= WIDTH: 
                return True
            elif y < 0 or y >= HEIGHT: 
                return True

            for body_part in snake.coordinates[1:]: 
                if x == body_part[0] and y == body_part[1]: 
                    return True

            return False

        def game_over(): 

            canvas.delete(tk.ALL) 
            canvas.create_text(canvas.winfo_width()/2, 
                            canvas.winfo_height()/2, 
                            font=('consolas', 70), 
                            text="GAME OVER", fill="red", 
                            tag="gameover") 

        global window, canvas, score, direction

        window = tk.Tk() 
        window.title("Snake game ") 

        score = 0
        direction = 'down'

        label = tk.Label(window, text="Points:{}".format(score), 
                        font=('consolas', 20)) 
        label.pack() 

        canvas = tk.Canvas(window, bg=BACKGROUND, 
                        height=HEIGHT, width=WIDTH) 
        canvas.pack() 

        window.update() 

        window_width = window.winfo_width() 
        window_height = window.winfo_height() 
        screen_width = window.winfo_screenwidth() 
        screen_height = window.winfo_screenheight() 

        x = int((screen_width/2) - (window_width/2)) 
        y = int((screen_height/2) - (window_height/2)) 

        window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

        window.bind('<Left>', 
                    lambda event: change_direction('left')) 
        window.bind('<Right>', 
                    lambda event: change_direction('right')) 
        window.bind('<Up>', 
                    lambda event: change_direction('up')) 
        window.bind('<Down>', 
                    lambda event: change_direction('down')) 

        snake = Snake() 
        food = Food() 

        next_turn(snake, food) 

        window.mainloop() 
def open_game(game_class):
    game_root = tk.Tk()
    game = game_class(game_root)
    game_root.mainloop()

root = tk.Tk()
root.geometry("500x60")
root.title("Navigation Bar")

open_tic_tac_toe = lambda: open_game(TicTacToe)
open_snake_game = lambda: open_game(SnakeGame)

button_tic_tac_toe = tk.Button(root, text="Tic Tac Toe", command=open_tic_tac_toe)
button_tic_tac_toe.pack(side=tk.LEFT, padx=5)

button_snake_game = tk.Button(root, text="Snake Game", command=open_snake_game)
button_snake_game.pack(side=tk.LEFT, padx=5)

root.mainloop()