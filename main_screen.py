import pygame
import sys
import game_methods
# Initialize Pygame
pygame.init()

# Screen dimensions
width = 1000
height = 750
screen = pygame.display.set_mode((width, height))

# Define colors
white = (255, 255, 255)
blue = (41, 86, 143)

# Load and scale background image
background_image = pygame.image.load('images/blue_bg.webp')
background_image = pygame.transform.scale(background_image, (width, height))

# Define button rectangles
easy_rect = pygame.Rect(365, 295, 270, 50)
medium_rect = pygame.Rect(365, 375, 270, 50)
hard_rect = pygame.Rect(365, 460, 270, 50)
exit_rect = pygame.Rect(365, 545, 270, 50)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def show_loading_screen():
    # Draw background image
    screen.blit(background_image, (0, 0))

    font_title = pygame.font.SysFont('maturascriptcapitals', 100)
    font = pygame.font.SysFont('gillsansultracondensed', 70)
    font30 = pygame.font.SysFont('gillsansultracondensed', 30)

    # Draw buttons
    pygame.draw.rect(screen, blue, easy_rect)
    pygame.draw.rect(screen, blue, medium_rect)
    pygame.draw.rect(screen, blue, hard_rect)
    pygame.draw.rect(screen, blue, exit_rect)

    # Draw text
    draw_text("The Crossing", font_title, white, width - 820, height - 700)
    draw_text("The Crossing", font_title, blue, width - 820, height - 705)
    draw_text("MAIN MENU", font, blue, width - 680, height - 560)
    draw_text("MAIN MENU", font, white, width - 680, height - 565)
    draw_text("EASY", font30, white, width / 2 - 35, height - 450)
    draw_text("MEDIUM", font30, white, width / 2 - 50, height - 370)
    draw_text("HARD", font30, white, width / 2 - 35, height - 280)
    draw_text("EXIT", font30, white, width / 2 - 25, height - 200)

    pygame.display.flip()  # Update the display

def main():
    show_loading_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_rect.collidepoint(mouse_pos):
                    game_methods.easy()
                elif medium_rect.collidepoint(mouse_pos):
                    game_methods.medium()
                elif hard_rect.collidepoint(mouse_pos):
                    game_methods.hard()
                elif exit_rect.collidepoint(mouse_pos):
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()




