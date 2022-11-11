import pygame
import random
from os import path
import math
from math import *

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 800
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 155, 50)
DGREEN = (1, 50, 32)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

kof = 180/(math.pi)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK , outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Battlefield", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "WASD keys to move, Mouse to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 75))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        

    def update(self):
        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10        
        
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -6
            self.image = pygame.transform.scale(tank90_img, (75, 50))
            self.image.set_colorkey(BLACK)
            
        if keystate[pygame.K_d]:
            self.speedx = 6
            self.image = pygame.transform.scale(tankm90_img, (75, 50))
            self.image.set_colorkey(BLACK)
            
        if keystate[pygame.K_w]:
            self.speedy = -4
            self.image = pygame.transform.scale(player_img, (50, 75))
            self.image.set_colorkey(BLACK)
            
        if keystate[pygame.K_s]:
            self.speedy = 4 
            self.image = pygame.transform.scale(tank180_img, (50, 75))
            self.image.set_colorkey(BLACK)
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH-10:
            self.rect.right = WIDTH-10
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.bottom > HEIGHT-10:
            self.rect.bottom = HEIGHT-10
        if self.rect.top < 400:
            self.rect.top =  400

    def shoot(self):
        global gunmode
        self.type = gunmode
        
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.type == 1:
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
            elif self.type == 2:
                bullet2 = Bullet2(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
    
    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)       
        
        self.speed = 10
        pos = pygame.mouse.get_pos()
        self.speedy = self.speed*((pos[1]-y)/(((pos[1]-y)**2+(pos[0]-x)**2)**0.5))
        self.speedx = self.speed*((pos[0]-x)/(((pos[1]-y)**2+(pos[0]-x)**2)**0.5))
        self.acseleration = 0.2
        ratio = (atan(self.speedx/self.speedy))*kof
        if abs(ratio) <= 15 and self.speedy <= 0:
            self.image = bullet_img
        elif 45 >= abs(ratio) > 15 and self.speedy <= 0 and self.speedx >= 0:
            self.image = bulletm30_img
        elif 45 >= abs(ratio) > 15 and self.speedy <= 0 and self.speedx <= 0:
            self.image = bullet30_img
        elif 75 >= abs(ratio) > 45 and self.speedy <= 0 and self.speedx >= 0:
            self.image = bulletm60_img
        elif 75 >= abs(ratio) > 45 and self.speedy <= 0 and self.speedx <= 0:
            self.image = bullet60_img
        elif 90 >= abs(ratio) > 75 and self.speedx >= 0:
            self.image = bulletm90_img
        elif 90 >= abs(ratio) > 75 and self.speedx <= 0:
            self.image = bullet90_img
        elif 75 >= abs(ratio) > 45 and self.speedy >= 0 and self.speedx >= 0:
            self.image = bulletm120_img
        elif 75 >= abs(ratio) > 45 and self.speedy >= 0 and self.speedx <= 0:
            self.image = bullet120_img
        elif 45 >= abs(ratio) > 15 and self.speedy >= 0 and self.speedx >= 0:
            self.image = bulletm150_img
        elif 45 >= abs(ratio) > 15 and self.speedy >= 0 and self.speedx <= 0:
            self.image = bullet150_img
        elif abs(ratio) <= 15 and self.speedy >= 0:
            self.image = bullet180_img
            
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x

    def update(self):
        ratio = (atan(self.speedx/self.speedy))*kof
        if abs(ratio) <= 15 and self.speedy <= 0:
            self.image = bullet_img
        elif 45 >= abs(ratio) > 15 and self.speedy <= 0 and self.speedx >= 0:
            self.image = bulletm30_img
        elif 45 >= abs(ratio) > 15 and self.speedy <= 0 and self.speedx <= 0:
            self.image = bullet30_img
        elif 75 >= abs(ratio) > 45 and self.speedy <= 0 and self.speedx >= 0:
            self.image = bulletm60_img
        elif 75 >= abs(ratio) > 45 and self.speedy <= 0 and self.speedx <= 0:
            self.image = bullet60_img
        elif 90 >= abs(ratio) > 75 and self.speedx >= 0:
            self.image = bulletm90_img
        elif 90 >= abs(ratio) > 75 and self.speedx <= 0:
            self.image = bullet90_img
        elif 75 >= abs(ratio) > 45 and self.speedy >= 0 and self.speedx >= 0:
            self.image = bulletm120_img
        elif 75 >= abs(ratio) > 45 and self.speedy >= 0 and self.speedx <= 0:
            self.image = bullet120_img
        elif 45 >= abs(ratio) > 15 and self.speedy >= 0 and self.speedx >= 0:
            self.image = bulletm150_img
        elif 45 >= abs(ratio) > 15 and self.speedy >= 0 and self.speedx <= 0:
            self.image = bullet150_img
        elif abs(ratio) <= 15 and self.speedy >= 0:
            self.image = bullet180_img
        self.image.set_colorkey(BLACK)
        self.speedy += self.acseleration
        if self.speedx > 0:
            self.speedx -= self.acseleration*0.5
        if self.speedx < 0:
            self.speedx += self.acseleration*0.5 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)   
        self.image = rasen0_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centery = y
        self.rect.centerx = x
        self.speed = 15
        pos = pygame.mouse.get_pos()
        self.speedy = self.speed*((pos[1]-y)/(((pos[1]-y)**2+(pos[0]-x)**2)**0.5))
        self.speedx = self.speed*((pos[0]-x)/(((pos[1]-y)**2+(pos[0]-x)**2)**0.5))
        self.acseleration = 0.2
        

    def update(self):
        self.speedy -= self.speedy*0.075
        if self.speedx > 0:
            self.speedx -= self.speedx*0.05
        if self.speedx < 0:
            self.speedx -= self.speedx*0.05 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0 or self.rect.left < 0 or self.rect.right > WIDTH or self.speedy >= -0.05:
            self.kill()
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, "field1.png")).convert()
background_rect = background.get_rect()
rasengun_img = pygame.image.load(path.join(img_dir, "rasengan.png")).convert()
rasen0_img = pygame.image.load(path.join(img_dir, "rasen000.png")).convert()

