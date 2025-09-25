# fonctions/Map.py
import pygame as pg
import random
from fonctions.cases import terrains



# ----------------- COULEUR JOUEURS -------------------- #
joueur_01 = (70, 130, 180)   # Bleu acier
joueur_02 = (178, 34, 3)     # Rouge brique
# ------------------------------------------------------- #
central_color = (255, 165, 0)  # orange pour la ville au centre
# ------------------------------------------------------- #



def create_map(screen):
    WIDTH, HEIGHT = screen.get_size()
    BCOLOR = (50, 50, 50)

    ligne, colonne = 21, 21
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))
    # calcule les marges pour centrer la grille
    total_width = colonne * taille
    total_height = ligne * taille
    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2


    # grille logique : None ou couleur (tuple)
    grid = [[None for _ in range(colonne)] for _ in range(ligne)]
    # Ajoute une structure grid_owner parallèle à grid
    grid_owner = [[0 for _ in range(colonne)] for _ in range(ligne)]
    # Ajoute une structure grid_owner parallèle à grid
    grid_points = [[10 for _ in range(colonne)] for _ in range(ligne)]


    # helper : vérifier qu'une case candidate est libre et qu'elle n'a pas
    # de voisin d'une couleur différente (pour garantir l'espace d'une case)
    def candidate_ok(i, j, color):
        if not (0 <= i < ligne and 0 <= j < colonne):
            return False
        if grid[i][j] is not None:
            return False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < ligne and 0 <= nj < colonne:
                    nc = grid[ni][nj]
                    if nc is not None and nc != color:
                        # voisin d'une autre couleur → interdit
                        return False
        return True

    # place une zone contiguë de 'size' cases, en autorisant uniquement
    # des cases qui n'ont pas de voisins d'autres couleurs
    def place_zone(color, size, zone_min_col=None, zone_max_col=None, attempts_limit=1000):
        attempts = 0
        while attempts < attempts_limit:
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(zone_min_col if zone_min_col is not None else 0,
                               zone_max_col if zone_max_col is not None else colonne - 1)
            # respecter la colonne demandée
            if zone_min_col is not None and zone_max_col is not None:
                if not (zone_min_col <= j <= zone_max_col):
                    continue

            if not candidate_ok(i, j, color):
                continue

            # init zone
            zone = [(i, j)]
            grid[i][j] = color

            # expansion par "frontier" : on collecte toutes les cases adjacentes valides
            while len(zone) < size:
                frontier = []
                for (ci, cj) in zone:
                    for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                        ni, nj = ci + di, cj + dj
                        # respecter limite colonnes si fournie
                        if zone_min_col is not None and zone_max_col is not None:
                            if not (zone_min_col <= nj <= zone_max_col):
                                continue
                        if candidate_ok(ni, nj, color):
                            frontier.append((ni, nj))
                if not frontier:
                    break  # plus de place pour grandir
                ni, nj = random.choice(frontier)
                grid[ni][nj] = color
                zone.append((ni, nj))

            if len(zone) >= size:
                return True

            # rollback si on n'a pas atteint la taille
            for x, y in zone:
                grid[x][y] = None

        return False
    

    # ---------------------------
    # 1) placer la zone centrale 3x3 (orange) et les joueurs 3x3 (bleu et rouge)
    # ---------------------------
    ci = ligne // 2
    cj = colonne // 2
    # indices pour 3x3 (vérifie les bords juste au cas où)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni, nj = ci + di, cj + dj
            if 0 <= ni < ligne and 0 <= nj < colonne:
                grid[ni][nj] = central_color
                grid_points[ni][nj] = 50
    print("[CENTER] 3x3 centrale placée")

    # ---------------------------
    # 2) placer au moins 1 zone de chaque terrain dans GAUCHE / CENTRE / DROITE
    # zones de colonnes : gauche 0-4, centre 5-14, droite 15-19
    # taille aléatoire entre 4 et 7
    # ---------------------------
    areas = [
        (0, 4, "GAUCHE"),
        (5, 14, "CENTRE"),
        (15, 19, "DROITE"),
    ]

    for min_col, max_col, label in areas:
        for name, color in terrains.items():
            size = random.randint(4, 7)
            ok = place_zone(color, size, zone_min_col=min_col, zone_max_col=max_col, attempts_limit=2000)
            if ok:
                print(f"[{label}] {name} taille {size} placé")
            else:
                print(f"[{label}] échec placement {name} taille {size}")

    # ---------------------------
    # 3) placer joueurs : chercher une case vraiment vide (et séparée)
    # ---------------------------
    # Génére une zone autour des joueurs
    def place_player(color, min_lin, max_lin, min_col, max_col):
        for _ in range(1000):
            i = random.randrange(min_lin, max_lin)
            j = random.randint(min_col, max_col)
            # ici on veut une case ayant aucun voisin occupé (safe spawn)
            if not (0 <= i < ligne and 0 <= j < colonne):
                continue
            if grid[i][j] is not None:
                continue
            ok = True
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < ligne and 0 <= nj < colonne:
                        if grid[ni][nj] is not None:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                grid[i][j] = color
                grid_owner[i][j] = i if color == joueur_01 else 2
                return (i, j)
        return None
    
    def expand_player_zone(grid, grid_owner, pos, color, owner_id):
        """Crée une zone 3x3 autour de la position du joueur."""
        if pos is None:
            return
        i, j = pos
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ni, nj = i + di, j + dj
                if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                    # On écrase seulement si la case est vide (None)
                    if grid[ni][nj] is None:
                        grid[ni][nj] = color
                        grid_owner[ni][nj] = owner_id



    pos_joueur_1 = place_player(joueur_01, 1, 18, 1, 3)
    pos_joueur_2 = place_player(joueur_02, 1, 18, 16, 18)

    # Étendre leur zone perso 3x3
    expand_player_zone(grid, grid_owner, pos_joueur_1, joueur_01, 1)
    expand_player_zone(grid, grid_owner, pos_joueur_2, joueur_02, 2)
    print(f"Players placed: {pos_joueur_1}, {pos_joueur_2}")


    # ---------------------------
    # 4) convertir en liste de rects + couleurs
    # ---------------------------
    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = offset_x + j * taille
            y = offset_y + i * taille
            rect = pg.Rect(x, y, taille, taille)
            couleur = grid[i][j] if grid[i][j] is not None else (191, 183, 161)
            case_original.append((rect, couleur, grid_owner[i][j]))

    print(f"Total cases créées : {len(case_original)}")
    # retourne aussi la taille utile pour dessiner les joueurs facilement
    return BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y, grid_points




