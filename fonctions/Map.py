import pygame as pg
import random  # Donne nombre aléatoire
from fonctions.cases import terrains
# ------------------------- MAP ------------------------ #

def create_map(screen):

    # Récupère la taille actuelle de la fenêtre
    WIDTH, HEIGHT = screen.get_size()

    #WCOLOR = (191 , 183, 161)
    BCOLOR = (50, 50, 50)

    ligne = 20
    colonne = 20
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))  # taille d’une case

    # Grille vide
    grid = [[None for _ in range(colonne)] for _ in range(ligne)]

    # Fonction pour vérifié si une case est libre avec espacement
    def is_valid(i, j):
        # Véfifié qui (i,j) est bien dans une grille
        if not (0 <= i < ligne and 0 <= j < colonne):
            return False
        
        # Vérifie si la case est déjà prise
        if grid[i][j] is not None :
            return False
        
        '''# Vérifie si l'espace est de minimun une case
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < ligne and 0 <= nj < colonne:
                    if grid[ni][nj] is not None:
                        return False'''
        
        return True
    

    # Fonction pour générer une zone contiguë
    def place_zone(color, size):
        attempts = 0
        while attempts < 1000: # enlever problème boucle infinie
            attempts += 1
            i, j = random.randrange(ligne), random.randrange(colonne)
            if not is_valid(i, j):
                continue

            # Commence la zone
            zone = [(i, j)]
            grid[i][j] = color

            # Expansion aléatoire
            while len(zone) < size:
                ci, cj = random.choice(zone)

                #Choisir une direction de la zone
                di, dj = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                ni, nj = ci + di, cj + dj
                if is_valid(ni, nj):
                    grid[ni][nj] = color
                    zone.append((ni, nj))
                else:
                    break # Evite boucle infinie

            return True
        return False

    # Placer 2 zones de 6 cases pour chaque type de terrain (essaie)
    for name, color in terrains.items():
        for _ in range(2):  # deux zones
            ok = place_zone(color, 6) # taille zone
            if not ok :
                print(f"Impossible de placer cette zonne pour {name}")

    
    # Création des cases
    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = int(WIDTH * 0.25) + j * taille
            y = int(HEIGHT * 0.1) + i * taille
            rect = pg.Rect(x, y, taille, taille)

            couleur = grid[i][j] if grid[i][j] is not None else (191, 183, 161) # Couleur par défault
            case_original.append((rect, couleur))


    print(len(case_original))
    return BCOLOR, case_original

# ------------------------------------------------------- #