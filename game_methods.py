import pygame
import random
import main_screen


pygame.init()
from pygame import mixer

def easy():
    width, height = 1000, 750
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('The Crossing')

    #color variables
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    blue_menu = (41, 86, 143)
    green = (0, 255, 0)
    black = (0, 0, 0)
    yellow = (255, 189, 25)

    #game variables
    player_size = 40
    obstacle_width = 85
    obstacle_height = 50
    obstacle_speed = 6
    safe_area_height = 100
    middle_height = height - 2 * safe_area_height
    lanes = 7
    lane_height = middle_height // lanes

    #fonts
    font30 = pygame.font.SysFont('gillsansultracondensed', 30)
    font40 = pygame.font.SysFont('Constantia', 40)
    font50 = pygame.font.SysFont('Constantia', 70)
    font = pygame.font.SysFont('gillsansultracondensed', 40)

    #time
    clock = pygame.time.Clock()
    fps = 60
    countdown = 3
    last_count = pygame.time.get_ticks()
    timer = 45

    #endges/safety
    top_safe_area = pygame.Rect(0, 0, width, safe_area_height)

    #buttons
    return_button = pygame.Rect(width - 150, 5, 120, 40)
    return_text = font30.render("RETURN", True, white)

    #Images
    #character images
    playerReady_img = pygame.image.load("images/swimmerready.png").convert_alpha()
    playerReady_img = pygame.transform.scale(playerReady_img, (30, 40))
    playerSwim_img = pygame.image.load("images/swimming.png").convert_alpha()
    playerSwim_img = pygame.transform.scale(playerSwim_img, (30, 35))
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
    background_image = pygame.image.load('images/blue_bg.webp')
    background_image = pygame.transform.scale(background_image, (width, height))

    #object images
    barrel_img = pygame.image.load('images/barrel.png').convert_alpha()
    barrel_img = pygame.transform.scale(barrel_img, (50, 50))
    wood_img = pygame.image.load('images/floatingwood.png').convert_alpha()
    wood_img = pygame.transform.scale(wood_img, (80, 40))
    ship1_img = pygame.image.load('images/boat1.png').convert_alpha()
    ship1_img = pygame.transform.scale(ship1_img, (90, 60))
    ship2_img = pygame.image.load('images/boat2.png').convert_alpha()
    ship2_img = pygame.transform.scale(ship2_img, (90, 60))
    buoy_img = pygame.image.load('images/buoy.png').convert_alpha()
    buoy_img = pygame.transform.scale(buoy_img, (50, 70))
    red_boat_img = pygame.image.load('images/red_boat.png').convert_alpha()
    red_boat_img = pygame.transform.scale(red_boat_img, (85, 60))
    orange_boat_img = pygame.image.load('images/orange_boat.png').convert_alpha()
    orange_boat_img = pygame.transform.scale(orange_boat_img, (75, 60))

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

    #list and variables
    game_end = 0
    obstacles = []
    obstacle_images = []
    obstacles_right = []
    obstacles_left = []
    objects = [wood_img, barrel_img, ship1_img, buoy_img, ship2_img, red_boat_img, orange_boat_img, ship2_img,
               ship1_img]
    #creats text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

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
        time = clock.tick() / 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.blit(background_image, (0, 0))
                pygame.mixer.music.stop()
                main_screen.main()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    screen.blit(background_image, (0, 0))
                    main_screen.main()
                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.blit(background_image, (0, 0))
                    pygame.mixer.music.stop()
                    main_screen.main()
                    break
        if game_end == 1:  # this allows it to go to main screen when you lose or win
            main_screen.main()

        #once count reaches 0 things inside will start
        if countdown == 0:
            pygame.time.get_ticks()

            #win collision
            if player.colliderect(top_safe_area):
                screen.blit(background_image, (0, 0))  # "Enter game_over surface"
                win_fx.play()
                text = font50.render("YOU WIN!", True, white)
                screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                game_end = 1  # added this to go to the menu screen instead of exiting out

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player.top > 0:
                player.y -= 5
                surf_player = playerSwim_img
            if keys[pygame.K_DOWN] and player.bottom < width:
                player.y += 5
                surf_player = playerBack_img

                # collision
            if any(player.colliderect(obstacle) for obstacle in obstacles_left) or any(
                    player.colliderect(obstacle) for obstacle in obstacles_right):
                screen.blit(background_image, (0, 0))
                game_over.play()
                text = font50.render("GAME OVER", True, red)
                screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(3000) # kills the game if you hit an obstacle
                game_end = 1 # added this to go to the menu screen instead of exiting out

            #if times runs out they lose
            timer -= 1 / 60
            if timer <= 0:
                screen.blit(background_image, (0, 0))
                game_over.play()
                text = font50.render("GAME OVER", True, red)
                screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                game_end = 1  # kills the game if you hit an obstacle

        # obstacle direction/random
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
        # obsticle blit
        for obstacle, image in zip(obstacles_left, obstacle_images):
            screen.blit(image, obstacle)
        for obstacle, image in zip(obstacles_right, obstacle_images):
            screen.blit(image, obstacle)

        #starts the count down
        if countdown > 0:
            draw_text("Use ARROWS to get to the other side", font, blue_menu, width / 2 - 300, height - 450)
            draw_text("before the Time runs out.", font, blue_menu, width / 2 - 220, height - 410)
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
        pygame.draw.rect(screen, green, return_button, 2)
        screen.blit(return_text, (return_button.x + 9, return_button.y))
        #bottom blit
        screen.blit(sandBottom_img, (0, 680))
        screen.blit(dockFlip_img, (470, 650))
        screen.blit(palmtree_img, (345, 695))
        screen.blit(palmtree_img, (645, 690))
        screen.blit(palmtree_img, (145, 660))

        #player blit
        screen.blit(surf_player, player)
        #timer blit
        if countdown == 0:
            text = font30.render(f"Time: {int(timer)}", True, (255, 255, 255))
            screen.blit(text, (20, 20))

        pygame.display.flip()
        clock.tick(60)
        previous_time = clock.get_time()
        fps = clock.get_fps()

    main_screen.main()

