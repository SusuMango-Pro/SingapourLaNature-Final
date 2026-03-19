import pygame
import sys
import random

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

# ---- Level config: each level introduces one animal, faster + more of them ----
LEVELS = [
    {"animal": "assets/mosqui-trp.png",  "name": "Moustique", "w": 70,  "h": 70,  "count": 3, "speed": 3.5, "threshold": 0},
    {"animal": "assets/serpent-trp.png", "name": "Serpent",   "w": 80,  "h": 80,  "count": 4, "speed": 5.0, "threshold": 15},
    {"animal": "assets/eagle-trp.png",   "name": "Aigle",     "w": 80,  "h": 80,  "count": 5, "speed": 6.5, "threshold": 30},
    {"animal": "assets/boar2-trp.png",   "name": "Sanglier",  "w": 90,  "h": 70,  "count": 6, "speed": 8.0, "threshold": 50},
    {"animal": "assets/croc-trp.png",    "name": "Crocodile", "w": 100, "h": 60,  "count": 8, "speed": 10.0,"threshold": 75},
]

def load_image(path, w, h):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except Exception:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 0, 0), (0, 0, w, h), border_radius=8)
        return surf

def get_level(score):
    current = 0
    for i, lv in enumerate(LEVELS):
        if score >= lv["threshold"]:
            current = i
    return current

# ---- Falling danger ----
class Danger:
    def __init__(self, img, w, h, speed, screen_w, screen_h):
        self.img      = img
        self.w        = w
        self.h        = h
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.speed    = speed
        self.scored   = False
        self._place_top()

    def _place_top(self):
        self.x = random.randint(0, self.screen_w - self.w)
        self.y = random.randint(-400, -self.h)
        self.scored = False

    def update(self):
        self.y += self.speed
        if self.y > self.screen_h:
            self._place_top()
            return True   # signal: passed bottom = +1 score
        return False

    def draw(self, screen):
        screen.blit(self.img, (int(self.x), int(self.y)))

    def get_rect(self):
        margin = 12
        return pygame.Rect(int(self.x) + margin, int(self.y) + margin,
                           self.w - margin * 2, self.h - margin * 2)