def handle_click(mouse_pos, case_original, joueur_id, joueurs, taille, offset_x, offset_y, grid_points):
    """
    mouse_pos: position du clic
    case_original: liste [(rect, couleur, owner)]
    joueur_id: 1 ou 2
    joueurs: dict interface.joueurs
    grid_points: grille contenant la valeur en points de chaque case
    """

    if joueurs[joueur_id]["tickets"] <= 0:
        return False  # pas de ticket -> rien

    largeur = int(len(grid_points))  # Taille d'une ligne = 21
    for idx, (rect, couleur, owner) in enumerate(case_original):
        if rect.collidepoint(mouse_pos):

            # --- Convertir index en (i, j) ---
            i, j = divmod(idx, largeur)

            # 1) Vérifie si la case est un terrain ou deja capturer par le même joueur → capture interdite
            if couleur in terrains.values():
                return False

            # 2) Vérifie si adjacent à une case du joueur
            if not est_adjacent(case_original, idx, joueur_id, taille, offset_x, offset_y):
                return False

            # 3) Gestion capture d'une case adverse
            if owner != 0 and owner != joueur_id:
                # Retirer les points à l'ancien propriétaire
                joueurs[owner]["points"] -= grid_points[i][j]
                if joueurs[owner]["points"] < 0:
                    joueurs[owner]["points"] = 0  # Sécurité pour éviter des points négatifs

            # 4) Capturer la case
            new_color = joueurs[joueur_id]["color"]
            case_original[idx] = (rect, new_color, joueur_id)

            joueurs[joueur_id]["tickets"] -= 1
            joueurs[joueur_id]["points"] += grid_points[i][j]

            return True

    return False  # aucun clic valide




def est_adjacent(case_original, idx, joueur_id, taille, offset_x, offset_y):
    # Reconvertir l’index en (i,j)
    largeur = int((len(case_original)) ** 0.5)  # puisque carré 21x21
    i, j = divmod(idx, largeur)

    voisins = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    for vi, vj in voisins:
        if 0 <= vi < largeur and 0 <= vj < largeur:
            v_idx = vi * largeur + vj
            _, _, owner = case_original[v_idx]
            if owner == joueur_id:
                return True
    return False