player_img = pygame.image.load(path.join(img_dir, "tank1.png")).convert()
tank90_img = pygame.image.load(path.join(img_dir, "tank90.png")).convert()
tankm90_img = pygame.image.load(path.join(img_dir, "tank-90.png")).convert()
tank180_img = pygame.image.load(path.join(img_dir, "tank180.png")).convert()

bullet_img = pygame.image.load(path.join(img_dir, "raketa.png")).convert()
bullet30_img = pygame.image.load(path.join(img_dir, "raketa30.png")).convert()
bulletm30_img = pygame.image.load(path.join(img_dir, "raketa-30.png")).convert()
bullet60_img = pygame.image.load(path.join(img_dir, "raketa60.png")).convert()
bulletm60_img = pygame.image.load(path.join(img_dir, "raketa-60.png")).convert()
bullet90_img = pygame.image.load(path.join(img_dir, "raketa90.png")).convert()
bulletm90_img = pygame.image.load(path.join(img_dir, "raketa-90.png")).convert()
bullet120_img = pygame.image.load(path.join(img_dir, "raketa120.png")).convert()
bulletm120_img = pygame.image.load(path.join(img_dir, "raketa-120.png")).convert()
bullet150_img = pygame.image.load(path.join(img_dir, "raketa150.png")).convert()
bulletm150_img = pygame.image.load(path.join(img_dir, "raketa-150.png")).convert()
bullet180_img = pygame.image.load(path.join(img_dir, "raketa180.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               ]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

gunmode = 2
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(9):
    newmob()
score = 0

# Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
        
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN: #pygame.KEYDOWN:
            #if event.key == pygame.MOUSEBUTTONDOWN:
            player.shoot()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                gunmode = 1
                
            elif event.key == pygame.K_2:
                gunmode = 2
                
    # Обновление
    all_sprites.update()

    # проверьте, не попала ли пуля в моб
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += int(0.1*hit.radius)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    
    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        running = False    
    
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()


