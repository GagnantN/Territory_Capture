import pygame as pg, sys
from fonctions.Map import create_map

# -------------------- CONFIGURATION -------------------- #
pg.init()
WIDTH, HEIGHT, FPS = 1500, 1000, 60

# Ecran Fullscreen
screen = pg.display.set_mode(((0, 0)), pg.FULLSCREEN)

# Nom du Jeu
pg.display.set_caption("Territory Capture")


clock = pg.time.Clock()
# ------------------------------------------------------- #

# --------------------- IMPORT -------------------------- #

# Maps
WCOLOR, walls = create_map()
# Buttons Quitter
from fonctions.boutons import button_rect, button_color, button_text_color, text_surface 
# ------------------------------------------------------- #





running = True



while running:

    dt = clock.tick(FPS) / 1000.0

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

        elif e.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(e.pos):
                running = False # Quitter si clic sur le bouton

    screen.fill((24,26,32))
    pg.draw.rect(screen, button_color, button_rect)
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))

    # Afficher la Map
    for w in walls :
        pg.draw.rect(screen, WCOLOR, w)


    pg.display.flip()


# ----------------------- Quitter ----------------------- #
pg.quit(); sys.exit()