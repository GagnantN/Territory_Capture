import pygame as pg
import random  # Donne nombre aléatoire
from fonctions.cases import terrains
# ------------------------- MAP ------------------------ #

def create_map(screen):

    # Récupère la taille actuelle de la fenêtre
    WIDTH, HEIGHT = screen.get_size()

    #WCOLOR = (191 , 183, 161)
    BCOLOR = (50, 50, 50)

    case_original = []
    ligne = 20
    colonne = 20
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))  # taille d’une case

    for i in range(ligne):
        for j in range(colonne):
            x = int(WIDTH * 0.25) + j * taille
            y = int(HEIGHT * 0.1) + i * taille
            rect = pg.Rect(x, y, taille, taille)

            # Choisir aléatoire le type de terrain
            terrain_couleur = random.choice(list(terrains.values()))

            case_original.append((rect, terrain_couleur))



    return BCOLOR, case_original

# ------------------------------------------------------- #