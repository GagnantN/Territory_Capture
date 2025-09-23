import pygame as pg, sys

# -------------------- CONFIGURATION -------------------- #
pg.init()
WIDTH, HEIGHT, FPS = 1500, 1000, 60

# Ecran Fullscreen
screen = pg.display.set_mode(((0, 0)), pg.FULLSCREEN)

clock = pg.time.Clock()
# ------------------------------------------------------- #




# ------------------------ IMPORT ----------------------- #
from fonctions.boutons import button_rect, button_color, button_text_color, text_surface 
# ------------------------------------------------------- #


# ------------------------- MURS ------------------------ #
WCOLOR = (200,80,80)
walls = [
    pg.Rect(150, 80, 500, 24),
    pg.Rect(150, 380, 500, 24),
    pg.Rect(150, 80, 24, 324),
    pg.Rect(626, 80, 24, 324),
    pg.Rect(300, 210, 200, 24),
]
# ------------------------------------------------------- #


running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running == False

        elif e.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(e.pos):
                running = False # Quitter si clic sur le bouton

    screen.fill((24,26,32))
    pg.draw.rect(screen, button_color, button_rect)
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))


    pg.display.flip()


# ----------------------- Quitter ----------------------- #
pg.quit(); sys.exit()