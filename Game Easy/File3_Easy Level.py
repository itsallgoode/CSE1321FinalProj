#Easy Setting

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Colors and constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 4  # Uniform speed for all obstacles
NUM_LANES = 4  # Reduced to 4 to keep the bottom of the screen clear
LANE_HEIGHT = (height - PLAYER_SIZE) // NUM_LANES

# Player setup
player = pygame.Rect(width // 2, height - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)

# Obstacle setup
obstacles = []

def add_obstacle():
    lane = random.randint(0, NUM_LANES - 1)
    y_position = lane * LANE_HEIGHT + (LANE_HEIGHT - OBSTACLE_HEIGHT) // 2
    new_obstacle = pygame.Rect(width, y_position, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    obstacles.append(new_obstacle)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < height:
        player.y += 5

    # Add new obstacle randomly, with varying spawn rate
    if random.randint(0, 100) > 95:  # Adjust spawn rate probability here
        add_obstacle()

    # Update obstacle positions
    for i in range(len(obstacles) - 1, -1, -1):
        obstacles[i].x -= OBSTACLE_SPEED
        if obstacles[i].right < 0:
            obstacles.pop(i)

    # Check for collisions
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            print("Collision detected!")
            running = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)  # Draw obstacles as blue rectangles

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

