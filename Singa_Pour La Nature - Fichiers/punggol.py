import pygame
import sys
import random
import math

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

def get_font_facts(size):
    return pygame.font.SysFont("timesnewroman", size)

# ---- Load animal images ----
def load_img(path, w, h):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (100, 180, 100), (0, 0, w, h))
        return surf

# ---- Facts about Punggol ----
FACTS = [
    "La voie navigable de Punggol est la premiere voie ecologique de Singapour.",
    "Elle s'etend sur 4,2 km a travers le quartier de Punggol.",
    "Les loutres a pelage lisse s'y sont installes depuis 2018.",
    "La voie relie le reservoir de Serangoon a celui de Punggol.",
    "Plus de 80 especes d'oiseaux ont ete observees le long de la voie.",
    "Le serpent d'eau a museau de chien est natif des voies navigables de Singapour.",
    "Punggol signifie 'lancer un baton sur des fruits' en malais.",
    "Le parc de la voie navigable a ouvert en 2011 sur 100 hectares.",
]

# ---- Ripple effect ----
class Ripple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.max_r  = random.randint(20, 45)
        self.alpha  = 200
        self.speed  = random.uniform(0.4, 0.8)
        self.alive  = True

    def update(self):
        self.radius += self.speed
        self.alpha   = int(200 * (1 - self.radius / self.max_r))
        if self.radius >= self.max_r:
            self.alive = False

    def draw(self, screen):
        surf = pygame.Surface((self.max_r * 2 + 4, self.max_r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, max(0, self.alpha)),
                           (self.max_r + 2, self.max_r + 2), int(self.radius), 2)
        screen.blit(surf, (int(self.x) - self.max_r - 2, int(self.y) - self.max_r - 2))

