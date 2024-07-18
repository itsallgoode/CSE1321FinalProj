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
player_size = 50
obstacle_width = 160
obstacle_height = 100
obstacle_speed = 6  
safe_area_height = 100  
middle_height = height - 2 * safe_area_height
lanes = 6
lane_height = middle_height // lanes

 

top_safe_area = pygame.Rect(0, 0, width, safe_area_height)
bottom_safe_area = pygame.Rect(0, height - safe_area_height, width, safe_area_height)
middle_area = pygame.Rect(0, safe_area_height, width, middle_height)


#images
full_image = pygame.image.load('images/road.jpg')
full_image = pygame.transform.scale(full_image, (width, height))
racecar_images = ['images/racecar1.png', 'images/racecar2.png']
racecar_image = [pygame.image.load(image) for image in racecar_images]
racecar_image = [pygame.transform.scale(image, (obstacle_width, obstacle_height)) for image in racecar_image]

obstacles = []
# randomly selects a lane and calculates the position for a new obstacle
def add_obstacle():
    lane = random.randint(0, lanes - 1)
    y_position = safe_area_height + lane * lane_height + (lane_height - obstacle_height) // 2
    new_obstacle_rect = pygame.Rect(width, y_position, obstacle_width, obstacle_height)
    obstacle_image = random.choice(racecar_image)  # Select a random image from preloaded images

    # Check for overlap
    overlap = any(new_obstacle_rect.colliderect(obstacle['rect']) for obstacle in obstacles)
    if not overlap:
        obstacles.append({'rect': new_obstacle_rect, 'image': obstacle_image})

player_start_x = width // 2 - player_size // 2
player_start_y = (height - safe_area_height + (safe_area_height - player_size) // 2) + 15
player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5

    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += 5

    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5

    if keys[pygame.K_DOWN] and player.bottom < height:
        player.y += 5


    if random.randint(0, 100) > 96: # lower number to increase the chance of adding an obstacle
        add_obstacle()

    for obstacle in obstacles:
        obstacle['rect'].x -= obstacle_speed
        if obstacle['rect'].right < 0:
            obstacles.remove(obstacle)

    if any(player.colliderect(obstacle['rect']) for obstacle in obstacles):
        running = False # kills the game if you hit an obstacle

    screen.blit(full_image, (0, 0))
    pygame.draw.rect(screen, red, player)

    for obstacle in obstacles:
        screen.blit(obstacle['image'], obstacle['rect'].topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
