import pygame

class PlayerJump(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = [
            pygame.image.load("assets/SpriteJump/Bird1.png").convert_alpha(),
            pygame.image.load("assets/SpriteJump/Bird2.png").convert_alpha(),
            pygame.image.load("assets/SpriteJump/Bird3.png").convert_alpha()
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.velocity = 0
        self.gravity = 0.5
        self.jump_force = -8
        self.animating = False

    def jump(self):
        self.velocity = self.jump_force
        self.animating = True

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.animating:
            self.current_sprite += 0.25
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.animating = False
        self.image = self.sprites[int(self.current_sprite)]