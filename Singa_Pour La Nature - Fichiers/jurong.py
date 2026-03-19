import pygame
import sys
import random
from jumpanimation import PlayerJump

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

font = get_font(36)

def draw_background(screen, W, H, scroll):
    # Sky gradient — tropical blue
    screen.fill((135, 206, 250))

    # Clouds
    for cx, cy in CLOUDS:
        shifted_x = (cx - scroll * 0.3) % (W + 200) - 100
        pygame.draw.ellipse(screen, (255, 255, 255), (shifted_x, cy, 120, 50))
        pygame.draw.ellipse(screen, (255, 255, 255), (shifted_x + 30, cy - 20, 80, 45))
        pygame.draw.ellipse(screen, (255, 255, 255), (shifted_x - 20, cy + 5, 70, 35))

    # Ground strip
    pygame.draw.rect(screen, (80, 160, 60), (0, H - 60, W, 60))
    pygame.draw.rect(screen, (60, 120, 40), (0, H - 60, W, 12))

def draw_bamboo_pipe(screen, rect, is_top):
    # Main bamboo body
    pygame.draw.rect(screen, (60, 140, 40), rect, border_radius=6)
    # Darker edge lines for bamboo segments
    segment_h = 40
    for sy in range(rect.top, rect.bottom, segment_h):
        pygame.draw.line(screen, (40, 100, 20),
                         (rect.left, sy), (rect.right, sy), 3)
    # Highlight strip
    pygame.draw.rect(screen, (100, 180, 60),
                     (rect.left + 6, rect.top, 14, rect.height), border_radius=4)
    # Cap at the open end
    cap_h = 18
    if is_top:
        cap_rect = pygame.Rect(rect.left - 6, rect.bottom - cap_h, rect.width + 12, cap_h)
    else:
        cap_rect = pygame.Rect(rect.left - 6, rect.top, rect.width + 12, cap_h)
    pygame.draw.rect(screen, (40, 120, 30), cap_rect, border_radius=4)

def LEVEL6():
    clock        = pygame.time.Clock()
    W, H         = 1280, 720
    pipe_x       = W
    pipe_width   = 80
    gap          = 210
    pipe_top_h   = 250
    pipe_speed   = 5
    score        = 0
    pipe_passed  = False
    game_over    = False
    scroll       = 0

    global CLOUDS
    CLOUDS = [(random.randint(0, W), random.randint(40, 200)) for _ in range(6)]

    moving_sprites = pygame.sprite.Group()
    player = PlayerJump(100, 360)
    moving_sprites.add(player)

    while True:
        clock.tick(60)
        scroll += pipe_speed * 0.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    return LEVEL6()
                if event.key == pygame.K_ESCAPE:
                    return

        if not game_over:
            pipe_x -= pipe_speed
            if pipe_x < -pipe_width:
                pipe_x = W
                pipe_top_h  = random.randint(120, 380)
                pipe_passed = False

        if not pipe_passed and pipe_x + pipe_width < player.rect.left:
            score += 1
            pipe_passed = True
            # Speed up slightly every 5 points
            if score % 5 == 0:
                pipe_speed = min(12, pipe_speed + 0.5)

        top_pipe    = pygame.Rect(pipe_x, 0,                  pipe_width, pipe_top_h)
        bottom_pipe = pygame.Rect(pipe_x, pipe_top_h + gap,   pipe_width, H)

        # ---- Draw ----
        draw_background(SCREEN, W, H, scroll)
        draw_bamboo_pipe(SCREEN, top_pipe,    is_top=True)
        draw_bamboo_pipe(SCREEN, bottom_pipe, is_top=False)

        moving_sprites.update()
        moving_sprites.draw(SCREEN)

        # Shrunk hitbox
        margin = 10
        hitbox = player.rect.inflate(-margin * 2, -margin * 2)

        if hitbox.colliderect(top_pipe) or hitbox.colliderect(bottom_pipe):
            game_over = True
        if player.rect.top <= 0 or player.rect.bottom >= H - 60:
            game_over = True

        # Score box
        pygame.draw.rect(SCREEN, (0, 0, 0), (10, 10, 210, 55), border_radius=8)
        SCREEN.blit(font.render(f"Score : {score}", True, (255, 255, 255)), (20, 15))

        # Speed indicator
        level_txt = get_font(16).render(
            f"Vitesse : {'▶' * min(int((pipe_speed - 4) // 0.5) + 1, 8)}",
            True, (200, 255, 200))
        SCREEN.blit(level_txt, (10, 70))

        # ESC hint
        SCREEN.blit(get_font(16).render("ECHAP = retour", True, (50, 50, 50)), (1060, 15))

        if game_over:
            # Dark overlay
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            SCREEN.blit(overlay, (0, 0))
            SCREEN.blit(font.render("Game Over !", True, (255, 50, 50)),
                        (W // 2 - 130, H // 2 - 60))
            SCREEN.blit(font.render(f"Score final : {score}", True, (255, 255, 255)),
                        (W // 2 - 140, H // 2))
            SCREEN.blit(get_font(22).render("R = rejouer  |  ECHAP = carte", True, (200, 200, 200)),
                        (W // 2 - 200, H // 2 + 60))

        pygame.display.update()