# ---- Animal swimming ----
class SwimmingAnimal:
    def __init__(self, img, img_flip, name, screen_w, screen_h, river_top, river_bot):
        self.img       = img
        self.img_flip  = img_flip
        self.name      = name
        self.screen_w  = screen_w
        self.river_top = river_top
        self.river_bot = river_bot
        self.ripple_timer = 0
        self.ripples      = []
        self._spawn()

    def _spawn(self):
        # Randomly come from left or right
        self.going_right = random.choice([True, False])
        if self.going_right:
            self.x = -120
        else:
            self.x = self.screen_w + 120
        self.y      = random.randint(self.river_top + 40, self.river_bot - 40)
        self.speed  = random.uniform(1.2, 2.5)
        self.wobble = 0   # vertical sine wobble
        self.wobble_speed = random.uniform(0.02, 0.04)
        self.wobble_amp   = random.uniform(6, 18)
        self.base_y = self.y

    def update(self):
        if self.going_right:
            self.x += self.speed
        else:
            self.x -= self.speed

        self.wobble += self.wobble_speed
        self.y = self.base_y + math.sin(self.wobble) * self.wobble_amp

        # Ripple trail
        self.ripple_timer += 1
        if self.ripple_timer >= 30:
            self.ripples.append(Ripple(self.x, self.y))
            self.ripple_timer = 0

        for r in self.ripples:
            r.update()
        self.ripples = [r for r in self.ripples if r.alive]

        # Respawn when off screen
        if self.going_right and self.x > self.screen_w + 150:
            self._spawn()
        elif not self.going_right and self.x < -150:
            self._spawn()

    def draw(self, screen):
        for r in self.ripples:
            r.draw(screen)
        img = self.img if self.going_right else self.img_flip
        w, h = img.get_width(), img.get_height()
        screen.blit(img, (int(self.x) - w // 2, int(self.y) - h // 2))

# ---- Floating fact card ----
class FactCard:
    def __init__(self, text, screen_w, screen_h, font):
        self.text      = text
        self.font      = font
        self.screen_w  = screen_w
        self.screen_h  = screen_h
        self.alpha     = 0
        self.state     = "fadein"   # fadein, hold, fadeout, dead
        self.timer     = 0
        self.hold_time = 220        # frames to hold
        self.fade_speed = 4
        self.alive     = True
        # Random position in lower third
        self.x = random.randint(60, screen_w - 460)
        self.y = random.randint(screen_h - 200, screen_h - 80)
        self.w = 420
        self.h = 70

    def update(self):
        if self.state == "fadein":
            self.alpha = min(240, self.alpha + self.fade_speed)
            if self.alpha >= 240:
                self.state = "hold"
        elif self.state == "hold":
            self.timer += 1
            if self.timer >= self.hold_time:
                self.state = "fadeout"
        elif self.state == "fadeout":
            self.alpha = max(0, self.alpha - self.fade_speed)
            if self.alpha == 0:
                self.alive = False

    def draw(self, screen):
        # Panel
        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        panel.fill((0, 30, 60, min(200, self.alpha)))
        screen.blit(panel, (self.x, self.y))
        pygame.draw.rect(screen, (0, 151, 178, min(240, self.alpha)),
                         (self.x, self.y, self.w, self.h), 2, border_radius=6)

        # Wrap text
        words = self.text.split()
        lines, line = [], ""
        for w in words:
            test = line + " " + w if line else w
            if self.font.size(test)[0] < self.w - 20:
                line = test
            else:
                lines.append(line)
                line = w
        lines.append(line)

        for i, l in enumerate(lines):
            surf = self.font.render(l, True, (220, 240, 255))
            surf.set_alpha(min(255, self.alpha))
            screen.blit(surf, (self.x + 10, self.y + 8 + i * 26))

# ---- Draw water ----
def draw_water(screen, W, H, river_top, river_bot, frame):
    # Main water body
    water_surf = pygame.Surface((W, river_bot - river_top), pygame.SRCALPHA)
    water_surf.fill((0, 105, 148, 210))
    screen.blit(water_surf, (0, river_top))

    # Animated shimmer lines
    for i in range(8):
        offset = (frame * 1.2 + i * 90) % W
        y = river_top + 40 + i * ((river_bot - river_top - 80) // 8)
        length = random.randint(40, 120) if frame % 4 == 0 else 80
        pygame.draw.line(screen, (180, 230, 255, 80),
                         (int(offset), y), (int(offset) + length, y), 2)

    # Banks (grass edges)
    pygame.draw.rect(screen, (60, 130, 60),  (0, 0, W, river_top))
    pygame.draw.rect(screen, (60, 130, 60),  (0, river_bot, W, H - river_bot))

    # Bank detail — darker strip right at water edge
    pygame.draw.rect(screen, (40, 100, 40), (0, river_top - 12, W, 12))
    pygame.draw.rect(screen, (40, 100, 40), (0, river_bot,      W, 12))

    # Lily pads
    for lp in LILY_PADS:
        pygame.draw.ellipse(screen, (34, 110, 34), lp)
        pygame.draw.ellipse(screen, (50, 140, 50), lp, 2)

def draw_bank_details(screen, W, river_top, river_bot, frame):
    # Grass tufts on banks
    for gx, gy, gh in GRASS_TUFTS:
        pygame.draw.line(screen, (80, 160, 60), (gx, gy), (gx - 4, gy - gh), 2)
        pygame.draw.line(screen, (80, 160, 60), (gx, gy), (gx,     gy - gh), 2)
        pygame.draw.line(screen, (80, 160, 60), (gx, gy), (gx + 4, gy - gh), 2)

# ---- LEVEL5 ----
def LEVEL5():
    clock  = pygame.time.Clock()
    W, H   = SCREEN.get_width(), SCREEN.get_height()

    font_title  = get_font(22)
    font_facts  = get_font_facts(18)
    font_hint   = get_font(14)

    river_top = 160
    river_bot = 560

    # Generate static scenery once
    global LILY_PADS, GRASS_TUFTS
    LILY_PADS = [
        pygame.Rect(random.randint(20, W-60), random.randint(river_top+20, river_bot-40), 
                    random.randint(30, 55), random.randint(18, 32))
        for _ in range(12)
    ]
    GRASS_TUFTS = [
        (random.randint(0, W), 
         random.randint(river_top - 60, river_top - 5) if i < 20 else random.randint(river_bot + 5, river_bot + 55),
         random.randint(12, 28))
        for i in range(40)
    ]

    # Load animals
    otter_img = load_img("assets/otter-trp.png", 100, 90)
    snake_img = load_img("assets/watersnake-trp.png", 90, 90)
    otter_flip = pygame.transform.flip(otter_img, True, False)
    snake_flip  = pygame.transform.flip(snake_img, True, False)

    animals = [
        SwimmingAnimal(otter_img, otter_flip, "Loutre",        W, H, river_top, river_bot),
        SwimmingAnimal(otter_img, otter_flip, "Loutre",        W, H, river_top, river_bot),
        SwimmingAnimal(snake_img, snake_flip,  "Serpent d'eau", W, H, river_top, river_bot),
    ]
    # Stagger starting positions
    animals[1].x = W // 2
    animals[1].base_y = random.randint(river_top + 40, river_bot - 40)

    facts        = random.sample(FACTS, len(FACTS))
    fact_index   = 0
    fact_cards   = []
    fact_timer   = 0
    FACT_INTERVAL = 280   # frames between new facts

    frame = 0

    while True:
        clock.tick(60)
        frame += 1
        fact_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # Spawn new fact card
        if fact_timer >= FACT_INTERVAL:
            fact_timer = 0
            text = facts[fact_index % len(facts)]
            fact_index += 1
            fact_cards.append(FactCard(text, W, H, font_facts))

        # Update
        for a in animals:
            a.update()
        for fc in fact_cards:
            fc.update()
        fact_cards = [fc for fc in fact_cards if fc.alive]

        # ---- Draw ----
        SCREEN.fill((60, 130, 60))   # grass base colour
        draw_water(SCREEN, W, H, river_top, river_bot, frame)
        draw_bank_details(SCREEN, W, river_top, river_bot, frame)

        for a in animals:
            a.draw(SCREEN)

        for fc in fact_cards:
            fc.draw(SCREEN)

        title = font_title.render("Voie navigable de Punggol", True, (0, 151, 178))
        SCREEN.blit(title, (W // 2 - title.get_width() // 2, 18))

        SCREEN.blit(font_hint.render("ECHAP = retour", True, (180, 220, 180)), (20, 18))

        pygame.display.update()