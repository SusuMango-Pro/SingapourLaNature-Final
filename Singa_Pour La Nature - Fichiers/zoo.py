import pygame
import sys
import random

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.SysFont("comicsansms", size, bold=True)

QUESTIONS = [
    {
        "question": "Quel animal est connu comme le 'jardinier de la foret'?",
        "options": ["A. Orang-outan", "B. Tigre blanc", "C. Hippo pygmee"],
        "answer": "A"
    },
    {
        "question": "Quelle est la longueur maximale de la langue d'une girafe?",
        "options": ["A. 20 cm", "B. 45 cm", "C. 70 cm"],
        "answer": "B"
    },
    {
        "question": "Comment les suricates se rechauffent-ils?",
        "options": ["A. En se roulant dans la boue", "B. En prenant le soleil", "C. En se serrant les uns contre les autres"],
        "answer": "B"
    },
    {
        "question": "En quelle annee le Zoo de Singapour a-t-il ouvert?",
        "options": ["A. 1965", "B. 1973", "C. 1990"],
        "answer": "B"
    },
    {
        "question": "Quel grand felide est le plus rare au monde?",
        "options": ["A. Leopard des neiges", "B. Tigre blanc", "C. Leopard de l'Amour"],
        "answer": "C"
    },
]

def LEVEL2():
    clock = pygame.time.Clock()
    font_title = get_font(36)
    font_q     = get_font(22)
    font_opt   = get_font(20)
    font_small = get_font(16)

    random.shuffle(QUESTIONS)
    q_index  = 0
    score    = 0
    feedback = ""
    fb_color = (255, 255, 255)
    answered = False

    while True:
        clock.tick(60)
        SCREEN.fill((20, 60, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if q_index < len(QUESTIONS) and not answered:
                    key_map = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C"}
                    if event.key in key_map:
                        chosen = key_map[event.key]
                        correct = QUESTIONS[q_index]["answer"]
                        if chosen == correct:
                            score += 10
                            feedback = "Correct ! +10"
                            fb_color = (100, 255, 100)
                        else:
                            feedback = f"Faux ! La reponse etait {correct}"
                            fb_color = (255, 80, 80)
                        answered = True

                elif q_index < len(QUESTIONS) and answered:
                    q_index += 1
                    feedback = ""
                    answered = False

        if q_index < len(QUESTIONS):
            q_data = QUESTIONS[q_index]

            prog = font_small.render(f"Question {q_index + 1} / {len(QUESTIONS)}", True, (180, 220, 180))
            SCREEN.blit(prog, (40, 30))

            sc = font_small.render(f"Score: {score}", True, (255, 220, 100))
            SCREEN.blit(sc, (1100, 30))

            pygame.draw.rect(SCREEN, (0, 40, 20), (40, 80, 1200, 130), border_radius=12)
            words = q_data["question"].split()
            lines = []
            line = ""
            for w in words:
                test = line + " " + w if line else w
                if font_q.size(test)[0] < 1150:
                    line = test
                else:
                    lines.append(line)
                    line = w
            lines.append(line)
            for i, l in enumerate(lines):
                SCREEN.blit(font_q.render(l, True, (255, 255, 255)), (60, 95 + i * 40))

            y = 260
            for opt in q_data["options"]:
                pygame.draw.rect(SCREEN, (0, 80, 40), (200, y, 880, 65), border_radius=8)
                SCREEN.blit(font_opt.render(opt, True, (220, 255, 220)), (220, y + 16))
                y += 95

            if feedback:
                fb_surf = font_q.render(feedback, True, fb_color)
                SCREEN.blit(fb_surf, (500, 590))
                next_hint = font_small.render("Appuie sur n'importe quelle touche pour continuer", True, (180, 180, 180))
                SCREEN.blit(next_hint, (330, 645))
            else:
                hint = font_small.render("Appuie sur A, B ou C pour repondre  |  ECHAP = retour", True, (120, 180, 120))
                SCREEN.blit(hint, (300, 670))

        else:
            pygame.draw.rect(SCREEN, (0, 40, 20), (240, 160, 800, 360), border_radius=16)
            done = font_title.render("Quiz termine !", True, (255, 220, 50))
            SCREEN.blit(done, (390, 210))
            sc_big = font_title.render(f"Score final : {score} / {len(QUESTIONS) * 10}", True, (255, 255, 255))
            SCREEN.blit(sc_big, (310, 300))
            grade = "Incroyable !" if score == len(QUESTIONS)*10 else "Bien joue !" if score >= len(QUESTIONS)*6 else "Continue d'apprendre !"
            SCREEN.blit(font_q.render(grade, True, (100, 255, 150)), (450, 390))
            esc_hint = font_small.render("ECHAP = retour a la carte", True, (180, 180, 180))
            SCREEN.blit(esc_hint, (470, 460))

        pygame.display.update()