import pygame
import random
import sys
import os 

def main():  
        
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
                return
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    running = False
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    pygame.quit()
                    os.system("python loading_screen.py")
                    sys.exit()
        keys = pygame.key.get_pressed()
        if game_state == 'playing':
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= 5
            if keys[pygame.K_RIGHT] and player.right < width:
                player.x += 5
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

        if random.randint(0, 100) > 95:
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
            pygame.quit()
            os.system("python loading_screen.py")
            sys.exit()
        if top_safe_area.contains(player):
            pygame.time.wait(500)  
            screen.blit(background_image, (0, 0))
            win_fx.play() 
            text = font50.render("YOU WIN!", True, white) 
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(3000)  
            running = False
            pygame.quit()
            os.system("python loading_screen.py")
            sys.exit()
        screen.blit(top_image, (0, 0))
        screen.blit(bottom_image, (0, height - safe_area_height))
        for i in range(lanes):
            lane_y_position = safe_area_height + i * lane_height
            screen.blit(lane_image, (0, lane_y_position))
        for obstacle in obstacles:
            screen.blit(obstacle['image'], obstacle['rect'].topleft)

        text = font50.render(f"Time: {int(timer)}", True, white)
        screen.blit(text, (10, 10))
        screen.blit(player_image, player.topleft)
        screen.blit(cat_bed, (top_center_x, top_center_y))

        if game_state == 'countdown':
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds >= countdown:
                game_state = 'playing'
            else:
                instruction_text = font40.render("Get to the cat bed without being ran over", True, black)
                screen.blit(instruction_text, (width / 2 - instruction_text.get_width() / 2, height / 2 - 100))
                countdown_text = font50.render(f"Get ready! {countdown - int(seconds)}", True, red)
                screen.blit(countdown_text, (width / 2 - countdown_text.get_width() / 2, height / 2))
        

        pygame.draw.rect(screen, black, return_button)
        screen.blit(return_text, (return_button.x + 10, return_button.y + 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