def medium():
    pygame.init()

    width, height = 1000, 750
    screen = pygame.display.set_mode((width, height))

    # colors
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (10, 150, 100)
    gray = (200, 200, 200)
    black = (0, 0, 0)

    # timer and fonts
    timer = 34  # +4 to account for when timer hidden
    countdown = 7
    last_count = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    fps = 60
    font30 = pygame.font.SysFont('Constantia', 30)
    font40 = pygame.font.SysFont('Constantia', 40)
    font50 = pygame.font.SysFont('Constantia', 50)
    font70 = pygame.font.SysFont('Constantia', 70)

    # Dimentions
    player_size = 40
    obstacle_width = 80
    obstacle_height = 50
    obstacle_speed = 8
    safe_area_height = 100
    middle_height = height - 2 * safe_area_height
    lanes = 3
    lane_height = 65
    cars = 95  # (0-100)lower number to increase the chance of adding an obstacle
    top_safe_area = pygame.Rect(width / 2 - 50, 0, 100, safe_area_height - 50)

    return_button = pygame.Rect(width - 150, 5, 120, 40)
    return_text = font30.render("RETURN", True, black)

    # player
    player_start_x = width // 2 - player_size // 2
    player_start_y = height - player_size
    player = pygame.Rect(player_start_x, player_start_y, player_size, player_size)
    player_bunny = pygame.Surface((player_size, player_size))

    # music

    pygame.mixer.music.load('music/music.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
    game_over = pygame.mixer.Sound('music/game_over.wav')
    game_over.set_volume(0.5)
    win_fx = pygame.mixer.Sound('music/win.mp3')
    win_fx.set_volume(0.5)
    background_image = pygame.image.load('images/blue_bg.webp')
    background_image = pygame.transform.scale(background_image, (width, height))

    # images
    game_image = pygame.image.load('images/interstate.png').convert_alpha()
    game_image = pygame.transform.scale(game_image, (width, height))
    green_car = pygame.image.load('images/green_car.png').convert_alpha()
    green_car = pygame.transform.scale(green_car, (70, 60))
    blue_car = pygame.image.load('images/blue_car.png').convert_alpha()
    blue_car = pygame.transform.scale(blue_car, (70, 60))
    red_car = pygame.image.load('images/red_car.png').convert_alpha()
    red_car = pygame.transform.scale(red_car, (65, 60))
    grey_car = pygame.image.load('images/grey_car.png').convert_alpha()
    grey_car = pygame.transform.scale(grey_car, (65, 55))
    yellow_car = pygame.image.load('images/yellow_car.png').convert_alpha()
    yellow_car = pygame.transform.scale(yellow_car, (80, 90))
    siren_car = pygame.image.load('images/siren_car.png').convert_alpha()
    siren_car = pygame.transform.scale(siren_car, (80, 60))
    cop_car = pygame.image.load('images/cop_car.png').convert_alpha()
    cop_car = pygame.transform.scale(cop_car, (80, 60))
    jeep_car = pygame.image.load('images/jeep_car.png').convert_alpha()
    jeep_car = pygame.transform.scale(jeep_car, (80, 60))
    pink_car = pygame.image.load('images/pink_car.png').convert_alpha()
    pink_car = pygame.transform.scale(pink_car, (70, 56))
    red_truck = pygame.image.load('images/red_truck.png').convert_alpha()
    red_truck = pygame.transform.scale(red_truck, (80, 60))
    moss_car = pygame.image.load('images/moss_car.png').convert_alpha()
    moss_car = pygame.transform.scale(moss_car, (60, 60))
    burn_car = pygame.image.load('images/burn_car.png').convert_alpha()
    burn_car = pygame.transform.scale(burn_car, (60, 60))
    bunny_down = pygame.image.load('images/bunny_down.png').convert_alpha()
    bunny_down = pygame.transform.scale(bunny_down, (player_size, player_size))
    bunny_ready = pygame.image.load('images/bunny_ready.png').convert_alpha()
    bunny_ready = pygame.transform.scale(bunny_ready, (player_size, player_size))
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

    # car list
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

    # methods
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
        overlap = any(new_obstacle.colliderect(obstacle) for obstacle in obstacles_left) or any(
            new_obstacle_two.colliderect(obstacle) for obstacle in obstacles_right)
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    main_screen.main()
                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    main_screen.main()
                    break
                if countdown <= 0:
                    if event.key == pygame.K_UP and player.top > 0:
                        player.y -= player_size
                        player_bunny = bunny_ready
                    elif event.key == pygame.K_DOWN and player.bottom < height:
                        player.y += player_size
                        player_bunny = bunny_down


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

        # environment images
        screen.blit(grass, (0, height - 125))  # bottom grass
        screen.blit(pygame.transform.flip(grass, True, True), (0, -60))  # top grass
        screen.blit(side_bush, (width / 2 + 25, height - side_bush.get_height() / 2))
        screen.blit(side_bush, (width / 2 - 100, height - side_bush.get_height() / 2))  # right horiz bush
        screen.blit(pygame.transform.rotate(moss_car, 20), (70, height - 150))  # bottom moss car
        screen.blit(pygame.transform.rotate(pygame.transform.flip(moss_car, True, False), -30), (width - 150, 30))
        screen.blit(pygame.transform.rotate(burn_car, -20), (width - 260, 30))
        screen.blit(long_bush, (width / 2 + 50, height - long_bush.get_height() / 2))
        screen.blit(long_bush, (width / 2 - 150, height - long_bush.get_height() / 2))
        pygame.draw.ellipse(screen, black, (width / 2 - 50, 50, 100, 30))
        screen.blit(plants, (width / 2 - 50, 30))
        screen.blit(plants, (width / 2 - 5, 30))
        screen.blit(tall_tree, (width / 2 - 100, -10))
        screen.blit(tall_tree, (width / 2 + 20, -10))
        screen.blit(plants, (width / 2 + 15, 65))
        screen.blit(plants, (width / 2 - 70, 65))
        pygame.draw.rect(screen, black, return_button, 2)
        screen.blit(return_text, (return_button.x, return_button.y + 10))
        screen.blit(player_bunny, player)

        # obstacle created for screen
        for obstacle, image in zip(obstacles_left, obstacle_images_left):
            screen.blit(image, obstacle)
        for obstacle, image in zip(obstacles_right, obstacle_images_right):
            screen.blit(image, obstacle)

        # Lose Functions
        timer -= 1 / 60
        if timer <= 0:
            screen.blit(background_image, (0, 0))
            game_over.play()
            text = font70.render("GAME OVER", True, red)
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

        if any(player.colliderect(obstacle) for obstacle in obstacles_left) or any(
                player.colliderect(obstacle) for obstacle in obstacles_right):
            screen.blit(background_image, (0, 0))
            game_over.play()
            text = font70.render("GAME OVER", True, (red))
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # Win function
        if player.colliderect(top_safe_area):
            screen.blit(background_image, (0, 0))
            win_fx.play()
            text = font70.render("You Win!", True, (white))
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(60)
    main_screen.main()

def hard():
    pygame.init()

    width, height = 1000, 750
    screen = pygame.display.set_mode((width, height))
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    player_size = 50
    obstacle_width = 160
    obstacle_height = 100
    obstacle_speed = 6
    safe_area_height = 100
    middle_height = height - 2 * safe_area_height
    lanes = 6
    lane_height = middle_height // lanes
    font40 = pygame.font.SysFont('Constantia', 40)
    font50 = pygame.font.SysFont('Constantia', 70)
    font30 = pygame.font.SysFont('Constantia', 30)
    timer = 15
    top_safe_area = pygame.Rect(0, 0, width, safe_area_height)
    bottom_safe_area = pygame.Rect(0, height - safe_area_height, width, safe_area_height)
    middle_area = pygame.Rect(0, safe_area_height, width, middle_height)

    return_button = pygame.Rect(width - 110, 10, 100, 50)
    return_text = font30.render("Return to Menu", True, white)
    # sound
    pygame.mixer.music.load('music/music.wav')
    pygame.mixer.music.play(-1, 0.0, 5000)
    game_over = pygame.mixer.Sound('music/game_over.wav')
    game_over.set_volume(0.5)
    win_fx = pygame.mixer.Sound('music/win.mp3')
    win_fx.set_volume(0.5)

    # images
    player_image = pygame.image.load('images/cat.png')
    player_image = pygame.transform.scale(player_image, (player_size, player_size))
    cat_bed = pygame.image.load('images/cat_bed.png')
    cat_bed = pygame.transform.scale(cat_bed, (75, 75))
    lane_image = pygame.image.load('images/lane_image.png')
    lane_image = pygame.transform.scale(lane_image, (width, lane_height + 5))
    top_image = pygame.image.load('images/top_image.png')
    top_image = pygame.transform.scale(top_image, (width, safe_area_height))
    bottom_image = pygame.image.load('images/bottom_image.png')
    bottom_image = pygame.transform.scale(bottom_image, (width, safe_area_height))
    racecar_images = ['images/off_road_car.png', 'images/off_road_car2.png', 'images/off_road_car3.png']
    racecar_image = [pygame.image.load(image) for image in racecar_images]
    racecar_image = [pygame.transform.scale(image, (obstacle_width, obstacle_height)) for image in racecar_image]
    top_center_x = (width - cat_bed.get_width()) // 2
    top_center_y = (safe_area_height - cat_bed.get_height()) // 2
    background_image = pygame.image.load('images/blue_bg.webp')
    background_image = pygame.transform.scale(background_image, (width, height))
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

    game_state = 'countdown'
    countdown = 3
    start_ticks = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                main_screen.main()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    main_screen.main()
                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    main_screen.main()
                    break

        keys = pygame.key.get_pressed()
        if game_state == 'playing':
            if keys[pygame.K_UP] and player.top > 0:
                player.y -= 5
            if keys[pygame.K_DOWN] and player.bottom < height:
                player.y += 5


        timer -= 1 / 60
        if timer <= 0:
            screen.blit(background_image, (0, 0))
            game_over.play()
            text = font50.render("GAME OVER", True, red)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        if random.randint(0, 100) > 94:
            add_obstacle()

        for obstacle in obstacles:
            obstacle['rect'].x -= obstacle_speed
            if obstacle['rect'].right < 0:
                obstacles.remove(obstacle)

        if any(player.colliderect(obstacle['rect']) for obstacle in obstacles):
            screen.blit(background_image, (0, 0))
            game_over.play()
            text = font50.render("GAME OVER", True, red)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        if top_safe_area.contains(player):
            pygame.time.wait(500)
            screen.blit(background_image, (0, 0))
            win_fx.play()
            text = font50.render("YOU WIN!", True, white)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        screen.blit(top_image, (0, 0))
        screen.blit(bottom_image, (0, height - safe_area_height))
        for i in range(lanes):
            lane_y_position = safe_area_height + i * lane_height
            screen.blit(lane_image, (0, lane_y_position))
        for obstacle in obstacles:
            screen.blit(obstacle['image'], obstacle['rect'].topleft)



        screen.blit(player_image, player.topleft)
        screen.blit(cat_bed, (top_center_x, top_center_y))

        if game_state == 'countdown':
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds >= countdown:
                game_state = 'playing'
                timer = 15

            else:
                instruction_text = font40.render("Get to the cat bed without being ran over", True, black)
                screen.blit(instruction_text, (width / 2 - instruction_text.get_width() / 2, height / 2 - 100))
                countdown_text = font50.render(f"Get ready! {countdown - int(seconds)}", True, red)
                screen.blit(countdown_text, (width / 2 - countdown_text.get_width() / 2, height / 2))
        if game_state == 'playing':
            text = font50.render(f"Time: {int(timer)}", True, white)
            screen.blit(text, (10, 10))
        pygame.draw.rect(screen, black, return_button)
        screen.blit(return_text, (return_button.x + 10, return_button.y + 10))
        pygame.display.flip()
        clock.tick(60)

    main_screen.main()