import tkinter as tk
from tkinter import messagebox
import time
import random
import pygame
import os
import customtkinter

# Initialize the mixer module for pygame
pygame.mixer.init()
from PIL import Image,ImageTk
class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.songs = os.listdir(music_dir)
        self.current_song = 0
        self.is_playing = False

    def play_next_song(self):
        if self.songs:
            self.current_song = (self.current_song + 1) % len(self.songs)
            pygame.mixer.music.load(os.path.join(self.music_dir, self.songs[self.current_song]))
            pygame.mixer.music.play()
            self.is_playing = True

    def play_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                self.play_next_song()
            self.is_playing = True

class TicTacToe:
    def __init__(self):
        self.root = tk.Toplevel()  # Create a new Toplevel window
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
                self.buttons[i][j].grid(row=i, column=j)  # Use grid geometry manager for buttons
                
                
    def on_click(self, i, j):
        if self.board[i][j] == "":
            self.buttons[i][j].config(text=self.current_player)
            self.board[i][j] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                self.close_window()  # Close window after a player wins
            elif self.check_draw():
                messagebox.showinfo("Draw", "The game is a draw!")
                self.close_window()  # Close window if it's a draw
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
                
    def close_window(self):
        self.root.destroy()  # Destroy the window when the game ends

class SnakeGame:
    def __init__(self):
        # self.root = root
        # self.root.title("Snake Game")
        self.start_snake_game()

    def start_snake_game(self):
        WIDTH = 500
        HEIGHT = 500
        SPEED = 200
        SPACE_SIZE = 20
        BODY_SIZE = 2
        SNAKE = "#E0115F"
        FOOD = "#FF0000"
        BACKGROUND = "#000000"

        class Snake: 

            def __init__(self): 
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

            def __init__(self): 

                x = random.randint(0, 
                        (WIDTH / SPACE_SIZE)-1) * (SPACE_SIZE) 
                y = random.randint(0, 
                        (HEIGHT / SPACE_SIZE) - 1) * (SPACE_SIZE)

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

class TodoList:
    def __init__(self):
        # self.root = root
        # self.root.title("To-Do List")
        self.tasks_list = []
        self.counter = 1
        self.TextArea = None
        self.enterTaskField = None
        self.taskNumberField = None
        self.openToDoListWindow()

    def inputError(self):
        if self.enterTaskField.get() == "":
            messagebox.showerror("Input Error", "Task field cannot be empty")
            return False
        return True

    def clear_taskField(self):
        self.enterTaskField.delete(0, tk.END)

    def clear_taskNumberField(self):
        self.taskNumberField.delete(0, tk.END)

    def insertTask(self):
        if self.inputError():
            content = self.enterTaskField.get() + "\n"
            self.tasks_list.append(content)
            self.TextArea.insert(tk.END, "[ " + str(self.counter) + " ] " + content)
            self.counter += 1
            self.clear_taskField()

    def delete(self):
        if len(self.tasks_list) == 0:
            messagebox.showerror("No Task", "No task to delete")
            return
        number = self.taskNumberField.get()
        if number == "":
            messagebox.showerror("Input Error", "Please enter task number")
            return
        else:
            task_no = int(number)
        self.clear_taskNumberField()
        if task_no <= 0 or task_no > len(self.tasks_list):
            messagebox.showerror("Invalid Task Number", "Task number does not exist")
            return
        self.tasks_list.pop(task_no - 1)
        self.counter -= 1
        self.TextArea.delete(1.0, tk.END)
        for i in range(len(self.tasks_list)):
            self.TextArea.insert(tk.END, "[ " + str(i + 1) + " ] " + self.tasks_list[i])

    def openToDoListWindow(self):
        self.todo_window = tk.Tk()
        self.todo_window.title("To-Do List")
        self.todo_window.geometry("250x300")

        enterTask = tk.Label(self.todo_window, text="Enter Your Task", bg="light green")
        self.enterTaskField = tk.Entry(self.todo_window)
        Submit = tk.Button(self.todo_window, text="Submit", fg="Black", bg="Red", command=self.insertTask)
        self.TextArea = tk.Text(self.todo_window, height=5, width=25, font="lucida 13")
        taskNumber = tk.Label(self.todo_window, text="Delete Task Number", bg="blue")
        self.taskNumberField = tk.Entry(self.todo_window)
        deleteButton = tk.Button(self.todo_window, text="Delete", fg="Black", bg="Red", command=self.delete)
        exitButton = tk.Button(self.todo_window, text="Exit", fg="Black", bg="Red", command=self.todo_window.destroy)

        enterTask.grid(row=0, column=2)
        self.enterTaskField.grid(row=1, column=2, ipadx=50)
        Submit.grid(row=2, column=2)
        self.TextArea.grid(row=3, column=2, padx=10, sticky=tk.W)
        taskNumber.grid(row=4, column=2, pady=5)
        self.taskNumberField.grid(row=5, column=2)
        deleteButton.grid(row=6, column=2, pady=5)
        exitButton.grid(row=7, column=2)

        for task in self.tasks_list:
            self.TextArea.insert(tk.END, task)

def open_game(game_class):
    # game_root = tk.Toplevel()
    game = game_class()
    # game_root.mainloop()

def start_meditation():
    global meditation_start_time, meditation_time
    meditation_time = int(meditation_time_entry.get()) * 60
    meditation_label.config(text=f"Time: {meditation_time//60}:{meditation_time%60:02d}")
    meditation_start_time = time.time()
    update_timer()

