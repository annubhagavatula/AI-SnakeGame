import sys
import pygame
import random
import time

# Initialize pygame
pygame.init()

# Grid size and screen dimensions
size = 20
width = 25
height = 25
s_width = size * width
s_height = size * height
speed = 3

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # Snake 1
blue = (0, 0, 255)  # Snake 2
red = (255, 0, 0)  # Food for Snake 1
pink = (255, 20, 147)  # Food for Snake 2

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game window
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Two-Player Snake Game")
clock = pygame.time.Clock()

# Obstacles
num_obstacles = 30
obstacles = set()
while len(obstacles) < num_obstacles:
    pos = (random.randint(0, width - 1), random.randint(0, height - 1))
    if pos not in obstacles:
        obstacles.add(pos)

# Ensure positions do not overlap obstacles
def valid_position(existing_positions, min_distance=3):
    while True:
        pos = (random.randint(0, width - 1), random.randint(0, height - 1))
        if pos not in existing_positions:
            nearby = [
                (pos[0] + dx, pos[1] + dy)
                for dx in range(-min_distance, min_distance + 1)
                for dy in range(-min_distance, min_distance + 1)
            ]
            if not any(p in obstacles for p in nearby):
                return pos

# Initialize snakes, food, and score
green_snake = [valid_position(obstacles)]
blue_snake = [valid_position(set(green_snake).union(obstacles))]
green_food = valid_position(set(green_snake).union(blue_snake).union(obstacles))
blue_food = valid_position(set(green_snake).union(blue_snake).union(obstacles, {green_food}))
green_direction = RIGHT
blue_direction = LEFT
green_score = 0
blue_score = 0
game_time = 300  # 5 minutes
start_time = time.time()

# Function to draw grid
def grid():
    for x in range(0, s_width, size):
        pygame.draw.line(screen, white, (x, 0), (x, s_height))
    for y in range(0, s_height, size):
        pygame.draw.line(screen, white, (0, y), (s_width, y))

# Draw snakes, food, and obstacles
def draw_snake(snake, color):
    for segment in snake:
        pygame.draw.rect(screen, color, (segment[0] * size, segment[1] * size, size, size))

def draw_food(food, color):
    pygame.draw.rect(screen, color, (food[0] * size, food[1] * size, size, size))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, white, (obstacle[0] * size, obstacle[1] * size, size, size))

# Snake movement
def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    return [head] + snake[:-1]

def grow_snake(snake):
    return snake + [snake[-1]]

def hit_wall_or_self(pos, snake, obstacles):
    x, y = pos
    return x < 0 or y < 0 or x >= width or y >= height or pos in snake[1:] or pos in obstacles

# Function for Blue Snake AI movement
def blue_snake_ai(snake, food, obstacles, other_snake):
    head = snake[0]
    directions = [UP, DOWN, LEFT, RIGHT]
    random.shuffle(directions)  # Randomize directions to add unpredictability

    # Move towards the food if possible
    best_direction = None
    min_distance = float('inf')
    for direction in directions:
        new_pos = (head[0] + direction[0], head[1] + direction[1])
        if new_pos not in snake and new_pos not in obstacles and new_pos not in other_snake:
            distance = abs(new_pos[0] - food[0]) + abs(new_pos[1] - food[1])
            if distance < min_distance:
                min_distance = distance
                best_direction = direction

    return best_direction or random.choice(directions)

# Main game loop
try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and green_direction != DOWN:
                    green_direction = UP
                elif event.key == pygame.K_DOWN and green_direction != UP:
                    green_direction = DOWN
                elif event.key == pygame.K_LEFT and green_direction != RIGHT:
                    green_direction = LEFT
                elif event.key == pygame.K_RIGHT and green_direction != LEFT:
                    green_direction = RIGHT

        # Update Blue Snake direction with AI
        new_direction = blue_snake_ai(blue_snake, blue_food, obstacles, green_snake)
        if new_direction:
            blue_direction = new_direction

        # Move snakes
        green_snake = move_snake(green_snake, green_direction)
        blue_snake = move_snake(blue_snake, blue_direction)

        # Check for collisions
        if hit_wall_or_self(green_snake[0], green_snake, obstacles) or green_snake[0] in blue_snake:
            print("Player 2 (Blue Snake) wins!")
            running = False
        if hit_wall_or_self(blue_snake[0], blue_snake, obstacles) or blue_snake[0] in green_snake:
            print("Player 1 (Green Snake) wins!")
            running = False

        # Check food consumption
        if green_snake[0] == green_food:
            green_score += 1
            green_snake = grow_snake(green_snake)
            green_food = valid_position(set(green_snake).union(blue_snake, obstacles, {blue_food}))
        if blue_snake[0] == blue_food:
            blue_score += 1
            blue_snake = grow_snake(blue_snake)
            blue_food = valid_position(set(blue_snake).union(green_snake, obstacles, {green_food}))

        # Timer
        if time.time() - start_time > game_time:
            if green_score > blue_score:
                print("Time's up! Player 1 (Green Snake) wins!")
            elif blue_score > green_score:
                print("Time's up! Player 2 (Blue Snake) wins!")
            else:
                print("Time's up! It's a tie!")
            running = False

        # Draw everything
        screen.fill(black)
        grid()
        draw_obstacles(obstacles)
        draw_snake(green_snake, green)
        draw_snake(blue_snake, blue)
        draw_food(green_food, red)
        draw_food(blue_food, pink)
        pygame.display.flip()
        clock.tick(speed)

except Exception as e:
    print(f"An error occurred: {e}")

pygame.quit()
sys.exit()
