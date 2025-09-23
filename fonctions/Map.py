import pygame as pg

# ------------------------- MAP ------------------------ #

def create_map(screen):

    # Récupère la taille actuelle de la fenêtre
    WIDTH, HEIGHT = screen.get_size()

    WCOLOR = (200 , int(WIDTH * 0.1) % 256, int(HEIGHT * 0.1) % 256)
    BCOLOR = (50, 50, 50)

    walls = []
    ligne = 20
    colonne = 20
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))  # taille d’une case

    for i in range(ligne):
        for j in range(colonne):
            x = int(WIDTH * 0.25) + j * taille
            y = int(HEIGHT * 0.1) + i * taille
            walls.append(pg.Rect(x, y, taille, taille))


    return WCOLOR, BCOLOR, walls

# ------------------------------------------------------- #