# ---- LEVEL4 ----
def LEVEL4():
    clock  = pygame.time.Clock()
    W, H   = SCREEN.get_width(), SCREEN.get_height()

    font_big   = get_font(36)
    font_med   = get_font(24)
    font_small = get_font(16)

    # Pre-load all animal images
    level_imgs = [load_image(lv["animal"], lv["w"], lv["h"]) for lv in LEVELS]

    # Player sprite (bird placeholder — swap for monkey)
    try:
        player_raw = pygame.image.load("assets/SpriteJump/Bird1.png").convert_alpha()
        player_img = pygame.transform.scale(player_raw, (60, 60))
    except Exception:
        player_img = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(player_img, (180, 100, 20), (30, 30), 30)

    PW, PH = 60, 60
    GROUND_Y = H - 80   # player walks along the bottom

    pygame.mouse.set_visible(False)

    def build_dangers(level_idx):
        lv    = LEVELS[level_idx]
        img   = level_imgs[level_idx]
        return [Danger(img, lv["w"], lv["h"], lv["speed"], W, H)
                for _ in range(lv["count"])]

    # ---- Game state ----
    def reset():
        return {
            "score":      0,
            "high_score": 0,
            "level_idx":  0,
            "player_x":   W // 2,
            "dangers":    build_dangers(0),
            "game_over":  False,
            "speed":      4,
        }

    state      = reset()
    high_score = 0   # persists across restarts

    PLAYER_SPEED = 6

    while True:
        clock.tick(60)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state["game_over"]:
                    hs = max(high_score, state["score"])
                    state = reset()
                    state["high_score"] = hs
                    high_score = hs

        if not state["game_over"]:
            # ---- Move player with arrow keys ----
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                state["player_x"] = max(PW // 2, state["player_x"] - PLAYER_SPEED)
            if keys[pygame.K_RIGHT]:
                state["player_x"] = min(W - PW // 2, state["player_x"] + PLAYER_SPEED)

            # ---- Check if level should change ----
            new_level = get_level(state["score"])
            if new_level != state["level_idx"]:
                state["level_idx"] = new_level
                state["dangers"]   = build_dangers(new_level)

            # ---- Update dangers ----
            for d in state["dangers"]:
                passed = d.update()
                if passed:
                    state["score"] += 1
                    if state["score"] > high_score:
                        high_score = state["score"]

            # ---- Collision ----
            player_rect = pygame.Rect(
                state["player_x"] - PW // 2 + 10,
                GROUND_Y - PH + 10,
                PW - 20, PH - 20
            )
            for d in state["dangers"]:
                if player_rect.colliderect(d.get_rect()):
                    state["game_over"] = True
                    if state["score"] > high_score:
                        high_score = state["score"]

        # ---- Draw ----
        SCREEN.fill((34, 85, 34))
        for i in range(0, W, 120):
            pygame.draw.rect(SCREEN, (30, 75, 30), (i, 0, 40, H))

        # Ground bar
        pygame.draw.rect(SCREEN, (101, 67, 33), (0, GROUND_Y, W, H - GROUND_Y))

        for d in state["dangers"]:
            d.draw(SCREEN)

        # Draw player at bottom, centered on player_x
        SCREEN.blit(player_img, (state["player_x"] - PW // 2, GROUND_Y - PH))

        # Draw cursor sprite at mouse pos everywhere
        SCREEN.blit(player_img, (mouse_x - PW // 2, mouse_y - PH // 2))

        # ---- HUD ----
        pygame.draw.rect(SCREEN, (0, 0, 0), (10, 10, 280, 90), border_radius=10)
        SCREEN.blit(font_med.render(f"Score : {state['score']}", True, (255, 255, 255)), (20, 15))
        SCREEN.blit(font_med.render(f"Meilleur : {high_score}",  True, (255, 220, 80)),  (20, 45))

        lv    = LEVELS[state["level_idx"]]
        label = font_small.render(
            f"Niveau {state['level_idx'] + 1} — {lv['name']}",
            True, (200, 255, 200)
        )
        SCREEN.blit(label, (W // 2 - label.get_width() // 2, 15))

        # Next level progress bar
        curr_lv   = state["level_idx"]
        next_lv   = curr_lv + 1
        if next_lv < len(LEVELS):
            curr_thresh = LEVELS[curr_lv]["threshold"]
            next_thresh = LEVELS[next_lv]["threshold"]
            progress    = (state["score"] - curr_thresh) / (next_thresh - curr_thresh)
            progress    = max(0, min(1, progress))
            bar_w       = 300
            pygame.draw.rect(SCREEN, (60, 60, 60),   (W // 2 - bar_w // 2, 45, bar_w, 16), border_radius=8)
            pygame.draw.rect(SCREEN, (100, 220, 100), (W // 2 - bar_w // 2, 45, int(bar_w * progress), 16), border_radius=8)
            next_label = font_small.render(f"Prochain niveau a {next_thresh} pts", True, (180, 180, 180))
            SCREEN.blit(next_label, (W // 2 - next_label.get_width() // 2, 64))
        else:
            SCREEN.blit(font_small.render("Niveau MAX !", True, (255, 215, 0)),
                        (W // 2 - 70, 45))

        SCREEN.blit(font_small.render("ECHAP = retour", True, (180, 180, 180)), (W - 200, 15))

        # ---- Game Over overlay ----
        if state["game_over"]:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            SCREEN.blit(overlay, (0, 0))
            SCREEN.blit(font_big.render("GAME OVER !",         True, (255, 50,  50)),  (W//2 - 170, H//2 - 90))
            SCREEN.blit(font_med.render(f"Score : {state['score']}", True, (255, 255, 255)), (W//2 - 110, H//2 - 20))
            SCREEN.blit(font_med.render(f"Meilleur : {high_score}",  True, (255, 220, 80)),  (W//2 - 120, H//2 + 30))
            SCREEN.blit(font_med.render("Clic pour rejouer  |  ECHAP = carte", True, (200, 200, 200)), (W//2 - 240, H//2 + 90))

        pygame.display.update()