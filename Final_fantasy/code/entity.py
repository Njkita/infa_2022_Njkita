import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1 
        self.direction = pygame.math.Vector2()
        
    def move(self, speed):
        #усреднение скорости для диагонального перемещения
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center    
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstracle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): #пересечение игрока и препятствия
                    if self.direction.x > 0: #движение вправо
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #движение вправо
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstracle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): #пересечение игрока и препятствия
                    if self.direction.y > 0: #движение вверх
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #движение вниз
                        self.hitbox.top = sprite.hitbox.bottom
