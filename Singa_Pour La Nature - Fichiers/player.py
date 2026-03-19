import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.mov_animation = False
        self.sprites = [
            pygame.image.load("assets/SpriteMovement/SpriteMov1.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov2.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov3.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov4.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov5.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov6.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov7.png").convert_alpha(),
            pygame.image.load("assets/SpriteMovement/SpriteMov8.png").convert_alpha(),
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def movement(self):
        self.mov_animation = True

    def update(self, speed):
        if self.mov_animation:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.mov_animation = False
        self.image = self.sprites[int(self.current_sprite)]