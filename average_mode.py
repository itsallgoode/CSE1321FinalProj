import pygame
import random
import sys
import loading_screen


pygame.init()

width, height = 1000, 750
screen = pygame.display.set_mode((width, height))

#colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (200, 200, 200)
black = (0, 0, 0)

#timer and fonts
timer = 34 #+4 to account for when timer hidden
countdown = 7
last_count = pygame.time.get_ticks()
clock = pygame.time.Clock()
fps = 60
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font50 = pygame.font.SysFont('Constantia', 70)

#Dimentions
player_size = 40
obstacle_width = 80
obstacle_height = 50
obstacle_speed = 8
safe_area_height = 100
middle_height = height - 2 * safe_area_height
lanes = 3
lane_height = 65
cars = 92 #(0-100)lower number to increase the chance of adding an obstacle
top_safe_area = pygame.Rect(width / 2 - 50 , 0, 100 , safe_area_height - 50)
bottom_safe_area = pygame.Rect(0, height - safe_area_height, width, safe_area_height)
middle_area = pygame.Rect(0, safe_area_height, width, middle_height)


#player
player_start_x = width // 2 - player_size // 2
player_start_y = height - player_size
player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)
player_bunny = pygame.Surface((player_size, player_size))

#music
background_music = pygame.mixer.Sound('music/music.wav')
channel = pygame.mixer.Channel(0)
game_over = pygame.mixer.Sound('music/game_over.wav')
win = pygame.mixer.Sound('music/win.mp3')

#images
game_image = pygame.image.load('images/interstate.png').convert_alpha()
game_image = pygame.transform.scale(game_image, (width, height))
green_car = pygame.image.load('images/green_car.png').convert_alpha()
green_car = pygame.transform.scale(green_car, (70 , 60))
blue_car = pygame.image.load('images/blue_car.png').convert_alpha()
blue_car = pygame.transform.scale(blue_car, (70 , 60))
red_car = pygame.image.load('images/red_car.png').convert_alpha()
red_car = pygame.transform.scale(red_car, (65 , 60))
grey_car = pygame.image.load('images/grey_car.png').convert_alpha()
grey_car = pygame.transform.scale(grey_car, (65 , 55))
yellow_car = pygame.image.load('images/yellow_car.png').convert_alpha()
yellow_car = pygame.transform.scale(yellow_car, (80 , 90))
siren_car = pygame.image.load('images/siren_car.png').convert_alpha()
siren_car = pygame.transform.scale(siren_car, (80 , 60))
cop_car = pygame.image.load('images/cop_car.png').convert_alpha()
cop_car = pygame.transform.scale(cop_car, (80 , 60))
jeep_car = pygame.image.load('images/jeep_car.png').convert_alpha()
jeep_car = pygame.transform.scale(jeep_car, (80 , 60))
pink_car = pygame.image.load('images/pink_car.png').convert_alpha()
pink_car = pygame.transform.scale(pink_car, (70 , 56))
red_truck = pygame.image.load('images/red_truck.png').convert_alpha()
red_truck = pygame.transform.scale(red_truck, (80 , 60))
moss_car = pygame.image.load('images/moss_car.png').convert_alpha()
moss_car = pygame.transform.scale(moss_car, (60 , 60))
burn_car = pygame.image.load('images/burn_car.png').convert_alpha()
burn_car = pygame.transform.scale(burn_car, (60 , 60))
bunny_down = pygame.image.load('images/bunny_down.png').convert_alpha()
bunny_down = pygame.transform.scale(bunny_down, (player_size , player_size))
bunny_ready = pygame.image.load('images/bunny_ready.png').convert_alpha()
bunny_ready =pygame.transform.scale(bunny_ready, (player_size, player_size))
bunny_left = pygame.image.load('images/bunny_left.png').convert_alpha()
bunny_left = pygame.transform.scale(bunny_left, (player_size, player_size))
bunny_right = pygame.image.load('images/bunny_right.png').convert_alpha()
bunny_right = pygame.transform.scale(bunny_right, (player_size, player_size))
long_bush = pygame.image.load('images/long_bush.png').convert_alpha()
long_bush = pygame.transform.scale(long_bush, (100, 60))
side_bush = pygame.image.load('images/side_bush.png').convert_alpha()
side_bush = pygame.transform.scale(side_bush, (70, 200))
grass = pygame.image.load('images/grass.png').convert_alpha()
grass = pygame.transform.scale(grass, (width, 200))
plants = pygame.image.load('images/plants.png').convert_alpha()
plants = pygame.transform.scale(plants, (50, 30))
tall_tree = pygame.image.load('images/tall_tree.png').convert_alpha()
tall_tree = pygame.transform.scale(tall_tree, (80, 100))
background_image = pygame.image.load('images/blue_bg.webp')
background_image = pygame.transform.scale(background_image, (width, height))

#car list
vehicles = [green_car, blue_car, red_car, grey_car, yellow_car, siren_car, cop_car, pink_car, red_truck, jeep_car]
vehicles_swap = [
    pygame.transform.flip(green_car, True, False),
    pygame.transform.flip(blue_car, True, False),
    pygame.transform.flip(yellow_car, True, False),
    pygame.transform.flip(siren_car, True, False),
    pygame.transform.flip(red_car, True, False),
    pygame.transform.flip(grey_car, True, False),
    pygame.transform.flip(cop_car, True, False)
]

