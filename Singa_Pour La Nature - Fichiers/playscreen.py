import pygame
import sys
from button import Button
from infoscreen import show_info
from sungei import LEVEL1
from zoo import LEVEL2
from sentosa import LEVEL3
from bukit import LEVEL4
from punggol import LEVEL5
from jurong import LEVEL6
from botanic import LEVEL7

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

try:
    CURSOR_IMG = pygame.transform.scale(
        pygame.image.load("assets/SpriteJump/Bird1.png").convert_alpha(), (50, 50)
    )
except:
    CURSOR_IMG = None

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def get_font_label(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

font_label = get_font_label(16)

sungei  = Button(image=pygame.image.load("assets/marker.png"), pos=(295, 230),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
zoo     = Button(image=pygame.image.load("assets/marker.png"), pos=(520, 158),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
sentosa = Button(image=pygame.image.load("assets/marker.png"), pos=(621, 527),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
bukit   = Button(image=pygame.image.load("assets/marker.png"), pos=(430, 280),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
punggol = Button(image=pygame.image.load("assets/marker.png"), pos=(620, 200),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
jurong  = Button(image=pygame.image.load("assets/marker.png"), pos=(480, 380),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")
botanic = Button(image=pygame.image.load("assets/marker.png"), pos=(500, 460),
                 text_input="", font=get_font(75), base_color="#18af0dc1", hovering_color="White")

label_sungei  = font_label.render("Sungei Buloh",          True, "#0097b2")
label_zoo     = font_label.render("Singapore Zoo",         True, "#0097b2")
label_sentosa = font_label.render("Sentosa Serapong",      True, "#0097b2")
label_bukit   = font_label.render("Bukit Timah",           True, "#0097b2")
label_punggol = font_label.render("Punggol Waterway",      True, "#0097b2")
label_jurong  = font_label.render("Jurong Bird Park",      True, "#0097b2")
label_botanic = font_label.render("Botanic Gardens", True, "#0097b2")


def PLAY_MENU():
    map_img = pygame.image.load("assets/SingaporeMap.png")
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sungei.checkForInput(MENU_MOUSE_POS):
                    show_info("sungei", LEVEL1)
                if zoo.checkForInput(MENU_MOUSE_POS):
                    show_info("zoo", LEVEL2)
                if sentosa.checkForInput(MENU_MOUSE_POS):
                    show_info("sentosa", LEVEL3)
                if bukit.checkForInput(MENU_MOUSE_POS):
                    show_info("bukit", LEVEL4)
                if punggol.checkForInput(MENU_MOUSE_POS):
                    show_info("punggol", LEVEL5)
                if jurong.checkForInput(MENU_MOUSE_POS):
                    show_info("jurong", LEVEL6)
                if botanic.checkForInput(MENU_MOUSE_POS):
                    show_info("botanic", LEVEL7)

        SCREEN.fill("black")
        SCREEN.blit(map_img, (0, 0))

        sungei.changeColor(MENU_MOUSE_POS)
        zoo.changeColor(MENU_MOUSE_POS)
        sentosa.changeColor(MENU_MOUSE_POS)
        bukit.changeColor(MENU_MOUSE_POS)
        punggol.changeColor(MENU_MOUSE_POS)
        jurong.changeColor(MENU_MOUSE_POS)
        botanic.changeColor(MENU_MOUSE_POS)

        sungei.update(SCREEN)
        zoo.update(SCREEN)
        sentosa.update(SCREEN)
        bukit.update(SCREEN)
        punggol.update(SCREEN)
        jurong.update(SCREEN)
        botanic.update(SCREEN)

        def blit_label(label, mx, my):
            x = mx - label.get_width() // 2
            y = my + 24
            SCREEN.blit(label, (x, y))

        blit_label(label_sungei,  295, 230)
        blit_label(label_zoo,     520, 158)
        blit_label(label_sentosa, 621, 527)
        blit_label(label_bukit,   430, 280)
        blit_label(label_punggol, 620, 200)
        blit_label(label_jurong,  480, 380)
        blit_label(label_botanic, 500, 460)

        if CURSOR_IMG:
            mx, my = pygame.mouse.get_pos()
            SCREEN.blit(CURSOR_IMG, (mx - 25, my - 25))

        pygame.display.update()