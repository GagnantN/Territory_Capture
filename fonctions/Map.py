import pygame as pg
import random
import os
from fonctions.cases import terrains



# ----------------- COULEUR JOUEURS --------------------- #
joueur_01 = (70, 130, 180)   # Bleu acier
joueur_02 = (178, 34, 3)     # Rouge brique
central_color = (255, 165, 0)  # orange pour la ville au centre
# ------------------------------------------------------- #



# ----------------- CHARGEMENT DES TEXTURES ------------- #
IMAGE_PATH = "Images"
textures = {
    "eau": pg.image.load(os.path.join(IMAGE_PATH, "Eau.png")).convert(),
    "roche": pg.image.load(os.path.join(IMAGE_PATH, "Roche.png")).convert(),
    "foret": pg.image.load(os.path.join(IMAGE_PATH, "Foret.png")).convert(),
    "sable": pg.image.load(os.path.join(IMAGE_PATH, "Sable.png")).convert(),
}
# ------------------------------------------------------- #



def create_map(screen):
    WIDTH, HEIGHT = screen.get_size()
    BCOLOR = (50, 50, 50)

    ligne, colonne = 21, 21
    taille = min(WIDTH // (colonne + 5), HEIGHT // (ligne + 5))
    total_width = colonne * taille
    total_height = ligne * taille
    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2

    grid = [[None for _ in range(colonne)] for _ in range(ligne)]
    grid_owner = [[0 for _ in range(colonne)] for _ in range(ligne)]
    grid_points = [[10 for _ in range(colonne)] for _ in range(ligne)]


    # ---------- Placement zone centrale 3x3 ----------
    ci = ligne // 2
    cj = colonne // 2
    for di in (-1,0,1):
        for dj in (-1,0,1):
            ni, nj = ci+di, cj+dj
            if 0 <= ni < ligne and 0 <= nj < colonne:
                grid[ni][nj] = central_color
                grid_points[ni][nj] = 50


    # ----------------- Placement joueurs ----------------------
    # ------------------- Placement Terrain --------------------
    areas = [(0,4,"GAUCHE"), (5,14,"CENTRE"), (15,19,"DROITE")]

    def candidate_ok(i,j,color):
        if not (0 <= i < ligne and 0 <= j < colonne):
            return False
        if grid[i][j] is not None:
            return False
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                ni, nj = i+di, j+dj
                if 0<=ni<ligne and 0<=nj<colonne:
                    nc = grid[ni][nj]
                    if nc is not None and nc != color:
                        return False
        return True



    def place_zone(color, size, zone_min_col=None, zone_max_col=None, attempts_limit=1000):
        attempts = 0
        while attempts < attempts_limit:
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(zone_min_col if zone_min_col is not None else 0,
                               zone_max_col if zone_max_col is not None else colonne-1)
            if zone_min_col is not None and zone_max_col is not None:
                if not (zone_min_col <= j <= zone_max_col):
                    continue
            if not candidate_ok(i,j,color):
                continue
            zone = [(i,j)]
            grid[i][j] = color
            while len(zone) < size:
                frontier = []
                for (ci,cj) in zone:
                    for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                        ni, nj = ci+di, cj+dj
                        if zone_min_col is not None and zone_max_col is not None:
                            if not (zone_min_col <= nj <= zone_max_col):
                                continue
                        if candidate_ok(ni,nj,color):
                            frontier.append((ni,nj))
                if not frontier:
                    break
                ni,nj = random.choice(frontier)
                grid[ni][nj] = color
                zone.append((ni,nj))
            if len(zone) >= size:
                return True
            for x,y in zone:
                grid[x][y] = None
        return False


    # Placer les zones de terrain
    for min_col,max_col,label in areas:
        for name, color in terrains.items():
            size = random.randint(4,7)
            ok = place_zone(color, size, min_col, max_col, 2000)



    # ----------------- Placement joueurs ----------------------
    def place_player(color, min_lin,max_lin,min_col,max_col):
        for _ in range(1000):
            i = random.randrange(min_lin,max_lin)
            j = random.randint(min_col,max_col)
            if grid[i][j] is not None:
                continue
            ok = True
            for di in [-1,0,1]:
                for dj in [-1,0,1]:
                    ni,nj = i+di,j+dj
                    if 0<=ni<ligne and 0<=nj<colonne and grid[ni][nj] is not None:
                        ok=False
                        break
                if not ok: break
            if ok:
                grid[i][j]=color
                grid_owner[i][j] = 1 if color == joueur_01 else 2
                return (i,j)
        return None


    def expand_player_zone(grid, grid_owner, pos, color, owner_id):
        if pos is None: return
        i,j = pos
        for di in (-1,0,1):
            for dj in (-1,0,1):
                ni,nj = i+di,j+dj
                if 0<=ni<ligne and 0<=nj<colonne:
                    if grid[ni][nj] is None:
                        grid[ni][nj] = color
                        grid_owner[ni][nj] = owner_id

    pos_joueur_1 = place_player(joueur_01, 1, 18, 1, 3)
    pos_joueur_2 = place_player(joueur_02, 1, 18, 16, 18)
    expand_player_zone(grid, grid_owner, pos_joueur_1, joueur_01, 1)
    expand_player_zone(grid, grid_owner, pos_joueur_2, joueur_02, 2)

    joueurs_data = {1: {"spawn": pos_joueur_1}, 2: {"spawn": pos_joueur_2}}



    # ----------------- Convertir en rects + textures ----------------
    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = offset_x + j*taille
            y = offset_y + i*taille
            rect = pg.Rect(x,y,taille,taille)
            cell = grid[i][j]  # tuple couleur ou central_color or player color

            # MAPPER les couleurs terrain vers les textures
            if cell == terrains.get("eau"):
                texture = pg.transform.scale(textures["eau"], (taille,taille))
            elif cell == terrains.get("montagne"):
                # la texture "roche" correspond à la couleur "montagne"
                texture = pg.transform.scale(textures["roche"], (taille,taille))
            elif cell == terrains.get("foret"):
                texture = pg.transform.scale(textures["foret"], (taille,taille))
            elif cell == terrains.get("bordure"):
                texture = pg.transform.scale(textures["sable"], (taille,taille))
            else:
                # joueur ou centre ou None -> surface colorée
                texture = pg.Surface((taille,taille))
                # si cell est None on met une couleur par défaut
                texture.fill(cell if cell is not None else (191,183,161))

            # NOTE: on stocke aussi 'cell' pour pouvoir faire des tests (terrains.values()) plus tard
            case_original.append((rect, texture, grid_owner[i][j], cell))

    return BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y, grid_points, joueurs_data


def handle_click(mouse_pos, case_original, joueur_id, joueurs, taille, offset_x, offset_y, grid_points, joueurs_data):
    """
    Gère le clic sur la carte.
    case_original contient maintenant des tuples (rect, surface, owner, cell_value)
    """
    if joueurs[joueur_id]["tickets"] <= 0:
        return False  # pas de ticket -> rien

    largeur = int(len(grid_points))  # normalement 21
    for idx, (rect, surface, owner, cell) in enumerate(case_original):
        if rect.collidepoint(mouse_pos):

            # Convertir index en coordonnées (i, j)
            i, j = divmod(idx, largeur)

            # 1) Vérifie si c'est un terrain, la propre zone du joueur, ou son propre spawn → interdit
            if cell in terrains.values() or owner == joueur_id or (i, j) == joueurs_data[joueur_id]["spawn"]:
                return False

            # 2) Vérifie si adjacent à une case du joueur
            if not est_adjacent(case_original, idx, joueur_id, taille, offset_x, offset_y):
                return False

            # 3) Gestion capture d'une case adverse
            if owner != 0 and owner != joueur_id:
                # Capture d'un spawn adverse → victoire
                if (i, j) == joueurs_data[owner]["spawn"]:
                    return "VICTOIRE", owner

                # Sinon, retirer les points normalement
                if owner in joueurs:
                    joueurs[owner]["points"] -= grid_points[i][j]
                    if joueurs[owner]["points"] < 0:
                        joueurs[owner]["points"] = 0  # éviter négatif

            # 4) Capturer la case : créer une surface colorée pour le joueur
            new_color = joueurs[joueur_id]["color"]
            new_surface = pg.Surface((taille, taille))
            new_surface.fill(new_color)
            # on garde aussi la valeur cell = new_color
            case_original[idx] = (rect, new_surface, joueur_id, new_color)

            joueurs[joueur_id]["tickets"] -= 1
            joueurs[joueur_id]["points"] += grid_points[i][j]

            return True

    return False  # Aucun clic valide


def est_adjacent(case_original, idx, joueur_id, taille, offset_x, offset_y):
    # Reconvertir l’index en (i,j)
    largeur = int((len(case_original)) ** 0.5)  # puisque carré 21x21
    i, j = divmod(idx, largeur)

    voisins = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    for vi, vj in voisins:
        if 0 <= vi < largeur and 0 <= vj < largeur:
            v_idx = vi * largeur + vj
            # case_original[v_idx] = (rect, surface, owner, cell)
            _, _, owner, _ = case_original[v_idx]
            if owner == joueur_id:
                return True
    return False

def afficher_victoire(screen, gagnant, largeur, hauteur):
    font = pg.font.SysFont("arial", 72, bold=True)
    petit_font = pg.font.SysFont("arial", 40)

    message = f"Le joueur {gagnant} a gagné la partie !"
    texte = font.render(message, True, (255, 255, 0))

    sous_texte = petit_font.render("Cliquez pour continuer", True, (255, 255, 255))

    overlay = pg.Surface((largeur, hauteur), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # fond semi-transparent
    screen.blit(overlay, (0, 0))
    screen.blit(texte, (largeur//2 - texte.get_width()//2, hauteur//2 - texte.get_height()//2))
    screen.blit(sous_texte, (largeur//2 - sous_texte.get_width()//2, hauteur//2 + 80))

    pg.display.flip()

    # Attente blocante
    attente = True
    while attente:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.MOUSEBUTTONDOWN, pg.KEYDOWN):
                attente = False
