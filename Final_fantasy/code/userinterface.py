import pygame
from settings import *


class UI:
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        
        #настройка шкалы здоровья/энергии
        self.health_bar_rect = pygame.Rect(10, 7, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 32, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        
        #словарик оружий
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
            
        #словарик магии
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
    
    def show_bar(self, actual, max_amount, back_rect, color):
        
        #шкала позади
        pygame.draw.rect(self.display_surface, BACK_COLOR, back_rect)
        
        #конвертация в пиксели
        correlation = actual / max_amount 
        actual_width = back_rect.width * correlation
        actual_rect = back_rect.copy()
        actual_rect.width = actual_width
        
        #главная шкала
        pygame.draw.rect(self.display_surface, color, actual_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, back_rect, 3)
    
    def selection_box(self, left, top, has_switched):
        back_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, BACK_COLOR, back_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, BORDER_COLOR_ACTIVE, 
                             back_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, BORDER_COLOR, 
                             back_rect, 3)
        return back_rect
    
    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))
        
        pygame.draw.rect(self.display_surface, BACK_COLOR, 
                         text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, BORDER_COLOR, 
                         text_rect.inflate(10, 10), 3)
    
    def weapon_inside(self, weapon_index, has_switched):
        back_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = back_rect.center)
        
        self.display_surface.blit(weapon_surf, weapon_rect)
        
    def magic_inside(self, magic_index, has_switched):
        back_rect = self.selection_box(100, 630, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = back_rect.center)
        
        self.display_surface.blit(magic_surf, magic_rect)
    
    def display(self, player):
        self.show_bar(player.health, player.stats['health'], 
                      self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], 
                      self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)
        
        self.weapon_inside(player.weapon_index, not player.can_switch_weapon)
        self.magic_inside(player.magic_index, not player.can_switch_magic)