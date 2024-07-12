import pygame
import sys
import os

def load_assets():
    pygame.time.delay(2000)  # Simulate loading assets with a delay

def show_loading_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render('Loading...', True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    # Button setup
    button_color = (0, 128, 0)
    button_rect = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 50, 100, 50)
    button_text = font.render('Start Game', True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, button_text_rect)
    pygame.display.flip()

    load_assets()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Loading Screen")

    show_loading_screen(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    # Assuming game2.py is in the same directory and is executable
                    os.system("python game2.py")
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

