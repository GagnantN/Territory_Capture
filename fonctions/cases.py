import pygame as pg

# Ecran Fullscreen
screen = pg.display.set_mode(((0, 0)), pg.FULLSCREEN)
# Récupère la taille actuelle de la fenêtre
WIDTH, HEIGHT = screen.get_size()
ligne = 20
colonne = 20
taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))  # taille d’une case



# ----------------- COULEUR TERRAINS -------------------- #
terrains = {
    "eau" : (50, 100, 200),
    "montagne" : (120, 120, 120),
    "foret" : (200, 200, 150),
    "bordure" : (0, 42, 9),
}

'''
# ------------------------------------------------------- #

# ----------------- COULEUR JOUEURS  -------------------- #
joueur_01 = (70, 130, 180)
joueur_02 = (178, 34, 3)

# ------------------------------------------------------- #




# ------------------------ EAU -------------------------- #
def create_eau():
    WCOLOR = eau
    BCOLOR = (50, 50, 50)

    case = []
    taille  # taille d’une case

    return WCOLOR, BCOLOR, case, taille
# ------------------------------------------------------- #




# --------------------- MONTAGNE ------------------------ #
def create_montagne():
    WCOLOR = montagne
    BCOLOR = (50, 50, 50)

    case = []
    taille  # taille d’une case

    return WCOLOR, BCOLOR, case, taille
# ------------------------------------------------------- #




# ----------------------- FORET ------------------------- #
def create_foret():
    WCOLOR = foret
    BCOLOR = (50, 50, 50)

    case = []
    taille  # taille d’une case

    return WCOLOR, BCOLOR, case, taille
# ------------------------------------------------------- #



# Case Joueur

# ----------------------- JOUEUR 01 --------------------- #
def create_joueur_01():
    WCOLOR = joueur_01
    BCOLOR = (50, 50, 50)

    case = []
    taille  # taille d’une case

    return WCOLOR, BCOLOR, case, taille
# ------------------------------------------------------- #

# ----------------------- JOUEUR 02 --------------------- #
def create_joueur_02():
    WCOLOR = joueur_02
    BCOLOR = (50, 50, 50)

    case = []
    taille  # taille d’une case

    return WCOLOR, BCOLOR, case, taille
# ------------------------------------------------------- #
'''