import pygame
import sys
from button import Button

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

try:
    CURSOR_IMG = pygame.transform.scale(
        pygame.image.load("assets/SpriteJump/Bird1.png").convert_alpha(), (50, 50)
    )
except:
    CURSOR_IMG = None

def get_font_info(size, bold=False):
    return pygame.font.SysFont("timesnewroman", size, bold=bold)

def get_font_button(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

LOCATION_DATA = {
    "sungei": {
        "name": "Reserve de zones humides de Sungei Buloh",
        "image": "assets/sungei_info.jpg",
        "facts": [
            "Premier parc du patrimoine de l'ASEAN a Singapour.",
            "Refuge pour les oiseaux migrateurs de Siberie et de Chine.",
            "Plus de 140 especes d'oiseaux recensees ici.",
            "Des crocodiles marins vivent dans ses cours d'eau.",
            "Couvre 202 hectares de zones humides de mangroves.",
        ],
    },
    "zoo": {
        "name": "Zoo de Singapour",
        "image": "assets/zoo_info.jpg",
        "facts": [
            "Ouvert en 1973 sur les rives du lac Mandai.",
            "Abrite plus de 2 400 animaux de 300 especes.",
            "Celebre pour ses enclos ouverts sans barreaux.",
            "Fait partie du complexe Mandai Wildlife Reserve.",
            "L'un des meilleurs zoos au monde.",
        ],
    },
    
    "bukit": {
        "name": "Reserve naturelle de Bukit Timah",
        "image": "assets/bukit_info.jpg",
        "facts": [
            "Point culminant de Singapour a 163,63 metres.",
            "L'une des forets les plus riches en especes au monde.",
            "Plus d'especes d'arbres qu'en Amerique du Nord entiere.",
            "Sangliers, pythons et aigles y vivent en liberte.",
            "Couvre 163 hectares de foret tropicale primaire.",
        ],
    },
    "punggol": {
        "name": "Voie navigable de Punggol",
        "image": "assets/punggol_info.jpg",
        "facts": [
            "Premiere voie navigable ecologique de Singapour.",
            "S'etend sur 4,2 km a travers le quartier de Punggol.",
            "Les loutres a pelage lisse s'y sont installes en 2018.",
            "Plus de 80 especes d'oiseaux observees sur les berges.",
            "Relie le reservoir de Serangoon a celui de Punggol.",
        ],
    },
    "jurong": {
        "name": "Jurong Bird Park",
        "image": "assets/jurong_info.jpg",
        "facts": [
            "L'un des plus grands parcs ornithologiques d'Asie.",
            "Abrite plus de 3 500 oiseaux de 400 especes.",
            "Ouvert en 1971 sur les pentes de la colline de Jurong.",
            "Celebre pour sa voliere de la foret tropicale humide.",
            "Desormais integre au complexe Mandai Wildlife Reserve.",
        ],
    },
    "botanic": {
        "name": "Jardins botaniques de Singapour",
        "image": "assets/botanic_info.jpg",
        "facts": [
            "Premier site du patrimoine mondial de l'UNESCO a Singapour.",
            "Fonde en 1859, l'un des plus anciens jardins tropicaux.",
            "Abrite plus de 10 000 especes de plantes et d'orchidees.",
            "Le National Orchid Garden compte 1 000 especes d'orchidees.",
            "Couvre 74 hectares en plein coeur de Singapour.",
        ],
    },
    "sentosa": {
        "name": "Recif de Sentosa Serapong",
        "image": "assets/sentosa_info.jpg",
        "facts": [
            "Sentosa signifie 'paix et tranquillite' en malais.",
            "Abrite le parc marin des iles Sisters.",
            "Plus de 250 especes de coraux durs a proximite.",
            "Le seul sanctuaire d'hippocampes de Singapour.",
            "Le recif s'etend le long de la cote sud.",
        ],
    },
    
}

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def show_info(location_key, game_func):
    data = LOCATION_DATA[location_key]

    title_font = get_font_info(32, bold=True)
    fact_font  = get_font_info(22)
    small_font = get_font_info(17)

    try:
        location_img = pygame.image.load(data["image"]).convert()
        location_img = pygame.transform.scale(location_img, (420, 280))
        has_img = True
    except Exception:
        has_img = False

    PLAY_BUTTON = Button(
        image=pygame.image.load("assets/mainmenubutton.png"),
        pos=(960, 580),
        text_input="JOUER",
        font=get_font_button(32),
        base_color="#18af0dc1",
        hovering_color="White"
    )
    BACK_BUTTON = Button(
        image=pygame.image.load("assets/mainmenubutton.png"),
        pos=(320, 580),
        text_input="RETOUR",
        font=get_font_button(32),
        base_color="#18af0dc1",
        hovering_color="White"
    )

    clock = pygame.time.Clock()
    bg = pygame.image.load("assets/SgMapBlurred.png")

    while True:
        clock.tick(60)
        MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    game_func()
                    return
                if BACK_BUTTON.checkForInput(MOUSE_POS):
                    return

        SCREEN.blit(bg, (0, 0))

        panel = pygame.Surface((1200, 480), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 160))
        SCREEN.blit(panel, (40, 40))

        if has_img:
            SCREEN.blit(location_img, (60, 100))
        else:
            pygame.draw.rect(SCREEN, (30, 80, 50), (60, 100, 420, 280))
            no_img = small_font.render("[ Aucune image trouvee ]", True, (200, 200, 200))
            SCREEN.blit(no_img, (160, 230))

        title_surf = title_font.render(data["name"], True, (255, 255, 255))
        SCREEN.blit(title_surf, (510, 80))

        y = 145
        for fact in data["facts"]:
            bullet = f"•  {fact}"
            lines = wrap_text(bullet, fact_font, 680)
            for line in lines:
                SCREEN.blit(fact_font.render(line, True, (220, 255, 200)), (510, y))
                y += 32
            y += 8

        PLAY_BUTTON.changeColor(MOUSE_POS)
        BACK_BUTTON.changeColor(MOUSE_POS)
        PLAY_BUTTON.update(SCREEN)
        BACK_BUTTON.update(SCREEN)

        if CURSOR_IMG:
            mx, my = pygame.mouse.get_pos()
            SCREEN.blit(CURSOR_IMG, (mx - 25, my - 25))

        pygame.display.update()