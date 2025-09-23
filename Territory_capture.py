import pygame as pg, sys

# ------------ CONFIG ------------

pg.init()
WIDTH, HEIGHT, FPS = 800, 480, 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


# ------------ CHARGEMENT IMAGE ------------


# ------------ CREER MAP ------------
MCOLORS = (200,80,80)

maps = [
    pg.Rect(150, 80, 20, 20)
]


# ------------ BOUCLE PRINCIPALE ------------

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running == False



# ------------ DESSIN ------------

    screen.fill((24,26,32))

    for m in maps:
        pg.draw.rect(screen,MCOLORS, m)








    pg.display.flip()

pg.quit(); sys.exit()  # QUITTEZ LE JEU