import pygame as pg
from pygame.draw import *
from math import *
from random import randint


pg.init()

FPS = 40
screen = pg.display.set_mode((900, 900))

Red = (255, 0, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Green = (0, 255, 0)
Pink = (255, 0, 255)
Cyan = (0, 255, 255)
Black = (0, 0, 0)
Lapis = (0, 150, 200)
Colors = [Red, Green, Blue, Yellow, Pink, Cyan]

counter = 0 #общее число очков 
misses = 0  #число мискликов

count_of_balls = 4
absis = [0 for i in range(count_of_balls)]
ordinate = [0 for i in range(count_of_balls)]
radius = [0 for i in range(count_of_balls)]
velocity = [] #скорость
repeat = 0
colour = []
cycle = 0
lapis = 0


def new_ball():  # Рисуем шарик
    global x, y, r, color, vx, vy
    x = randint(100, 1100)
    y = randint(100, 700)
    r = randint(20, 70)
    vx = randint(-7, 7)
    vy = randint(-7, 7)
    color = Colors[randint(0, 5)]
    circle(screen, color, (x, y), r)


def multiple_balls():  # Рисуем несколько шариков, с возможностью указать их максимальное количество
    global count_of_balls, absis, ordinate, radius, FPS, color, velocity
    new_ball()
    velocity.append([vx, vy])
    colour.append(color)
    absis.append(x)
    ordinate.append(y)
    radius.append(r)


def ball_move():  # Передвижение шариков по экрану
    global count_of_balls, absis, ordinate, radius, FPS, colour, velocity
    screen.fill(Black)
    for i in range(count_of_balls):
        absis[i] += velocity[i][0]
        ordinate[i] += velocity[i][1]
        if radius[i] > absis[i]:
            velocity[i][0] = randint(0, 7)
            velocity[i][1] = randint(-7, 7)
        if radius[i] > ordinate[i]:
            velocity[i][1] = randint(0, 7)
            velocity[i][0] = randint(-7, 7)
        if absis[i] > 900 - radius[i]:
            velocity[i][0] = randint(-7, 0)
            velocity[i][1] = randint(-7, 7)
        if ordinate[i] > 900 - radius[i]:
            velocity[i][1] = randint(-7, 0)
            velocity[i][0] = randint(-7, 7)
        absis[i] += velocity[i][0]
        ordinate[i] += velocity[i][1]
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])


def ball_death(n):  # Удаляем самый старый шарик
    global count_of_balls, absis, ordinate, radius, FPS, colour, velocity
    screen.fill(Black)
    velocity = velocity[:n] + velocity[n + 1:]
    absis = absis[:n] + absis[n + 1:]
    ordinate = ordinate[:n] + ordinate[n + 1:]
    radius = radius[:n] + radius[n + 1:]
    colour = colour[:n] + colour[n + 1:]
    for i in range(count_of_balls - 1):
        circle(screen, colour[i], (absis[i], ordinate[i]), radius[i])


def lapis_move():
    global vx_lapis, vy_lapis, x_lapis, y_lapis
    x_lapis += vx_lapis*0.1
    y_lapis += vy_lapis*0.1
    vx_lapis = randint(-15, 15)
    vy_lapis = randint(-15, 15)
    rect(screen, Lapis, (x_lapis, y_lapis, 50, 50))
    pg.display.update()
def lapis_rect():
    global x_lapis, y_lapis, vx_lapis, vy_lapis
    x_lapis = randint(100, 800)
    y_lapis = randint(100, 800)
    vx_lapis = randint(-15, 15)
    vy_lapis = randint(-15, 15)
    rect(screen, Lapis, (x_lapis, y_lapis, 50, 50))




def score_points(rad, vel):  # Подсчёт очков за различные цели
    global counter
    if rad > 50:
        precounter = 1
    elif rad > 35:
        precounter = 2
    elif rad > 20:
        precounter = 4
    counter += precounter
    


pg.display.update()
clock = pg.time.Clock()
finished = False

while not finished:
    multiple_balls()
    if repeat < count_of_balls:  # Проверка наличия на экране необходимого числа шариков посе запуска
        repeat += 1
    elif cycle < 20:  # Реализуем движение шариков
        clock.tick(FPS)
        ball_move()
        pg.display.update()
        cycle += 1
    else:
        ball_death(0)  # Реализуем удаление шариков по истечении их срока жизни
        pg.display.update()
        cycle = 0

    for event in pg.event.get():
        not_miss = False
        if event.type == pg.QUIT:
            finished = True

        elif event.type == pg.MOUSEBUTTONDOWN:  # Событие нажатия мыши
            mousepos = list(event.pos)  # запоминаем координаты мыши в момент нажатия

            for i in range(count_of_balls):
                if (absis[i] - mousepos[0]) ** 2 + (ordinate[i] - mousepos[1]) ** 2 <= radius[i] ** 2:  # Проверка попадания в один из кругов
                    score_points(radius[i], velocity[i][0] ** 2 + velocity[i][1] ** 2)  # Подсчёт оков
                    print("Tap")
                    not_miss = True
                    ball_death(i)  # Удаление нажатого шарика
                    pg.display.update()


            if lapis > 0:
                if abs(x_lapis - mousepos[0]) <= 50 or abs(y_lapis - mousepos[1]) <= 50:
                    print("-UltraMegaTap-")
                    not_miss = True
                    counter += 10
                    lapis = 0

            if not not_miss:
                print("Miss")
                misses += 1  # Подсчёт промахов
                not_miss = 0
            if misses == 5:
                finished = True  # Проигрыш при пяти промахах
                print("---You lose---")

    if randint(0, 150) == 20 and lapis == 0:
        lapis_rect()
        lapis = 50
    if lapis > 0:
        lapis_move()
        lapis -= 1

print("Your score is", counter)
pg.quit()
