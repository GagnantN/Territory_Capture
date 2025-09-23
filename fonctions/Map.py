import pygame as pg

# ------------------------- MAP ------------------------ #

def create_map():
    WCOLOR = (200,80,80)
    BCOLOR = (50, 50, 50)

    walls = []
    ligne = 20
    colonne = 20
    taille = 20  # taille d’une case

    for i in range(ligne):
        for j in range(colonne):
            x = 150 + j * taille
            y = 80 + i * taille
            walls.append(pg.Rect(x, y, taille, taille))


    return WCOLOR, BCOLOR, walls

# ------------------------------------------------------- #