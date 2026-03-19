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

# ---- Load images ----
def load_img(path, w, h):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (100, 180, 220), (0, 0, w, h))
        return surf

# ---- Fish data — mirroring your p5 setup ----
FISH_DATA = [
    {"path": "assets/fish1-trp.png",  "w": 80,  "h": 65,  "speed": 2.1, "y_start": 350},
    {"path": "assets/fish2-trp.webp", "w": 90,  "h": 70,  "speed": 1.9, "y_start": 420},
    {"path": "assets/fish3-trp.jpeg", "w": 75,  "h": 60,  "speed": 2.3, "y_start": 280},
    {"path": "assets/fish4-trp.webp", "w": 85,  "h": 68,  "speed": 2.0, "y_start": 490},
    {"path": "assets/fish5-trp.png",  "w": 70,  "h": 55,  "speed": 2.5, "y_start": 200},
    {"path": "assets/shark1-trp.png", "w": 120, "h": 80,  "speed": 2.5, "y_start": 320},
    {"path": "assets/turtle1-trp.png","w": 100, "h": 85,  "speed": 1.6, "y_start": 450},
]

FACTS = [
    "Sentosa abrite le parc marin des iles Sisters.",
    "Plus de 250 especes de coraux durs a proximite du recif.",
    "Le seul sanctuaire d'hippocampes de Singapour est ici.",
    "Le recif s'etend le long de toute la cote sud.",
    "Sentosa signifie 'paix et tranquillite' en malais.",
    "Les eaux de Sentosa abritent plus de 40 especes de coraux.",
    "Le parc marin protege une biodiversite marine exceptionnelle.",
    "Des raies manta ont ete observees dans les eaux de Sentosa.",
]

