import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstracle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
    
        self.obstracle_sprites = obstracle_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
    
    def move(self, speed):
        #усреднение скорости для диагонального перемещения
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.center += self.direction * speed
    
    def collision(self, direction):
        if direction == 'horizontal':
            pass
        if direction == 'vertical':
            pass
    
    def update(self):
        self.input()
        self.move(self.speed)