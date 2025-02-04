import tkinter as tk
import random

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 39) * 10  # Ensure alignment with snake
        self.y = random.randint(0, 39) * 10
        self.food_item = self.canvas.create_rectangle(self.x, self.y, self.x + 10, self.y + 10, fill="red", tags="food")

    def reset_position(self):
        self.canvas.delete(self.food_item)  # Only delete food, not everything
        self.x = random.randint(0, 39) * 10
        self.y = random.randint(0, 39) * 10
        self.food_item = self.canvas.create_rectangle(self.x, self.y, self.x + 10, self.y + 10, fill="red", tags="food")

class Snake:
    def __init__(self, canvas, food):
        self.canvas = canvas
        self.body = [(50, 50)]
        self.food = food
        self.direction = "Right"
        self.snake_parts = []
        self.create_snake()

    def create_snake(self):
        for x, y in self.body:
            part = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", tags="snake")
            self.snake_parts.append(part)

    def move(self):
        x, y = self.body[0]

        if self.direction == "Up":
            y -= 10
        elif self.direction == "Down":
            y += 10
        elif self.direction == "Left":
            x -= 10
        elif self.direction == "Right":
            x += 10

        new_head = (x, y)
        self.body.insert(0, new_head)

        if self.check_food_collision():
            self.food.reset_position()
        else:
            self.body.pop()

        if not self.check_collision():
            self.update_snake_graphics()
            self.canvas.after(100, self.move)
        else:
            self.game_over()

    def update_snake_graphics(self):
        for part in self.snake_parts:
            self.canvas.delete(part)
        self.snake_parts.clear()
        self.create_snake()

    def check_collision(self):
        x, y = self.body[0]

        if x < 0 or x >= 400 or y < 0 or y >= 400:
            return True

        if (x, y) in self.body[1:]:
            return True

        return False

    def check_food_collision(self):
        x, y = self.body[0]
        return x == self.food.x and y == self.food.y

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="red", font=("Arial", 20))

    def change_direction(self, event):
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

# Tkinter Setup
root = tk.Tk()
root.title("Snake Game")

canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack()

food = Food(canvas)  # ✅ Now Food is defined
snake = Snake(canvas, food)

root.bind("<Key>", snake.change_direction)
snake.move()

root.mainloop()

