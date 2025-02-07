import tkinter as tk
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 10

class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake
        self.food_item = None
        self.spawn_food()

    def spawn_food(self):
        """Spawns food at a random location, ensuring it doesn't overlap with the snake."""
        while True:
            self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (self.x, self.y) not in self.snake.body:
                break

        if self.food_item:
            self.canvas.delete(self.food_item)
        self.food_item = self.canvas.create_rectangle(self.x, self.y, self.x + CELL_SIZE, self.y + CELL_SIZE, fill="red")

class Snake:
    def __init__(self, canvas, speed, hard_mode):
        self.canvas = canvas
        self.body = [(50, 50)]
        self.direction = "Right"
        self.snake_parts = []
        self.speed = speed
        self.hard_mode = hard_mode  # If True, disable closing window
        self.create_snake()
        self.food = Food(canvas, self)

    def create_snake(self):
        """Creates the snake's body parts."""
        for x, y in self.body:
            part = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green", tags="snake")
            self.snake_parts.append(part)

    def move(self):
        """Moves the snake in the current direction and applies wrap-around logic."""
        x, y = self.body[0]

        if self.direction == "Up":
            y -= CELL_SIZE
        elif self.direction == "Down":
            y += CELL_SIZE
        elif self.direction == "Left":
            x -= CELL_SIZE
        elif self.direction == "Right":
            x += CELL_SIZE

        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT

        new_head = (x, y)
        self.body.insert(0, new_head)

        if self.check_food_collision():
            self.food.spawn_food()
        else:
            self.body.pop()  # Remove tail if food is not eaten

        if not self.check_self_collision():
            self.update_snake_graphics()
            self.canvas.after(self.speed, self.move)
        else:
            self.game_over()

    def update_snake_graphics(self):
        """Efficiently updates the snake's graphics without full redraw."""
        for i, (x, y) in enumerate(self.body):
            if i < len(self.snake_parts):
                self.canvas.coords(self.snake_parts[i], x, y, x + CELL_SIZE, y + CELL_SIZE)
            else:
                part = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green", tags="snake")
                self.snake_parts.append(part)

        while len(self.snake_parts) > len(self.body):
            self.canvas.delete(self.snake_parts.pop())

    def check_self_collision(self):
        """Checks if the snake collides with itself."""
        return self.body[0] in self.body[1:]

    def check_food_collision(self):
        """Checks if the snake's head collides with food."""
        return self.body[0] == (self.food.x, self.food.y)

    def game_over(self):
        """Displays Game Over text."""
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text="Game Over", fill="red", font=("Arial", 20))

    def change_direction(self, event):
        """Updates the snake's movement direction."""
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

# --- Menu to Select Difficulty ---
def start_game(difficulty):
    """Starts the game with the chosen difficulty."""
    menu_frame.pack_forget()  # Hide menu

    # Define speed based on difficulty
    if difficulty == "Easy":
        speed = 150  # Slow speed
        hard_mode = False
    elif difficulty == "Medium":
        speed = 100  # Faster speed
        hard_mode = False
    elif difficulty == "Hard":
        speed = 75  # Very fast speed
        hard_mode = True  # Disable window close

    # Set up game window
    canvas.pack()
    snake = Snake(canvas, speed, hard_mode)
    root.bind("<Key>", snake.change_direction)

    # Disable window closing on Hard mode
    if hard_mode:
        root.protocol("WM_DELETE_WINDOW", lambda: None)

    snake.move()

# --- Tkinter Window Setup ---
root = tk.Tk()
root.title("Snake Game")

# Menu Frame
menu_frame = tk.Frame(root)
menu_frame.pack()

tk.Label(menu_frame, text="Select Difficulty", font=("Arial", 20)).pack(pady=10)

# Difficulty Buttons
tk.Button(menu_frame, text="Easy", font=("Arial", 14), command=lambda: start_game("Easy")).pack(pady=5)
tk.Button(menu_frame, text="Medium", font=("Arial", 14), command=lambda: start_game("Medium")).pack(pady=5)
tk.Button(menu_frame, text="Hard", font=("Arial", 14), command=lambda: start_game("Hard")).pack(pady=5)

# Game Canvas (Hidden at start)
canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")

# Run the game
root.mainloop()
