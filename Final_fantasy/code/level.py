import pygame 
from settings import *
from support import *
from tile import Tile
from player import Player
from random import choice
from weapon import Weapon
from userinterface import UI
from monsters import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer

class Level:
    def __init__(self):
        
        #отображение поверхности
        self.display_surface = pygame.display.get_surface()
        
        #настройка группы спрайтов (видимые, препятствия)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #спрайт атаки
        self.actual_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        #настройка спрайтов
        self.create_map()
        
        
        #пользовательский интерфейс
        self.ui = UI()
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
    
    def create_attack(self):
        self.actual_attack = Weapon(self.player,[self.visible_sprites, 
                                                 self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
            
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    
    def destroy_attack(self):
        if self.actual_attack:
            self.actual_attack.kill()
        self.actual_attack = None
    
    def create_map(self):
        #макеты
        layouts = {
            'boundary': import_csv_layout('../map/Map2_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/Map2_Grass.csv'),
            'object1': import_csv_layout('../map/Map2_Objects1.csv'),
            'object2': import_csv_layout('../map/Map2_Objects2.csv'),
            'entities': import_csv_layout('../map/Map2_Entities.csv'),              
        }
        graphics = {
            'grass': import_folder('../graphics/Grass'), 
            'objects': import_folder('../graphics/objects')
        }
        
        
        for stile, layout in layouts.items():  
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '168':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if stile == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                       
                        if stile == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y), 
                                [self.visible_sprites,
                                 self.obstacle_sprites,
                                 self.attackable_sprites],
                                'grass', 
                                random_grass_image
                            )
                            
                        if stile == 'object1':
                            surf = graphics['objects'][int(col)]
                            Tile(
                                (x,y), 
                                [self.visible_sprites, 
                                 self.obstacle_sprites], 
                                'object1', 
                                surf
                            )
                        if stile == 'object2':
                            surf = graphics['objects'][int(col)]
                            Tile(
                                (x,y), 
                                [self.visible_sprites, 
                                 self.obstacle_sprites], 
                                'object2', 
                                surf
                            )
                        if stile == 'entities':
                            if col == '496':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack,
                                    self.create_magic
                                    )
                            else:
                                if col == '492':
                                    monster_name = 'evil_plant'
                                elif col == '493':
                                    monster_name = 'litch'
                                elif col == '494':
                                    monster_name = 'raccoon'
                                elif col == '495':
                                    monster_name = 'orgalorg'
                                Enemy(
                                    monster_name, 
                                      (x, y), 
                                      [self.visible_sprites, 
                                       self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.add_exp
                                      )
       
    def player_attack_logick(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprites, 
                                            self.attackable_sprites, 
                                            False) #список столкнувшихся с игроком спрайтов
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,
                                                     attack_sprites.sprite_type)
                            
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #self.animation_player.create_particles(attack_type,
                                          #self.player.rect.center,
                                          #[self.visible_sprites])

    
    def add_exp(self, amount):
        
        self.player.exp += amount 
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logick()
        self.ui.display(self.player)
        
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #базовые настройки
        super().__init__()
        
        #отображение поверхности
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2() #смещение камеры
        
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    
    def custom_draw(self, player):
        
        #смещение
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #изображение бэка
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery): #сортирование спрайтов по положению
            #прямоугольник смещения
            offset_pos = sprite.rect.topleft - self.offset #смещение
            self.display_surface.blit(sprite.image, offset_pos)
            
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