# ---- Swimming fish ----
class Fish:
    def __init__(self, img, img_flip, data, screen_w, screen_h):
        self.img       = img
        self.img_flip  = img_flip
        self.w         = data["w"]
        self.h         = data["h"]
        self.base_y    = data["y_start"] + random.randint(-30, 30)
        self.speed     = data["speed"] + random.uniform(-0.3, 0.3)
        self.screen_w  = screen_w
        self.screen_h  = screen_h
        # Start at random x, all going left like in p5
        self.x         = float(random.randint(0, screen_w))
        self.y         = float(self.base_y)
        self.wobble    = random.uniform(0, math.pi * 2)
        self.wobble_sp = random.uniform(0.02, 0.035)
        self.wobble_amp= random.uniform(8, 20)
        self.going_right = False  # default swim left like p5

    def update(self):
        # Swim left, wrap to right when off screen (like p5's swim())
        self.x -= self.speed
        if self.x < -self.w:
            self.x = float(self.screen_w + self.w)
            self.base_y = random.randint(120, self.screen_h - 100)

        self.wobble += self.wobble_sp
        self.y = self.base_y + math.sin(self.wobble) * self.wobble_amp

    def draw(self, screen):
        screen.blit(self.img_flip, (int(self.x) - self.w // 2,
                                    int(self.y) - self.h // 2))

# ---- Bubble ----
class Bubble:
    def __init__(self, x, screen_h):
        self.x       = x + random.randint(-10, 10)
        self.y       = float(screen_h)
        self.r       = random.randint(4, 12)
        self.speed   = random.uniform(0.8, 1.8)
        self.wobble  = random.uniform(0, math.pi * 2)
        self.wobble_sp = random.uniform(0.03, 0.06)
        self.alpha   = random.randint(140, 220)

    def update(self):
        self.y      -= self.speed
        self.wobble += self.wobble_sp
        self.x      += math.sin(self.wobble) * 0.8

    def draw(self, screen):
        surf = pygame.Surface((self.r * 2 + 4, self.r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 230, 255, self.alpha),
                           (self.r + 2, self.r + 2), self.r)
        pygame.draw.circle(surf, (255, 255, 255, min(255, self.alpha + 40)),
                           (self.r + 2, self.r + 2), self.r, 2)
        screen.blit(surf, (int(self.x) - self.r - 2, int(self.y) - self.r - 2))

    @property
    def alive(self):
        return self.y > -20

# ---- Coral decorations drawn at top ----
def draw_coral_strip(screen, W, coral_imgs):
    # Tile coral images across the top like p5's deco()
    for i, img in enumerate(coral_imgs):
        screen.blit(img, (i * (W // len(coral_imgs)), 0))

# ---- Fact card (same as Punggol) ----
class FactCard:
    def __init__(self, text, screen_w, screen_h, font):
        self.text      = text
        self.font      = font
        self.screen_w  = screen_w
        self.screen_h  = screen_h
        self.alpha     = 0
        self.state     = "fadein"
        self.timer     = 0
        self.hold_time = 220
        self.fade_speed = 4
        self.alive     = True
        self.x = random.randint(60, screen_w - 460)
        self.y = random.randint(screen_h - 200, screen_h - 90)
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
        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        panel.fill((0, 30, 80, min(200, self.alpha)))
        screen.blit(panel, (self.x, self.y))
        pygame.draw.rect(screen, (0, 151, 178, min(240, self.alpha)),
                         (self.x, self.y, self.w, self.h), 2, border_radius=6)

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

# ---- Background ----
def draw_water(screen, W, H, frame):
    # Deep blue water
    screen.fill((10, 60, 120))

    # Light rays from top
    for i in range(5):
        ray_x = (W // 6) * (i + 1) + int(math.sin(frame * 0.01 + i) * 20)
        ray_surf = pygame.Surface((60, H), pygame.SRCALPHA)
        for y in range(H):
            alpha = max(0, 18 - y // 30)
            pygame.draw.line(ray_surf, (180, 220, 255, alpha), (30, y), (30, y))
        screen.blit(ray_surf, (ray_x - 30, 0))

    # Sandy bottom
    pygame.draw.rect(screen, (180, 150, 80), (0, H - 55, W, 55))
    pygame.draw.rect(screen, (200, 170, 100), (0, H - 55, W, 10))

    # Seaweed
    for sx, sh, sc in SEAWEED:
        for seg in range(sh // 12):
            wx = sx + int(math.sin(frame * 0.04 + seg * 0.5) * 6)
            wy = H - 55 - seg * 12
            pygame.draw.circle(screen, sc, (wx, wy), 5)

# ---- LEVEL3 ----
def LEVEL3():
    clock  = pygame.time.Clock()
    W, H   = SCREEN.get_width(), SCREEN.get_height()

    font_title  = get_font(22)
    font_facts  = get_font_facts(18)
    font_hint   = get_font(14)

    global SEAWEED
    SEAWEED = [
        (random.randint(0, W), random.randint(40, 90),
         (random.randint(20, 80), random.randint(120, 60+80), random.randint(20, 60)))
        for _ in range(18)
    ]

    # Load fish images + flipped versions (fish swim left so we flip horizontally)
    fish_list = []
    for data in FISH_DATA:
        img      = load_img(data["path"], data["w"], data["h"])
        img_flip = pygame.transform.flip(img, True, False)
        fish_list.append(Fish(img, img_flip, data, W, H))


    # Bubbles — two columns like p5's deco()
    bubbles      = []
    bubble_timer = 0

    facts       = random.sample(FACTS, len(FACTS))
    fact_index  = 0
    fact_cards  = []
    fact_timer  = 0
    FACT_INTERVAL = 280

    frame = 0

    while True:
        clock.tick(60)
        frame      += 1
        fact_timer += 1
        bubble_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # Spawn bubbles on left and right sides like p5
        if bubble_timer % 8 == 0:
            bubbles.append(Bubble(10,   H))
            bubbles.append(Bubble(W-10, H))

        # Spawn fact card
        if fact_timer >= FACT_INTERVAL:
            fact_timer = 0
            fact_cards.append(FactCard(facts[fact_index % len(facts)], W, H, font_facts))
            fact_index += 1

        # Update
        for f in fish_list:
            f.update()
        for b in bubbles:
            b.update()
        bubbles = [b for b in bubbles if b.alive]
        for fc in fact_cards:
            fc.update()
        fact_cards = [fc for fc in fact_cards if fc.alive]

        # ---- Draw ----
        draw_water(SCREEN, W, H, frame)


        for b in bubbles:
            b.draw(SCREEN)
        for f in fish_list:
            f.draw(SCREEN)
        for fc in fact_cards:
            fc.draw(SCREEN)

        # Title
        title = font_title.render("Recif de Sentosa Serapong", True, (0, 220, 255))
        SCREEN.blit(title, (W // 2 - title.get_width() // 2, H - 40))

        # ESC hint
        SCREEN.blit(font_hint.render("ECHAP = retour", True, (150, 200, 220)), (20, 18))

        pygame.display.update()