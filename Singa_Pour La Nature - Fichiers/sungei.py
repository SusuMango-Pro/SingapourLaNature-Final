import pygame
import sys
import random
import math

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Sungei Buloh - Jeu de canons")

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

# ---- Helpers ----
def make_stars(n, w, h):
    return [{"x": random.randint(0, w-1), "y": random.randint(0, h-1), "r": random.randint(1, 3)} for _ in range(n)]

def draw_stars(screen, stars):
    for s in stars:
        pygame.draw.circle(screen, (250, 250, 210), (s["x"], s["y"]), s["r"])

def clamp_angle(a):
    while a < -180: a += 360
    while a >  180: a -= 360
    return a

# ---- Load all existing animals ----
def load_img(path, w, h):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 50, 50), (0, 0, w, h), border_radius=8)
        return surf

ANIMALS = [
    {"path": "assets/serpent-trp.png",   "name": "Serpent",        "w": 80,  "h": 80},
    {"path": "assets/mosqui-trp.png",    "name": "Moustique",      "w": 70,  "h": 70},
    {"path": "assets/croc-trp.png",      "name": "Crocodile",      "w": 100, "h": 60},
    {"path": "assets/eagle-trp.png",     "name": "Aigle",          "w": 80,  "h": 80},
    {"path": "assets/boar2-trp.png",     "name": "Sanglier",       "w": 90,  "h": 70},
    {"path": "assets/otter-trp.png",     "name": "Loutre",         "w": 80,  "h": 80},
    {"path": "assets/watersnake-trp.png","name": "Serpent d'eau",  "w": 80,  "h": 80},
]

# ---- Bullet ----
class Bullet:
    SPEED  = 14
    LENGTH = 18

    def __init__(self, x, y, angle_deg, color):
        rad      = math.radians(angle_deg)
        self.dx  = math.cos(rad) * self.SPEED
        self.dy  = math.sin(rad) * self.SPEED
        self.x   = float(x)
        self.y   = float(y)
        self.color = color
        self.alive = True

    def update(self, w, h):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > w or self.y < 0 or self.y > h:
            self.alive = False

    def draw(self, screen):
        tail_x = self.x - self.dx * (self.LENGTH / self.SPEED)
        tail_y = self.y - self.dy * (self.LENGTH / self.SPEED)
        pygame.draw.line(screen, self.color,
                         (int(tail_x), int(tail_y)), (int(self.x), int(self.y)), 4)

    def hits(self, target):
        fx, fy = target.x - self.x, target.y - self.y
        return math.sqrt(fx*fx + fy*fy) < target.r

