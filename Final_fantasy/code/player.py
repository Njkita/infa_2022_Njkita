import pygame 
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self,pos,groups,obstracle_sprites, create_attack, 
                 destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player1/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-2, -26)
        
        #настройка графики
        self.import_player_assets()
        self.status = 'down'
        
        #перемещение
        self.attacking = False
        self.attack_cooldown = 350
        self.attack_time = None
        self.obstracle_sprites = obstracle_sprites
        
        #атака
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        #магия
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.switch_duration_cooldown = 200
        
        
        #статистика
        self.stats = {'health': 100, 'energy': 75, 
                      'attack': 8, 'magic': 5, 'speed': 7}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 100
        self.speed = self.stats['speed']
    
    def import_player_assets(self):
        #скины
        character_path = '../graphics/player1/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 
                           'down_idle': [], 'right_attack': [], 'left_attack': [], 
                           'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def input(self):        
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            #движение
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status  = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status  = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status  = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status  = 'right'
            else:
                self.direction.x = 0
            
            #атака
            if keys[pygame.K_RCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                
            if keys[pygame.K_RIGHT] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                    
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                
            if keys[pygame.K_LEFT] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index > 0:
                    self.weapon_index -= 1
                else:
                    self.weapon_index = len(list(weapon_data.keys())) - 1
                    
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            #магия
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                
                self.create_magic(style, strength, cost)
                
            if keys[pygame.K_UP] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                    
                self.magic = list(magic_data.keys())[self.magic_index]
                
            if keys[pygame.K_DOWN] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index > 0:
                    self.magic_index -= 1
                else:
                    self.magic_index = len(list(magic_data.keys())) - 1
                    
                self.magic = list(magic_data.keys())[self.magic_index]
    
    def get_status(self):
        
        #статус ожидания
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
         
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        
    def cooldowns(self):
        actual_time = pygame.time.get_ticks()
        
        if self.attacking:
            if actual_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        
        #для оружия        
        if not self.can_switch_weapon:
            if actual_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        
        #для магии
        if not self.can_switch_magic:
            if actual_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
    
    def animate(self):
        animation = self.animations[self.status]
    
        self.frame_index += self.animation_speed 
        if self.frame_index >= len(animation):
            self.frame_index = 0
    
        #создание изображения
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