def update_timer():
    current_time = time.time()
    elapsed_time = current_time - meditation_start_time
    if elapsed_time >= meditation_time:
        meditation_label.config(text="Chlo bhot rest ho gya!")
    else:
        meditation_label.config(text=f"Time Remaining: {int((meditation_time - elapsed_time) // 60)}:{int((meditation_time - elapsed_time) % 60):02d}")
        meditation_window.after(1000, update_timer)

def helloCallBack():
    global meditation_window
    meditation_window = tk.Toplevel()
    meditation_window.title("Timer")
    meditation_window.geometry("200x200")
    meditation_window.config(bg="#922B21")
    meditation_window.resizable(width=False, height=False)

    global meditation_label, meditation_time_entry
    meditation_label = tk.Label(meditation_window, text="", font=("Helvetica", 20), fg="white", bg="#922B21")
    meditation_label.place(x=50, y=50)

    meditation_time_entry = tk.Entry(meditation_window, bg="#48C9B0", width=10, font=(20))
    meditation_time_entry.place(x=50, y=100)

    start_button = tk.Button(meditation_window, text="Start Rest", fg="Black", bg="#D4AC0D", width=15, command=start_meditation, font=(20))
    start_button.place(x=30, y=150)

    meditation_window.mainloop()
    

if __name__ == "__main__":
    
    root = customtkinter.CTk(fg_color="#000000")
    root.title("")
    root.geometry("140x170")



    player = MusicPlayer("LazyDays")

    # Function to open Tic Tac Toe game
    def open_tic_tac_toe():
        TicTacToe()

    # Function to open Snake Game
    def open_snake_game():
        open_game(SnakeGame)

    # Function to open To-Do List
    def open_todo_list():
        open_game(TodoList)

    # Load your logo image (replace 'logo.png' with your image path)
    logo_image = Image.open("clock.jpg")
    logo_ctk_image = customtkinter.CTkImage(logo_image, size=(30, 30))  # Specify the desired size

    # Create a frame to hold button1 and button2
    button_frame = tk.Frame(root,background="#000000")
    button_frame.pack(side=tk.TOP, padx=5, pady=5)

    # Create button1
    button1 = customtkinter.CTkButton(button_frame, hover_color="#ED849D", text="",
                                    width=30, height=35, fg_color="#E0115F",
                                    border_width=2, corner_radius=8,
                                    border_color=("#444444", "#222222"),
                                    text_color=("#FFFFFF", "#000000"),
                                    image=logo_ctk_image, compound="left",command=helloCallBack)  # Place logo on the left
    button1.pack(side=tk.LEFT,padx=5,pady=5)

    # Load your logo image for button2 (replace 'todo.jpg' with your image path)
    logo_image2 = Image.open("todo.jpg")
    logo_todo_image = customtkinter.CTkImage(logo_image2, size=(30, 30))  # Specify the desired size

    # Create button2
    button2 = customtkinter.CTkButton(button_frame, hover_color="#ED849D", text="",
                                    width=30, height=35, fg_color="#E0115F",
                                    border_width=2, corner_radius=8,
                                    border_color=("#444444", "#222222"),
                                    text_color=("#FFFFFF", "#000000"),
                                    image=logo_todo_image, compound="left",command=open_todo_list)  # Place logo on the left
    button2.pack(side=tk.LEFT, padx=5,pady=5)

    button_frame1 = tk.Frame(root,background="#000000")
    button_frame1.pack(side=tk.TOP, padx=5, pady=5)

    # Load your logo image for button3 (replace 'todo.jpg' with your image path)
    logo_image3 = Image.open("music.png")
    logo_lofi_image = customtkinter.CTkImage(logo_image3, size=(30, 30))  # Specify the desired size

    # Create button3
    button3 = customtkinter.CTkButton(button_frame1, hover_color="#ED849D", text="",
                                    width=30, height=35, fg_color="#E0115F",
                                    border_width=2, corner_radius=8,
                                    border_color=("#444444", "#222222"),
                                    text_color=("#FFFFFF", "#000000"),
                                    image=logo_lofi_image, compound="left",command=player.play_pause)  # Place logo on the left
    button3.pack(side=tk.LEFT, padx=5, pady=5)

    # Load your logo image for button3 (replace 'todo.jpg' with your image path)
    logo_image4 = Image.open("tic.jpg")
    logo_ttt_image = customtkinter.CTkImage(logo_image4, size=(30, 30))  # Specify the desired size

    button4 = customtkinter.CTkButton(button_frame1, hover_color="#ED849D", text="",
                                    width=30, height=35, fg_color="#E0115F",
                                    border_width=2, corner_radius=8,
                                    border_color=("#444444", "#222222"),
                                    text_color=("#FFFFFF", "#000000"),
                                    image=logo_ttt_image, compound="left",command=open_tic_tac_toe)  # Place logo on the left
    button4.pack(side=tk.LEFT, padx=5, pady=5)


    button_frame2 = tk.Frame(root,background="#000000")
    button_frame2.pack(side=tk.TOP, padx=5, pady=5)
    # Load your logo image for button3 (replace 'todo.jpg' with your image path)
    logo_image5 = Image.open("snake.jpg")
    logo_snake_image = customtkinter.CTkImage(logo_image5, size=(30, 30))  # Specify the desired size

    button5 = customtkinter.CTkButton(button_frame2, hover_color="#ED849D", text="",
                                    width=30, height=35, fg_color="#E0115F",
                                    border_width=2, corner_radius=8,
                                    border_color=("#444444", "#222222"),
                                    text_color=("#FFFFFF", "#000000"),
                                    image=logo_snake_image, compound="left",command=open_snake_game)  # Place logo on the left
    button5.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()