# ---- Cannon ----
class Cannon:
    FIRE_COOLDOWN = 10

    def __init__(self, x, ground_h, w, h, color, left_key, right_key, shoot_key):
        self.x         = x
        self.ground_h  = ground_h
        self.w         = w
        self.h         = h
        self.color     = color
        self.angle     = -90
        self.left_key  = left_key
        self.right_key = right_key
        self.shoot_key = shoot_key
        self.shooting  = False
        self.fire_timer = 0
        self.bullet_color = tuple(min(255, c + 80) for c in color)

    def aim(self, keys):
        if keys[self.left_key]:  self.angle += 1.5
        if keys[self.right_key]: self.angle -= 1.5
        self.angle = clamp_angle(self.angle)

    def update(self, keys, bullets):
        self.shooting = keys[self.shoot_key]
        self.fire_timer = max(0, self.fire_timer - 1)
        if self.shooting and self.fire_timer == 0:
            ex, ey = self.barrel_end()
            bullets.append(Bullet(ex, ey, self.angle, self.bullet_color))
            self.fire_timer = self.FIRE_COOLDOWN

    def base_pos(self):
        return self.x + self.w // 2, self.ground_h + self.h

    def barrel_end(self):
        bx, by = self.base_pos()
        rad = math.radians(self.angle)
        return bx + int(math.cos(rad) * self.w // 2), by + int(math.sin(rad) * self.w // 2)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.ground_h, self.w, self.h), border_radius=6)
        bx, by = self.base_pos()
        pygame.draw.circle(screen, self.color, (bx, by), self.w // 2)
        ex, ey = self.barrel_end()
        pygame.draw.line(screen, (240, 255, 255), (bx, by), (ex, ey), 10)

    def check_hit(self, target):
        if not self.shooting:
            return False
        bx, by = self.base_pos()
        rad = math.radians(self.angle)
        dx, dy = math.cos(rad), math.sin(rad)
        fx, fy = target.x - bx, target.y - by
        proj = fx * dx + fy * dy
        if proj < 0:
            return False
        cx = bx + dx * proj - target.x
        cy = by + dy * proj - target.y
        return math.sqrt(cx*cx + cy*cy) < target.r

# ---- Moving Animal Target ----
class Target:
    def __init__(self, animal_data, img, screen_w, screen_h, ground_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.ground_h = ground_h
        self.name     = animal_data["name"]
        self.img      = img
        self.w        = animal_data["w"]
        self.h        = animal_data["h"]
        self.r        = max(self.w, self.h) // 2 - 8
        self.alive    = True
        self._place()

    def _place(self):
        self.x    = float(random.randint(150, self.screen_w - 150))
        self.y    = float(random.randint(self.ground_h + 80, self.screen_h - 80))
        speed     = random.uniform(1.5, 3.2)
        angle     = random.uniform(0, 2 * math.pi)
        self.vx   = math.cos(angle) * speed
        self.vy   = math.sin(angle) * speed

    def respawn(self):
        self.alive = True
        self._place()

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r < 0:
            self.x = self.r;                      self.vx *= -1
        if self.x + self.r > self.screen_w:
            self.x = self.screen_w - self.r;      self.vx *= -1
        if self.y - self.r < self.ground_h + 5:
            self.y = self.ground_h + self.r + 5;  self.vy *= -1
        if self.y + self.r > self.screen_h:
            self.y = self.screen_h - self.r;      self.vy *= -1

    def draw(self, screen, font):
        cx, cy = int(self.x) - self.w // 2, int(self.y) - self.h // 2
        screen.blit(self.img, (cx, cy))
        label = font.render(self.name, True, (255, 255, 255))
        # Small dark shadow for legibility
        shadow = font.render(self.name, True, (0, 0, 0))
        screen.blit(shadow, (int(self.x) - label.get_width() // 2 + 1,
                             int(self.y) + self.h // 2 + 5))
        screen.blit(label,  (int(self.x) - label.get_width() // 2,
                             int(self.y) + self.h // 2 + 4))

# ---- Background: mangrove swamp feel ----
def draw_background(screen, W, H, ground_h, frame):
    # Sky — warm tropical
    screen.fill((135, 195, 135))

    # Water/mud strip at bottom
    pygame.draw.rect(screen, (101, 80, 50), (0, H - 60, W, 60))

    # Ground bar (top)
    pygame.draw.rect(screen, (60, 100, 50), (0, 0, W, ground_h))

    # Simple mangrove tree silhouettes on the sides
    for tx, ty, th in MANGROVES:
        pygame.draw.rect(screen, (30, 60, 30), (tx, ty, 18, th))
        pygame.draw.circle(screen, (40, 80, 40), (tx + 9, ty), 28)

# ---- LEVEL1 (formerly LEVEL3 / Sentosa) ----
def LEVEL1():
    clock      = pygame.time.Clock()
    W, H       = SCREEN.get_width(), SCREEN.get_height()
    ground_h   = 10
    font_sm    = get_font(13)
    font_md    = get_font(24)
    font_label = get_font(11)

    global MANGROVES
    MANGROVES = [(random.randint(80, 200), random.randint(80, H - 150),
                  random.randint(60, 140)) for _ in range(6)] + \
                [(random.randint(W - 220, W - 80), random.randint(80, H - 150),
                  random.randint(60, 140)) for _ in range(6)]

    # Load all animal images
    loaded = [(a, load_img(a["path"], a["w"], a["h"])) for a in ANIMALS]

    # Build targets — one per animal type, shuffled
    random.shuffle(loaded)
    targets = [Target(a, img, W, H, ground_h) for a, img in loaded]

    c1 = Cannon(25,   ground_h, 50, 75, (180, 60, 20),
                pygame.K_a, pygame.K_d, pygame.K_w)
    c2 = Cannon(W-75, ground_h, 50, 75, (20, 80, 160),
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

    bullets     = []
    score       = 0
    hit_cooldown = 0
    frame_count  = 0

    while True:
        clock.tick(60)
        frame_count  += 1
        hit_cooldown  = max(0, hit_cooldown - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        c1.aim(keys)
        c2.aim(keys)
        c1.update(keys, bullets)
        c2.update(keys, bullets)

        for b in bullets:
            b.update(W, H)
        bullets = [b for b in bullets if b.alive]

        for t in targets:
            t.update()

        # Bullet-target collision
        for b in bullets:
            for t in targets:
                if t.alive and b.alive and b.hits(t):
                    t.alive = False
                    b.alive = False
                    score  += 10

        for t in targets:
            if not t.alive:
                t.respawn()

        # ---- Draw ----
        draw_background(SCREEN, W, H, ground_h, frame_count)

        for t in targets:
            t.draw(SCREEN, font_label)
        for b in bullets:
            b.draw(SCREEN)
        c1.draw(SCREEN)
        c2.draw(SCREEN)

        # Score
        sc = font_md.render(f"Score : {score}", True, (255, 255, 255))
        SCREEN.blit(sc, (W // 2 - sc.get_width() // 2, 18))

        # ESC hint
        SCREEN.blit(font_sm.render("ECHAP = retour", True, (200, 230, 200)), (20, 18))

        # Instructions (first 500 frames)
        if frame_count < 500:
            lines = [
                ("Des animaux sauvages envahissent Sungei Buloh ! Chassez-les avec vos canons.", (255, 255, 255)),
                ("ROUGE : A / D pour viser,  W pour tirer", (220, 100, 80)),
                ("BLEU  : GAUCHE / DROITE pour viser,  HAUT pour tirer", (100, 150, 255)),
            ]
            for i, (txt, col) in enumerate(lines):
                surf = font_sm.render(txt, True, col)
                SCREEN.blit(surf, (W // 2 - surf.get_width() // 2, H - 85 + i * 27))

        pygame.display.update()