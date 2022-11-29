import math

from solar_vis import *

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.
    Параметры:
    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """
    global mass_center
    mass_center = [0, 0]
    system_mass = 0
    body.ax = body.ay = 0
    for obj in space_objects:
        system_mass += obj.m
        mass_center[0] += obj.m * obj.x
        mass_center[1] += obj.m * obj.y
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = [(body.x - obj.x), (body.y - obj.y)]
        # r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        # cosinus = (body.x - obj.x) / r
        # sinus = (body.y - obj.y) / r
        if r[0] == 0:
            body.ax = 0
        else:
            body.ax += -r[0] / abs(r[0]) * gravitational_constant * body.m / (r[0] ** 2 + r[1] ** 2)
        if r[1] == 0:
            body.ay = 0
        else:
            body.ay += -r[1] / abs(r[1]) * gravitational_constant * body.m / (r[0] ** 2 + r[1] ** 2)
        # body.Fx += cosinus * gravitational_constant * body.m * obj.m / r** 2
    for coord in mass_center:
        coord/=system_mass
    return body, mass_center


def move_space_object(body, mass_center):
    """Перемещает тело в соответствии с действующей на него силой.
    Параметры:
    **body** — тело, которое нужно переместить.
    """

    ax = body.ax
    dx = body.Vx + ax / 2
    body.Vx += ax

    ay = body.ay
    dy = body.Vy + ay / 2
    body.Vy += ay

    d_phi = ((dx**2 + dy**2)/((mass_center[0] - body.x)**2 + (mass_center[1] - body.y))**2)**0.5
    dx -= dy * math.sin(d_phi)
    dy -= dx * math.sin(d_phi)

    body.x += (dx)
    body.y += (dy)
    return body


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.
    Параметры:
    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """
    for i in range(int(dt)):
        for body in space_objects:
            calculate_force(body, space_objects)

        for body in space_objects:
            move_space_object(body, mass_center)


if __name__ == "__main__":
    print("This module is not for direct call!")
