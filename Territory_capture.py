import pygame as pg, sys
pg.init()
WIDTH, HEIGHT, FPS = 800, 480, 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running == False

    screen.fill((24,26,32))
    pg.display.flip()

pg.quit(); sys.exit()