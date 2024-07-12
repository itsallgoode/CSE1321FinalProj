

import pygame
import sys
import random


pygame.init()


width, height = 640, 480
player_size = 20
finish_size = 10
obstacle_size = 50
timer = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


screen = pygame.display.set_mode((width, height))


font = pygame.font.Font(None, 36)


player = pygame.Rect((width / 2) - player_size, height - player_size * 2, player_size, player_size)
finish = pygame.Rect(0, 0, width, finish_size)  #(x,y,w,l)

obstacles = [
    pygame.Rect(-obstacle_size, random.randint(0, height - obstacle_size), obstacle_size, obstacle_size),
    pygame.Rect(width-obstacle_size, random.randint(0, height - obstacle_size), obstacle_size, obstacle_size),
    pygame.Rect(width-obstacle_size, random.randint(0, height - obstacle_size), obstacle_size, obstacle_size),
    pygame.Rect(-obstacle_size, random.randint(0, height - obstacle_size), obstacle_size, obstacle_size),
]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

#player movement
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_UP]:
        player.y -= 5
    if keys[pygame.K_DOWN]:
        player.y += 5

    for obstacle in obstacles:
        if obstacle.x < 0:
            obstacle.x = width
        elif obstacle.x > width:
            obstacle.x = -obstacle_size
        obstacle.x -= 2 if obstacle == obstacles[2] else 2


    if player.colliderect(finish):
        screen.fill(WHITE)  #Enter you_win background surface"
                            #"play sound" channel.play(win_sound) - referencing var (win_sound)
        text = font.render("You win!", True, (0, 0, 0))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    for obstacle in obstacles:
        if player.colliderect(obstacle):
            screen.fill(WHITE)  #"Enter game_over surface"
                                 #"Play sound"  channel.play(dead sound) - referencing variable(dead_sound)
            text = font.render("Game over", True, (0, 0, 0))  #aliasing makes font smooth
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()


    timer -= 1 / 60
    if timer <= 0:
        screen.fill(WHITE)
        text = font.render("Game over", True, (0, 0, 0))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()


    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, YELLOW, finish)
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 0, 0), obstacle)
    text = font.render(f"Time: {int(timer)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()

    clock.tick(60)