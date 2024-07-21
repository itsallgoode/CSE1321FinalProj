import pygame
from pygame.locals import *
import random
import sys

#from pygame import mixer

pygame.init()

width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Crossing')

#color variables
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (200, 200, 200)
black = (0, 0, 0)
yellow = (255, 189, 25)

#game variables
player_size = 40
obstacle_width = 85
obstacle_height = 50
obstacle_speed = 6
safe_area_height = 100
middle_height = height - 2 * safe_area_height
lanes = 3
lane_height = middle_height // lanes

#fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font50 = pygame.font.SysFont('Constantia', 50)

#time
clock = pygame.time.Clock()
fps = 60
countdown = 3
last_count = pygame.time.get_ticks()
timer = 30

#endges/safety
top_safe_area = pygame.Rect(0, 0, width, safe_area_height)
bottom_safe_area = pygame.Rect(0, 90 - safe_area_height, width, safe_area_height)
middle_area = pygame.Rect(0, safe_area_height, width, middle_height)

#Images
#character images
playerReady_img = pygame.image.load("images/swimmerready.png").convert_alpha()
playerReady_img = pygame.transform.scale(playerReady_img, (30, 40))
playerSwim_img = pygame.image.load("images/swimming.png").convert_alpha()
playerSwim_img = pygame.transform.scale(playerSwim_img, (30, 40))
playerLeft_img = pygame.image.load("images/swimmerleft.png").convert_alpha()
playerLeft_img = pygame.transform.scale(playerLeft_img, (35, 35))
playerRight_img = pygame.image.load("images/swimmerright.png").convert_alpha()
playerRight_img = pygame.transform.scale(playerRight_img, (35, 35))
playerBack_img = pygame.image.load("images/swimmerback.png").convert_alpha()
playerBack_img = pygame.transform.scale(playerBack_img, (35, 35))
surf_player = playerReady_img


#background images
water_img = pygame.image.load("images/Water.png").convert_alpha()
water_img = pygame.transform.scale(water_img, (width, height))
sandTop_img = pygame.image.load('images/Topbeach.png').convert_alpha()
sandTop_img = pygame.transform.scale(sandTop_img, (width, safe_area_height - 20))
sandBottom_img = pygame.image.load('images/Bottombeach.png').convert_alpha()
sandBottom_img = pygame.transform.scale(sandBottom_img, (width, safe_area_height))
palmtree_img = pygame.image.load('images/Palmtree.png').convert_alpha()
palmtree_img = pygame.transform.scale(palmtree_img, (50, 50))
dock_img = pygame.image.load('images/dock.png')
dockFlip_img = pygame.image.load('images/Dockflip.png')

#object images
barrel_img = pygame.image.load('images/barrel.png').convert_alpha()
barrel_img = pygame.transform.scale(barrel_img, (50, 50))
wood_img = pygame.image.load('images/floatingwood.png').convert_alpha()
wood_img = pygame.transform.scale(wood_img, (80, 40))
ship1_img = pygame.image.load('images/boat1.png').convert_alpha()
ship1_img = pygame.transform.scale(ship1_img, (110, 60))
ship2_img = pygame.image.load('images/boat2.png').convert_alpha()
ship2_img = pygame.transform.scale(ship2_img, (110, 60))
buoy_img = pygame.image.load('images/buoy.png').convert_alpha()
buoy_img = pygame.transform.scale(buoy_img, (50, 70))

#sound
pygame.mixer.music.load('music/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
game_over = pygame.mixer.Sound('music/game_over.wav')
game_over.set_volume(0.5)
win_fx = pygame.mixer.Sound('music/win.mp3')
win_fx.set_volume(0.5)

#player
player_start_x = width // 2 - player_size // 2
player_start_y = height - safe_area_height + (safe_area_height - 30 - player_size) // 2
player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)
player_surf = pygame.Surface((30, 100))


#creats text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

