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

player_size = 40
obstacle_width = 110
obstacle_height = 60
obstacle_speed = 8
safe_area_height = 100
middle_height = height - 2 * safe_area_height
lanes = 3
lane_height = obstacle_height + 25
cars = 95 #(0-100)lower number to increase the chance of adding an obstacle

#music
background_music = pygame.mixer.Sound('File 4 music.mp3')
channel = pygame.mixer.Channel(0)

#images
game_image = pygame.image.load('interstate.png').convert_alpha()
game_image = pygame.transform.scale(game_image, (width, height))
green_car = pygame.image.load('green_car.png').convert_alpha()
green_car = pygame.transform.scale(green_car, (100, obstacle_height))
orange_car = pygame.image.load('orange_car.png').convert_alpha()
orange_car = pygame.transform.scale(orange_car, (100, obstacle_height))

vehicles = [green_car, orange_car]
vehicles_swap = [
    pygame.transform.flip(green_car, True, False),
    pygame.transform.flip(orange_car, True, False)
]
obstacle_images = []
obstacles_right = []
obstacles_left = []

top_safe_area = pygame.Rect(0, 0, width, safe_area_height)
bottom_safe_area = pygame.Rect(0, height - safe_area_height, width, safe_area_height)
middle_area = pygame.Rect(0, safe_area_height, width, middle_height)


# randomly selects a lane and calculates the position for a new obstacle
def add_obstacle():
    lane = random.randint(0, lanes - 1)
    y_position_one = (safe_area_height + lane * lane_height + lane_height) + 10
    new_obstacle = pygame.Rect(width, y_position_one, obstacle_width, obstacle_height)

    y_position_two = ((middle_height / 2 + 80) + lane * lane_height + lane_height) + 10
    new_obstacle_two = pygame.Rect(0 - obstacle_width, y_position_two, obstacle_width, obstacle_height)

    # keeps the obstacles from overlapping
    overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles_left) or any(new_obstacle_two.colliderect(obstacle) for obstacle in obstacles_right)
    if not overlap:
        obstacles_left.append(new_obstacle)
        obstacle_images.append(random.choice(vehicles))
        obstacles_right.append(new_obstacle_two)
        obstacle_images.append(random.choice(vehicles_swap))

player_start_x = width // 2 - player_size // 2
player_start_y = height - safe_area_height + (safe_area_height - player_size) // 2
player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)


running = True
clock = pygame.time.Clock()
channel.play(background_music)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.left > 0:
                player.x -= player_size
            elif event.key == pygame.K_RIGHT and player.right < width:
                player.x += player_size
            elif event.key == pygame.K_UP and player.top > 0:
                player.y -= player_size
            elif event.key == pygame.K_DOWN and player.bottom < height:
                player.y += player_size
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    if player.colliderect(top_safe_area):
        screen.fill(white)  # "Enter game_over surface"
        # "Play sound"  channel.play(dead sound) - referencing variable(dead_sound)
        text = font.render("You Win!", True, (black))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False


    if random.randint(0, 100) > cars:
        add_obstacle()

    for obstacle, image in zip(obstacles_left, obstacle_images[:len(obstacles_left)]):
        obstacle.x -= obstacle_speed
        if obstacle.right < 0:
            obstacles_left.remove(obstacle)
            obstacle_images.pop(0)

    for obstacle, image in zip(obstacles_right, obstacle_images[:len(obstacles_right)]):
        obstacle.x += obstacle_speed
        if obstacle.right > 1000 + obstacle_width:
            obstacles_right.remove(obstacle)
            obstacle_images.pop(len(obstacles_right))

    if any(player.colliderect(obstacle) for obstacle in obstacles_left) or any(player.colliderect(obstacle) for obstacle in obstacles_right):
        screen.fill(black)
        # "Play sound"  channel.play(dead sound) - referencing variable(dead_sound)
        text = font.render("Game Over", True, (white))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    screen.blit(game_image, (0, 0))
    pygame.draw.rect(screen, red, player)
    #screen.blit(image, player)

#when obstacles are created for screen
    for obstacle, image in zip(obstacles_left, obstacle_images):
        screen.blit(image, obstacle)
    for obstacle, image in zip(obstacles_right, obstacle_images):
        screen.blit(image, obstacle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
