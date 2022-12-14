import pygame 
from settings import *

#покрытие(плитка)
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, 
                 surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'object1':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1]-TILESIZE))
        elif sprite_type == 'object2':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10) #сжатие

