import pygame
import sys
import random
import math

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

# ---- Load all animal images ----
def load_img(path, w, h):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.circle(surf, (180, 100, 50), (w//2, h//2), w//2)
        return surf

ANIMAL_PATHS = [
    "assets/serpent-trp.png",
    "assets/mosqui-trp.png",
    "assets/croc-trp.png",
    "assets/eagle-trp.png",
    "assets/boar2-trp.png",
    "assets/otter-trp.png",
    "assets/watersnake-trp.png",
    "assets/shark1-trp.png",
    "assets/turtle1-trp.png",
    "assets/fish1-trp.png",
    "assets/fish2-trp.webp",
    "assets/fish3-trp.jpeg",
    "assets/fish4-trp.webp",
    "assets/fish5-trp.png",
]

BALL_SIZE = 60

# ---- Background ----
def draw_background(screen, W, H):
    # Lush green botanic garden feel
    screen.fill((34, 100, 34))

    # Darker green stripes for garden path feel
    for i in range(0, W, 160):
        pygame.draw.rect(screen, (28, 85, 28), (i, 0, 80, H))

    # Centre dashed line
    for y in range(0, H, 40):
        pygame.draw.rect(screen, (255, 255, 255, 80), (W//2 - 3, y, 6, 22))

    # Top and bottom walls
    pygame.draw.rect(screen, (20, 60, 20), (0, 0,      W, 15))
    pygame.draw.rect(screen, (20, 60, 20), (0, H - 15, W, 15))

    # Flower decorations on the sides
    for fx, fy, fc in FLOWERS:
        pygame.draw.circle(screen, fc,          (fx, fy), 10)
        pygame.draw.circle(screen, (255, 255, 0),(fx, fy), 5)

# ---- LEVEL7 ----
def LEVEL7():
    clock  = pygame.time.Clock()
    W, H   = SCREEN.get_width(), SCREEN.get_height()
    WALL_T = 15   # top/bottom wall thickness

    font_big   = get_font(42)
    font_med   = get_font(28)
    font_small = get_font(18)
    font_tiny  = get_font(14)

    # Pre-load all animal images
    animal_imgs = [load_img(p, BALL_SIZE, BALL_SIZE) for p in ANIMAL_PATHS]

    global FLOWERS
    FLOWERS = []
    for _ in range(30):
        side = random.choice(["left", "right"])
        fx   = random.randint(10, 80) if side == "left" else random.randint(W-80, W-10)
        fy   = random.randint(WALL_T + 10, H - WALL_T - 10)
        fc   = (random.randint(180, 255), random.randint(50, 150), random.randint(50, 200))
        FLOWERS.append((fx, fy, fc))

    # ---- Game state ----
    PADDLE_W  = 18
    PADDLE_H  = 100
    PADDLE_SP = 6
    AI_SPEED  = 4   # AI is beatable but not trivial

    def reset_ball():
        angle  = random.uniform(-math.pi/4, math.pi/4)
        speed  = 5
        dirx   = random.choice([-1, 1])
        return {
            "x":     float(W // 2),
            "y":     float(H // 2),
            "vx":    dirx * math.cos(angle) * speed,
            "vy":    math.sin(angle) * speed,
            "img":   random.choice(animal_imgs),
        }

    def next_animal(ball):
        # Change to a different animal on bounce
        current = ball["img"]
        choices = [img for img in animal_imgs if img is not current]
        ball["img"] = random.choice(choices)

    player_y  = float(H // 2 - PADDLE_H // 2)
    ai_y      = float(H // 2 - PADDLE_H // 2)
    ball      = reset_ball()

    player_score = 0
    ai_score     = 0
    WIN_SCORE    = 7

    game_over    = False
    winner       = ""
    life         = 300   # health bar like original

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r and game_over:
                    # Restart
                    player_y     = float(H // 2 - PADDLE_H // 2)
                    ai_y         = float(H // 2 - PADDLE_H // 2)
                    ball         = reset_ball()
                    player_score = 0
                    ai_score     = 0
                    life         = 300
                    game_over    = False
                    winner       = ""

        if not game_over:
            # ---- Player paddle (W / S keys) ----
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_y -= PADDLE_SP
            if keys[pygame.K_s]:
                player_y += PADDLE_SP
            player_y = max(WALL_T, min(H - WALL_T - PADDLE_H, player_y))

            # ---- AI paddle (tracks ball with limited speed) ----
            ai_centre = ai_y + PADDLE_H // 2
            if ai_centre < ball["y"] - 5:
                ai_y += AI_SPEED
            elif ai_centre > ball["y"] + 5:
                ai_y -= AI_SPEED
            ai_y = max(WALL_T, min(H - WALL_T - PADDLE_H, ai_y))

            # ---- Ball movement ----
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]

            # Top / bottom wall bounce
            if ball["y"] - BALL_SIZE//2 <= WALL_T:
                ball["y"] = WALL_T + BALL_SIZE//2
                ball["vy"] *= -1
                next_animal(ball)
            if ball["y"] + BALL_SIZE//2 >= H - WALL_T:
                ball["y"] = H - WALL_T - BALL_SIZE//2
                ball["vy"] *= -1
                next_animal(ball)

            # Player paddle rect (left side)
            player_rect = pygame.Rect(60, int(player_y), PADDLE_W, PADDLE_H)
            # AI paddle rect (right side)
            ai_rect     = pygame.Rect(W - 60 - PADDLE_W, int(ai_y), PADDLE_W, PADDLE_H)

            ball_rect = pygame.Rect(
                int(ball["x"]) - BALL_SIZE//2,
                int(ball["y"]) - BALL_SIZE//2,
                BALL_SIZE, BALL_SIZE
            )

            # Player paddle hit
            if ball_rect.colliderect(player_rect) and ball["vx"] < 0:
                ball["vx"] *= -1
                # Add slight angle based on where ball hits paddle
                rel = (ball["y"] - (player_y + PADDLE_H//2)) / (PADDLE_H//2)
                ball["vy"] = rel * 5
                next_animal(ball)
                # Increase speed slightly
                ball["vx"] *= 1.05

            # AI paddle hit
            if ball_rect.colliderect(ai_rect) and ball["vx"] > 0:
                ball["vx"] *= -1
                rel = (ball["y"] - (ai_y + PADDLE_H//2)) / (PADDLE_H//2)
                ball["vy"] = rel * 5
                next_animal(ball)
                ball["vx"] *= 1.05

            # Ball goes past left — AI scores, reduce life
            if ball["x"] < 0:
                ai_score += 1
                life -= 60
                ball = reset_ball()

            # Ball goes past right — player scores
            if ball["x"] > W:
                player_score += 1
                ball = reset_ball()

            # Win condition
            if player_score >= WIN_SCORE:
                game_over = True
                winner    = "Joueur"
            if ai_score >= WIN_SCORE:
                game_over = True
                winner    = "IA"

            # Life depleted
            if life <= 0:
                game_over = True
                winner    = "IA"

        # ---- Draw ----
        draw_background(SCREEN, W, H)

        # Centre dashed line
        for y in range(WALL_T, H - WALL_T, 40):
            pygame.draw.rect(SCREEN, (255, 255, 255),
                             (W//2 - 3, y, 6, 22))

        # Paddles
        pygame.draw.rect(SCREEN, (50, 180, 50),
                         (60, int(player_y), PADDLE_W, PADDLE_H), border_radius=6)
        pygame.draw.rect(SCREEN, (180, 50, 50),
                         (W - 60 - PADDLE_W, int(ai_y), PADDLE_W, PADDLE_H), border_radius=6)

        # Ball — animal image
        SCREEN.blit(ball["img"],
                    (int(ball["x"]) - BALL_SIZE//2, int(ball["y"]) - BALL_SIZE//2))

        # Scores
        ps = font_big.render(str(player_score), True, (50, 220, 50))
        ai = font_big.render(str(ai_score),     True, (220, 50, 50))
        SCREEN.blit(ps, (W//2 - 100 - ps.get_width(), 20))
        SCREEN.blit(ai, (W//2 + 100, 20))

        # Player / AI labels
        SCREEN.blit(font_tiny.render("JOUEUR  (W/S)", True, (180, 255, 180)), (30, H - 40))
        SCREEN.blit(font_tiny.render("IA", True, (255, 180, 180)), (W - 60, H - 40))

        # Life bar (bottom centre like original)
        bar_w = 300
        pygame.draw.rect(SCREEN, (60, 60, 60),
                         (W//2 - bar_w//2, H - 40, bar_w, 15), border_radius=6)
        life_clamped = max(0, life)
        fill_w = int(bar_w * life_clamped / 300)
        color  = (50, 200, 50) if life > 150 else (220, 180, 0) if life > 80 else (220, 50, 50)
        pygame.draw.rect(SCREEN, color,
                         (W//2 - bar_w//2, H - 40, fill_w, 15), border_radius=6)
        SCREEN.blit(font_tiny.render("Vie", True, (220, 220, 220)),
                    (W//2 - bar_w//2 - 40, H - 42))

        # Win to score hint
        SCREEN.blit(font_tiny.render(f"Premier a {WIN_SCORE} points gagne !", True, (200, 230, 200)),
                    (W//2 - 160, 75))

        # ESC hint
        SCREEN.blit(font_tiny.render("ECHAP = retour", True, (180, 220, 180)), (20, 18))

        # ---- Game over overlay ----
        if game_over:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            SCREEN.blit(overlay, (0, 0))

            if winner == "Joueur":
                msg_color = (50, 255, 50)
                msg       = "Bravo, vous avez gagne !"
            else:
                msg_color = (255, 50, 50)
                msg       = "L'IA a gagne !"

            SCREEN.blit(font_big.render(msg, True, msg_color),
                        (W//2 - font_big.size(msg)[0]//2, H//2 - 80))
            SCREEN.blit(font_med.render(f"Joueur : {player_score}  —  IA : {ai_score}",
                        True, (255, 255, 255)),
                        (W//2 - 180, H//2))
            SCREEN.blit(font_med.render("R = rejouer  |  ECHAP = carte",
                        True, (200, 200, 200)),
                        (W//2 - 220, H//2 + 70))

        pygame.display.update()