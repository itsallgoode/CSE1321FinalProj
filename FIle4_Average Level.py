import pygame
import random
import sys


pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))


white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (200, 200, 200)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)

player_size = 50
obstacle_width = 120
obstacle_height = 80
obstacle_speed = 10
safe_area_height = 100
middle_height = height - 2 * safe_area_height
lanes = 8
lane_height = middle_height // lanes


top_safe_area = pygame.Rect(0, 0, width, safe_area_height)
bottom_safe_area = pygame.Rect(0, height - safe_area_height, width, safe_area_height)
middle_area = pygame.Rect(0, safe_area_height, width, middle_height)

obstacles = []
# randomly selects a lane and calculates the position for a new obstacle
def add_obstacle():
    lane = random.randint(0, lanes - 1)
    y_position = safe_area_height + lane * lane_height + (lane_height - obstacle_height) // 2
    new_obstacle = pygame.Rect(width, y_position, obstacle_width, obstacle_height)

    # keeps the obstacles from overlapping
    overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles)
    if not overlap:
        obstacles.append(new_obstacle)

player_start_x = width // 2 - player_size // 2
player_start_y = height - safe_area_height + (safe_area_height - player_size) // 2
player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.left > 0:
                player.x -= 50
            elif event.key == pygame.K_RIGHT and player.right < width:
                player.x += 50
            elif event.key == pygame.K_UP and player.top > 0:
                player.y -= 50
            elif event.key == pygame.K_DOWN and player.bottom < height:
                player.y += 50


    if random.randint(0, 100) > 96: # lower number to increase the chance of adding an obstacle
        add_obstacle()

    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
        if obstacle.right < 0:
            obstacles.remove(obstacle)

    if any(player.colliderect(obstacle) for obstacle in obstacles):
        screen.fill(white)  # "Enter game_over surface"
        # "Play sound"  channel.play(dead sound) - referencing variable(dead_sound)
        text = font.render("Game Over", True, (black))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False # kills the game if you hit an obstacle

    screen.fill(white)
    pygame.draw.rect(screen, gray, top_safe_area)
    pygame.draw.rect(screen, gray, bottom_safe_area)
    pygame.draw.rect(screen, green, middle_area)  #
    pygame.draw.rect(screen, red, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, blue, obstacle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
