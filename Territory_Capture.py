import pygame as pg, sys

# ------------ CONFIG ------------ #
pg.init()
WIDTH, HEIGHT, FPS = 1500, 1000, 60

# Ecran Fullscreen
screen = pg.display.set_mode(((0, 0)), pg.FULLSCREEN)

clock = pg.time.Clock()


# --- Murs ---
WCOLOR = (200,80,80)
walls = [
    pg.Rect(150, 80, 500, 24),
    pg.Rect(150, 380, 500, 24),
    pg.Rect(150, 80, 24, 324),
    pg.Rect(626, 80, 24, 324),
    pg.Rect(300, 210, 200, 24),
]


# ---------- Bouton Quitter ----- #
# Couleurs et police du bouton
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pg.font.SysFont(None, 30)

# Position bas gauche
button_rect = pg.Rect(10, HEIGHT - 50, 120, 40)

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

pg.quit(); sys.exit()  # QUITTEZ LE JEU