obstacle_images_left = []
obstacle_images_right = []
obstacles_right = []
obstacles_left = []

clock = pygame.time.Clock()
channel.play(background_music)

#methods
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# randomly selects a lane and calculates the position for a new obstacle
def add_obstacle():
    lane = random.randint(0, lanes - 1)
    y_position_one = 30 + (safe_area_height + lane * lane_height)
    new_obstacle = pygame.Rect(width, y_position_one, obstacle_width, obstacle_height)

    y_position_two = ((middle_height / 2 + 130) + lane * lane_height) + 5
    new_obstacle_two = pygame.Rect(0 - obstacle_width, y_position_two, obstacle_width, obstacle_height)

    # keeps the obstacles from overlapping
    overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles_left) or any(new_obstacle_two.colliderect(obstacle) for obstacle in obstacles_right)
    if not overlap:
        obstacles_left.append(new_obstacle)
        obstacle_images_left.append(random.choice(vehicles))
        obstacles_right.append(new_obstacle_two)
        obstacle_images_right.append(random.choice(vehicles_swap))

running = True
player_bunny = bunny_ready

while running:
    screen.blit(game_image, (0, 0))
    time = clock.tick() / 100
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if countdown <= 0:
                if event.key == pygame.K_LEFT and player.left > 0:
                    player.x -= player_size
                    player_bunny = bunny_left
                elif event.key == pygame.K_RIGHT and player.right < width:
                    player.x += player_size
                    player_bunny = bunny_right
                elif event.key == pygame.K_UP and player.top > 0:
                    player.y -= player_size
                    player_bunny = bunny_ready
                elif event.key == pygame.K_DOWN and player.bottom < height:
                    player.y += player_size
                    player_bunny = bunny_down
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    # directions and countdown settings
    if countdown == 0:
        time_now = pygame.time.get_ticks()

    if countdown > 0 and countdown <= 3:
        draw_text("GET READY!", font40, white, int(width / 2 - 110), int(height / 2 - 20))
        draw_text(str(countdown), font40, white, int(width / 2 - 10), int(height / 2))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    if countdown > 3:
        draw_text("Use the arrow keypad to reach the rabbit hole", font50, black, int(5), int(height / 2 - 20))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    if random.randint(0, 100) > cars:
        add_obstacle()

    for obstacle, image in zip(obstacles_left, obstacle_images_left[:len(obstacles_left)]):
        obstacle.x -= obstacle_speed
        if obstacle.right < 0:
            obstacles_left.remove(obstacle)
            obstacle_images_left.pop(0)

    for obstacle, image in zip(obstacles_right, obstacle_images_right[:len(obstacles_right)]):
        obstacle.x += obstacle_speed
        if obstacle.right > 1000 + obstacle_width:
            obstacles_right.remove(obstacle)
            obstacle_images_right.pop(0)

    #environment images
    screen.blit(grass, (0,  height - 125)) #bottom grass
    screen.blit(pygame.transform.flip(grass, True, True), (0, -60)) #top grass
    screen.blit(side_bush, (width / 2 + 25 , height - side_bush.get_height() / 2))
    screen.blit(side_bush, (width / 2 - 100 , height - side_bush.get_height() / 2)) #right horiz bush
    screen.blit(pygame.transform.rotate(moss_car, 20), (70, height - 150))#bottom moss car
    screen.blit(pygame.transform.rotate(pygame.transform.flip(moss_car, True, False), -30),(width - 150 , 30 ))
    screen.blit(pygame.transform.rotate(burn_car, -20), (width - 260 , 30 ))
    screen.blit(long_bush, (width / 2 + 50 , height - long_bush.get_height() / 2))
    screen.blit(long_bush, (width / 2 - 150 , height - long_bush.get_height() / 2))
    pygame.draw.ellipse(screen, black , (width / 2 - 50, 50 , 100 , 30))
    screen.blit(plants, (width / 2 - 50, 30))
    screen.blit(plants, (width / 2 - 5, 30))
    screen.blit(tall_tree, (width / 2 - 100, -10))
    screen.blit(tall_tree, (width / 2 + 20, -10))
    screen.blit(plants, (width / 2 + 15, 65))
    screen.blit(plants, (width / 2 - 70, 65))
    screen.blit(player_bunny, player)



    #obstacle created for screen
    for obstacle, image in zip(obstacles_left, obstacle_images_left):
        screen.blit(image, obstacle)
    for obstacle, image in zip(obstacles_right, obstacle_images_right):
        screen.blit(image, obstacle)

    # Lose Functions
    timer -= 1 / 60
    if timer <= 0:
        screen.blit(background_image, (0, 0))
        game_over.play()
        text = font50.render("GAME OVER", True, red)
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # display timer
    if countdown <= 0:
        text = font30.render(f"Time: {int(timer)}", True, (0, 0, 0))
        screen.blit(text, (10, 10))
    clock.tick(60)
    previous_time = clock.get_time()
    fps = clock.get_fps()

    if any(player.colliderect(obstacle) for obstacle in obstacles_left) or any(player.colliderect(obstacle) for obstacle in obstacles_right):
        screen.blit(background_image, (0, 0))
        channel.play(game_over)
        text = font50.render("GAME OVER", True, (red))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

        # Win function
        if player.colliderect(top_safe_area):
            screen.blit(background_image, (0, 0))
            channel.play(win)
            text = font50.render("You Win!", True, (white))
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
#loading_screen.main()