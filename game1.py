import pygame
import sys

def load_assets():
    # Simulate loading assets with a delay
    pygame.time.delay(2000)  # Delay for 2 seconds, for example

def show_loading_screen(screen):
    # Set up font and colors
    font = pygame.font.Font(None, 36)
    text = font.render('Loading...', True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

    # Display loading text
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Load assets (simulate with a delay)
    load_assets()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Loading Screen")

    show_loading_screen(screen)

    # Main game loop would go here
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
