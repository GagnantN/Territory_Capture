# ----------------- COULEUR TERRAINS -------------------- #
eau = (50, 100, 200)
montagne = (120, 120, 120)
foret = (200, 200, 150)
bordure = (0, 42, 9)

# ------------------------------------------------------- #




# ------------------------ EAU -------------------------- #
def create_eau():
    WCOLOR = eau
    BCOLOR = (50, 50, 50)

    walls = []
    taille = 20  # taille d’une case

    return WCOLOR, BCOLOR, walls, taille
# ------------------------------------------------------- #




# --------------------- MONTAGNE ------------------------ #
def create_montagne():
    WCOLOR = montagne
    BCOLOR = (50, 50, 50)

    walls = []
    taille = 20  # taille d’une case

    return WCOLOR, BCOLOR, walls, taille
# ------------------------------------------------------- #




# ----------------------- FORET ------------------------- #
def create_foret():
    WCOLOR = foret
    BCOLOR = (50, 50, 50)

    walls = []
    taille = 20  # taille d’une case

    return WCOLOR, BCOLOR, walls, taille
# ------------------------------------------------------- #

