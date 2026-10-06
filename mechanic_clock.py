import pygame
import math
import time

# =========================
# PYGAME
# =========================

pygame.init()

WIDTH = 800
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mechanical Clock")

clock = pygame.time.Clock()

# =========================
# MARKAZ
# =========================

CX = WIDTH // 2
CY = HEIGHT // 2

# Shriftlar
font_big = pygame.font.SysFont("arial", 42, bold=True)
font_small = pygame.font.SysFont("arial", 22, bold=True)

running = True


# =========================
# TISHLI G'ILDIRAK
# =========================

def gear(surface, x, y, radius, teeth, angle, color):

    points = []

    for i in range(teeth * 2):

        a = angle + i * math.pi / teeth

        if i % 2 == 0:
            r = radius
        else:
            r = radius * 0.78

        px = x + math.cos(a) * r
        py = y + math.sin(a) * r

        points.append((px, py))

    pygame.draw.polygon(
        surface,
        color,
        points
    )

    # Ichki qism
    pygame.draw.circle(
        surface,
        (40, 40, 40),
        (int(x), int(y)),
        int(radius * 0.35)
    )

    # Markaziy teshik
    pygame.draw.circle(
        surface,
        (190, 170, 120),
        (int(x), int(y)),
        int(radius * 0.12)
    )


# =========================
# STRELKA
# =========================

def hand(surface, angle, length, width, color):

    x = CX + math.sin(angle) * length
    y = CY - math.cos(angle) * length

    pygame.draw.line(
        surface,
        color,
        (CX, CY),
        (int(x), int(y)),
        width
    )


# =========================
# G'ILDIRAKLAR
# =========================

gears = [
    (220, 250, 65, 16),
    (335, 230, 43, 14),
    (470, 260, 70, 18),
    (575, 350, 45, 14),
    (220, 420, 48, 15),
    (350, 510, 72, 18),
    (505, 510, 48, 15),
    (600, 455, 62, 17)
]


# =========================
# ASOSIY LOOP
# =========================

while running:

    # =========================
    # EVENTLAR
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False


    # =========================
    # HAQIQIY VAQT
    # =========================

    now = time.time()

    current = time.localtime(now)

    hours = current.tm_hour % 12
    minutes = current.tm_min
    seconds = current.tm_sec

    # Sekundning kasr qismi
    fraction = now - int(now)

    # =========================
    # SOAT STRELKASI
    # =========================

    hour_angle = (
        hours * math.pi / 6
        + minutes * math.pi / 360
        + seconds * math.pi / 21600
    )

    # =========================
    # MINUT STRELKASI
    # =========================

    minute_angle = (
        minutes * math.pi / 30
        + seconds * math.pi / 1800
    )

    # =========================
    # SEKUND STRELKASI
    # =========================

    second_angle = (
        (seconds + fraction) * math.pi / 30
    )


    # =========================
    # FON
    # =========================

    screen.fill((15, 15, 19))


    # =========================
    # SOAT KORPUSI
    # =========================

    pygame.draw.circle(
        screen,
        (78, 50, 27),
        (CX, CY),
        340
    )

    pygame.draw.circle(
        screen,
        (25, 25, 28),
        (CX, CY),
        310
    )

    # Tashqi halqa
    pygame.draw.circle(
        screen,
        (190, 160, 105),
        (CX, CY),
        292,
        8
    )


    # =========================
    # MEXANIK G'ILDIRAKLAR
    # =========================

    gear_time = pygame.time.get_ticks() / 1000

    for index, (x, y, r, teeth) in enumerate(gears):

        if index % 2 == 0:
            direction = 1
        else:
            direction = -1

        angle = gear_time * direction * 0.8

        gear(
            screen,
            x,
            y,
            r,
            teeth,
            angle,
            (160, 130, 75)
        )


    # =========================
    # SOAT RAQAMLARI
    # =========================

    for number in range(1, 13):

        angle = number * math.pi / 6

        radius = 245

        x = CX + math.sin(angle) * radius
        y = CY - math.cos(angle) * radius

        text = font_big.render(
            str(number),
            True,
            (225, 215, 180)
        )

        rect = text.get_rect(
            center=(int(x), int(y))
        )

        screen.blit(
            text,
            rect
        )


    # =========================
    # SOAT STRELKASI
    # =========================

    hand(
        screen,
        hour_angle,
        135,
        12,
        (230, 220, 185)
    )


    # =========================
    # MINUT STRELKASI
    # =========================

    hand(
        screen,
        minute_angle,
        195,
        8,
        (230, 220, 185)
    )


    # =========================
    # SEKUND STRELKASI
    # =========================

    hand(
        screen,
        second_angle,
        225,
        3,
        (210, 65, 45)
    )


    # =========================
    # MARKAZ
    # =========================

    pygame.draw.circle(
        screen,
        (215, 180, 95),
        (CX, CY),
        14
    )

    pygame.draw.circle(
        screen,
        (45, 45, 45),
        (CX, CY),
        6
    )


    # =========================
    # MAYATNIK
    # =========================

    pendulum_angle = math.sin(
        gear_time * 2.5
    ) * 0.35

    pendulum_x = (
        CX +
        math.sin(pendulum_angle) * 120
    )

    pendulum_y = CY + 270

    pygame.draw.line(
        screen,
        (190, 160, 100),
        (CX, CY + 80),
        (int(pendulum_x), int(pendulum_y)),
        6
    )

    pygame.draw.circle(
        screen,
        (170, 140, 80),
        (int(pendulum_x), int(pendulum_y)),
        27
    )

    pygame.draw.circle(
        screen,
        (50, 50, 50),
        (int(pendulum_x), int(pendulum_y)),
        16
    )


    # =========================
    # RAQAMLI VAQT
    # =========================

    time_text = time.strftime(
        "%H:%M:%S"
    )

    digital = font_small.render(
        time_text,
        True,
        (220, 205, 165)
    )

    screen.blit(
        digital,
        (
            CX - digital.get_width() // 2,
            715
        )
    )


    # =========================
    # EKRANNI YANGILASH
    # =========================

    pygame.display.flip()

    clock.tick(60)


# =========================
# YOPISH
# =========================

pygame.quit()