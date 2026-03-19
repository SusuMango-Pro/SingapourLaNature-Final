import pygame
from button import Button
import sys
from playscreen import PLAY_MENU

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

try:
    CURSOR_IMG = pygame.transform.scale(
        pygame.image.load("assets/SpriteJump/Bird1.png").convert_alpha(), (50, 50)
    )
except:
    CURSOR_IMG = None

def get_font_playful(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

def main_menu():
    START_BUTTON = Button(
        image=pygame.image.load("assets/mainmenubutton.png"),
        pos=(640, 250),
        text_input="COMMENCER",
        font=get_font_playful(36),
        base_color="#18af0dc1",
        hovering_color="White"
    )
    QUIT_BUTTON = Button(
        image=pygame.image.load("assets/mainmenubutton.png"),
        pos=(640, 500),
        text_input="QUITTER",
        font=get_font_playful(36),
        base_color="#18af0dc1",
        hovering_color="White"
    )

    bg = pygame.image.load("assets/SgMapBlurred.png")

    while True:
        clock.tick(60)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAY_MENU()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        SCREEN.blit(bg, (0, 0))
        START_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        START_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)

        if CURSOR_IMG:
            mx, my = pygame.mouse.get_pos()
            SCREEN.blit(CURSOR_IMG, (mx - 25, my - 25))

        pygame.display.update()

main_menu()