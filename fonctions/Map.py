import pygame as pg
import random
from fonctions.cases import terrains



# ----------------- COULEUR JOUEURS -------------------- #
joueur_01 = (70, 130, 180)   # Bleu acier
joueur_02 = (178, 34, 3)     # Rouge brique
# ------------------------------------------------------- #



def create_map(screen):
    WIDTH, HEIGHT = screen.get_size()
    BCOLOR = (50, 50, 50)

    ligne = 20
    colonne = 20
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))  # taille d’une case

    # Grille vide
    grid = [[None for _ in range(colonne)] for _ in range(ligne)]



    # -------- Vérifie qu'une case est libre + espacement -------- #
    def is_valid(i, j, zone_min_col=None, zone_max_col=None, strict=True):
        """
        Vérifie si la case est libre, respecte l'espacement et reste dans une zone de colonnes optionnelle.
        """
        if not (0 <= i < ligne and 0 <= j < colonne):
            return False

        # Case déjà occupée
        if grid[i][j] is not None:
            return False

        # Limite aux colonnes définies
        if zone_min_col is not None and zone_max_col is not None:
            if not (zone_min_col <= j <= zone_max_col):
                return False

        # Vérifie qu'aucune case voisine n'est occupée
        if strict:
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < ligne and 0 <= nj < colonne:
                        if grid[ni][nj] is not None:
                            return False
        return True



    # -------- Générer une zone contiguë -------- #
    def place_zone(color, size, zone_min_col=None, zone_max_col=None, strict=True):
        """
        Place une zone contiguë dans une plage de colonnes (si définie).
        """
        attempts = 0
        while attempts < 1000:  # éviter boucle infinie
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(zone_min_col if zone_min_col is not None else 0,
                               zone_max_col if zone_max_col is not None else colonne - 1)

            if not is_valid(i, j, zone_min_col, zone_max_col, strict):
                continue

            zone = [(i, j)]
            grid[i][j] = color

            # Expansion aléatoire
            while len(zone) < size:
                ci, cj = random.choice(zone)
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)

                placed = False
                for di, dj in directions:
                    ni, nj = ci + di, cj + dj
                    if is_valid(ni, nj, zone_min_col, zone_max_col, strict=False):
                        grid[ni][nj] = color
                        zone.append((ni, nj))
                        placed = True
                        break

                if not placed:  # aucune extension possible
                    break

            if len(zone) == size:
                return True

            # Sinon, reset
            for x, y in zone:
                grid[x][y] = None

        return False



    # -------- Placement des obstacles dans les zones de spawn -------- #
    def place_spawn_obstacles(min_col, max_col):
        """
        Place exactement 1 zone de chaque type dans une zone de spawn.
        """
        for name, color in terrains.items():
            ok = place_zone(color, 6, zone_min_col=min_col, zone_max_col=max_col, strict=True)
            if ok:
                print(f"[SPAWN] Zone placée pour {name} ({min_col}-{max_col})")
            else:
                print(f"[SPAWN] Impossible de placer {name} ({min_col}-{max_col})")

    # Joueur 1 → colonnes 0-4
    place_spawn_obstacles(0, 4)

    # Joueur 2 → colonnes 15-19
    place_spawn_obstacles(15, 19)



    # -------- Placement du reste des zones dans la zone centrale -------- #
    for name, color in terrains.items():
        for z in range(4):  # nombre de zones centrales
            ok = place_zone(color, 6, zone_min_col=5, zone_max_col=14, strict=True)
            if ok:
                print(f"[CENTRAL] Zone placée pour {name} #{z+1}")
            else:
                print(f"[CENTRAL] Impossible de placer {name} #{z+1}")



    # -------- Placement des joueurs -------- #
    def place_player(color, min_col, max_col):
        """
        Place un joueur dans une case vide avec une zone de sécurité autour.
        """
        attempts = 0
        while attempts < 500:
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(min_col, max_col)

            if is_valid(i, j, zone_min_col=min_col, zone_max_col=max_col, strict=True):
                grid[i][j] = color
                print(f"Joueur placé en ({i},{j}) - {color}")
                return (i, j)

        print(f"Impossible de placer le joueur {color} après {attempts} tentatives")
        return None



    # Joueur 1 à gauche
    pos_joueur_1 = place_player(joueur_01, 0, 4)



    # Joueur 2 à droite
    pos_joueur_2 = place_player(joueur_02, 15, 19)



    # -------- Création des cases -------- #
    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = int(WIDTH * 0.25) + j * taille
            y = int(HEIGHT * 0.1) + i * taille
            rect = pg.Rect(x, y, taille, taille)

            couleur = grid[i][j] if grid[i][j] is not None else (191, 183, 161)
            case_original.append((rect, couleur))

    print(f"Total cases créées : {len(case_original)}")
    return BCOLOR, case_original, pos_joueur_1, pos_joueur_2
