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

# ---------------------RECUPERE DONNEES------------------ #

WCOLOR, walls = create_map()



# ------------------------------------------------------- #



# ------------------- BOUTTON QUITTER ------------------- #
# Couleurs et police du bouton
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pg.font.SysFont(None, 30)

# Position bas gauche
button_rect = pg.Rect(10, HEIGHT - 50, 120, 40)
# ------------------------------------------------------- #


running = True
while running:

    dt = clock.tick(FPS) / 1000.0

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running == False

        elif e.type == pg.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(e.pos):
                running = False

    screen.fill((24,26,32))

    # DESSIN
    for w in walls:
        pg.draw.rect(screen, WCOLOR, w)
    pg.draw.rect(screen, BLACK, button_rect)
    text_surf = font.render("Quitter", True, WHITE)
    screen.blit(text_surf, (button_rect.x + 10, button_rect.y + 5))



    pg.display.flip()


# ----------------------- Quitter ----------------------- #
pg.quit(); sys.exit()