obstacles = []
obstacle_images = []
obstacles_right = []
obstacles_left = []
objects = [wood_img, barrel_img, ship1_img, buoy_img, ship2_img]


# randomly selects a lane and calculates the position for a new obstacle
def add_obstacle():
    lane = random.randint(0, lanes - 1)
    y_position_one = (safe_area_height - 95 + lane * lane_height + lane_height) + 20
    new_obstacle = pygame.Rect(width, y_position_one, obstacle_width, obstacle_height)
    # keeps the obstacles from overlapping
    overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles_left)
    if not overlap:
        obstacles_left.append(new_obstacle)
        obstacle_images.append(random.choice(objects))


running = True
while running:
    screen.fill(white)
    screen.blit(water_img, (0, 0))
    player_surf = playerReady_img
    time = clock.tick() / 100
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    #once count reaches 0 things inside will start
    if countdown == 0:
        time_now = pygame.time.get_ticks()
        player_surf = playerSwim_img

        #win collision
        if player.colliderect(top_safe_area):
            screen.fill(blue)  # "Enter game_over surface"
            win_fx.play()
            text = font50.render("YOU WIN!", True, yellow)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        #obstacle direction/random
        if random.randint(0, 100) > 96:  # lower number to increase the chance of adding an obstacle
            add_obstacle()

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed
            if obstacle.right < 0:
                obstacles.remove(obstacle)

        for obstacle, image in zip(obstacles_left, obstacle_images[:len(obstacles_left)]):
            obstacle.x -= obstacle_speed
            if obstacle.right < 0:
                obstacles_left.remove(obstacle)
                obstacle_images.pop(0)

        for obstacle, image in zip(obstacles_right, obstacle_images[:len(obstacles_left)]):
            obstacle.x += obstacle_speed
            if obstacle.right > 1000 + obstacle_width:
                obstacles_right.remove(obstacle)
                obstacle_images.pop(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
            surf_player = playerLeft_img
        if keys[pygame.K_RIGHT] and player.right < width:
            player.x += 5
            surf_player = playerRight_img
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= 5
            surf_player = playerSwim_img
        if keys[pygame.K_DOWN] and player.bottom < width:
            player.y += 5
            surf_player = playerBack_img

        #if times runs out they lose
        timer -= 1 / 60
        if timer <= 0:
            screen.fill(black)
            game_over.play()
            text = font50.render("GAME OVER", True, red)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False  # kills the game if you hit an obstacle

        #collision
        if any(player.colliderect(obstacle) for obstacle in obstacles_left) or any(
                player.colliderect(obstacle) for obstacle in obstacles_right):
            screen.fill(black)
            game_over.play()
            text = font50.render("GAME OVER", True, red)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False  # kills the game if you hit an obstacle

    #starts the count down
    if countdown > 0:
        draw_text("GET READY!", font40, white, int(width / 2 - 110), int(height / 2 + 50))
        draw_text(str(countdown), font40, white, int(width / 2 - 10), int(height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    #top blit
    screen.blit(sandTop_img, (0, 0))
    screen.blit(dock_img, (470, 0))
    screen.blit(palmtree_img, (430, 0))
    screen.blit(palmtree_img, (750, 0))
    screen.blit(palmtree_img, (130, 15))
    #bottom blit
    screen.blit(sandBottom_img, (0, 680))
    screen.blit(dockFlip_img, (470, 650))
    screen.blit(palmtree_img, (345, 695))
    screen.blit(palmtree_img, (645, 690))
    screen.blit(palmtree_img, (145, 660))
    #obsticle blit
    for obstacle, image in zip(obstacles_left, obstacle_images):
        screen.blit(image, obstacle)
    for obstacle, image in zip(obstacles_right, obstacle_images):
        screen.blit(image, obstacle)
    #player blit
    screen.blit(surf_player, player)
    #timer blit
    text = font30.render(f"Time: {int(timer)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
    previous_time = clock.get_time()
    fps = clock.get_fps()

pygame.quit()
sys.exit()
