import pygame
import sys
import os
from pygame.locals import *

width = 1000
height = 750
screen = pygame.display.set_mode((1000, 750))

#defines colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (0, 0, 255)
blue = (41, 86, 143)


class Button():
    def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action

def load_assets():
    pygame.time.delay(2000)  # Simulate loading assets with a delay

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def show_loading_screen(screen):
    pygame.mixer.music.load("music/music.wav")
    pygame.mixer.music.play(-1, 0.0, 5000)
    font30 = pygame.font.SysFont('gillsansultracondensed', 30)
    font20 = pygame.font.SysFont('gillsansultracondensed', 20)
    font = pygame.font.SysFont('gillsansultracondensed', 70)
    font_title = pygame.font.SysFont('maturascriptcapitals', 100)

    #button rects
    easy_rect = pygame.Rect(365, 295, 270, 50)
    medium_rect = pygame.Rect(365, 375, 270, 50)
    hard_rect = pygame.Rect(365, 460, 270, 50)
    exit_rect = pygame.Rect(365, 545, 270, 50)

    # Button setup
    #button_color = (0, 128, 0)
    #button_rect = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 50, 200, 50)
    #button_text = font.render('Start Game', True, (255, 255, 255))
    #button_text_rect = button_text.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, blue, easy_rect)
    pygame.draw.rect(screen, blue, medium_rect)
    pygame.draw.rect(screen, blue, hard_rect)
    pygame.draw.rect(screen, blue, exit_rect)
    draw_text("The Crossing", font_title, white, width - 820, height - 695)
    draw_text("The Crossing", font_title, blue, width - 820, height - 700)
    draw_text("MAIN MENU", font, blue, width - 680, height - 555)
    draw_text("MAIN MENU", font, white, width - 680, height - 560)
    draw_text("EASY", font30, white, width / 2 - 35, height - 450)
    draw_text("MEDIUM", font30, white, width / 2 - 50, height - 370)
    draw_text("HARD", font30, white, width / 2 - 35, height - 280)
    draw_text("EXIT", font30, white, width / 2 - 25, height - 200)

    #pygame.draw.rect(screen, button_color, button_rect)
    #screen.blit(button_text, button_text_rect)
    pygame.display.flip()

    load_assets()

def main():
    pygame.init()
    screen.fill(white)
    pygame.display.set_caption("Start Screen")
    bg = pygame.image.load('images/blue_bg.webp')
    bg = pygame.transform.scale(bg, (1000, 750))
    screen.blit(bg, (0, 0))
    show_loading_screen(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if menu_button.collidepoint(mouse_pos):
                    # Assuming game2.py is in the same directory and is executable
                    os.system("python game2.py")
                    running = False

    pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

