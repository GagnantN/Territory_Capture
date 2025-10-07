import pygame as pg, sys
import random
import os
from fonctions.cases import terrains, get_reachable_cells, find_path

# ----------------- COULEUR JOUEURS --------------------- #
joueur_01 = (70, 130, 180)   # Bleu acier
joueur_02 = (178, 34, 3)     # Rouge brique
central_color = (255, 165, 0)
muraille_color = (100, 100, 100)  # gris foncé
# ------------------------------------------------------- #

# Déplacements d’unités
selected_unit = None
reachable_cells = []
current_path = []
animating_move = None
dragging = False

# ----------------- CHARGEMENT DES TEXTURES ------------- #
IMAGE_PATH = "Images"
textures = {
    "eau": pg.image.load(os.path.join(IMAGE_PATH, "Eau.png")),
    "roche": pg.image.load(os.path.join(IMAGE_PATH, "Roche.png")),
    "foret": pg.image.load(os.path.join(IMAGE_PATH, "Foret.png")),
    "sable": pg.image.load(os.path.join(IMAGE_PATH, "Sable.png")),
}
# ------------------------------------------------------- #

def darker_color(color, factor=0.6):
    r, g, b = color
    return (int(r*factor), int(g*factor), int(b*factor))

# NOTE: make_case must return 5-tuple to match case_original throughout the code.
def make_case(rect, couleur, owner, cell, taille, is_terrain=False):
    surface = pg.Surface((taille, taille))
    surface.fill(couleur)
    return (rect, surface, owner, cell, is_terrain)

# ------------------------------------------------------- #
# Création de la map
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
    global murailles
    murailles = set()  # Vider la cache de la muraille


    grid = [[None for _ in range(colonne)] for _ in range(ligne)]
    grid_owner = [[0 for _ in range(colonne)] for _ in range(ligne)]
    grid_points = [[10 for _ in range(colonne)] for _ in range(ligne)]

    # --- zone centrale 3x3 ---
    ci, cj = ligne // 2, colonne // 2
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni, nj = ci + di, cj + dj
            grid[ni][nj] = central_color
            grid_points[ni][nj] = 50

    # --- génération terrains (inchangée) ---
    areas = [(0, 4, "GAUCHE"), (5, 14, "CENTRE"), (15, 19, "DROITE")]

    def candidate_ok(i, j, color):
        if not (0 <= i < ligne and 0 <= j < colonne):
            return False
        if grid[i][j] is not None:
            return False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < ligne and 0 <= nj < colonne and grid[ni][nj] not in [None, color]:
                    return False
        return True

    def place_zone(color, size, zone_min_col=None, zone_max_col=None, attempts_limit=1000):
        attempts = 0
        while attempts < attempts_limit:
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(zone_min_col if zone_min_col else 0,
                               zone_max_col if zone_max_col else colonne - 1)
            if zone_min_col is not None and zone_max_col is not None and not (zone_min_col <= j <= zone_max_col):
                continue
            if not candidate_ok(i, j, color):
                continue
            zone = [(i, j)]
            grid[i][j] = color
            while len(zone) < size:
                frontier = []
                for ci, cj in zone:
                    for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        ni, nj = ci + di, cj + dj
                        if zone_min_col is not None and zone_max_col is not None and not (zone_min_col <= nj <= zone_max_col):
                            continue
                        if candidate_ok(ni, nj, color):
                            frontier.append((ni, nj))
                if not frontier:
                    break
                ni, nj = random.choice(frontier)
                grid[ni][nj] = color
                zone.append((ni, nj))
            if len(zone) >= size:
                return True
            for x, y in zone:
                grid[x][y] = None
        return False

    for min_col, max_col, label in areas:
        for name, color in terrains.items():
            size = random.randint(4, 7)
            place_zone(color, size, zone_min_col=min_col, zone_max_col=max_col, attempts_limit=2000)

    # --- placement joueurs ---
    def is_near_terrain(grid, i, j, distance=2):
        nrows, ncols = len(grid), len(grid[0])
        for di in range(-distance, distance + 1):
            for dj in range(-distance, distance + 1):
                ni, nj = i + di, j + dj
                if 0 <= ni < nrows and 0 <= nj < ncols:
                    if grid[ni][nj] in terrains.values():
                        return True
        return False

    def place_player(color, min_lin, max_lin, min_col, max_col):
        for _ in range(1000):
            i = random.randrange(min_lin, max_lin)
            j = random.randint(min_col, max_col)
            if grid[i][j] is None and not is_near_terrain(grid, i, j, distance=2):
                grid[i][j] = color
                grid_owner[i][j] = 1 if color == joueur_01 else 2
                return (i, j)
        # Si aucun spawn valide trouvé → fallback forcé
        return (min_lin, min_col)


    def expand_player_zone(pos, color, owner_id):
        captured = []
        if pos:
            i, j = pos
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < ligne and 0 <= nj < colonne and grid[ni][nj] is None:
                        grid[ni][nj] = color
                        grid_owner[ni][nj] = owner_id
                        captured.append((ni, nj))
        return captured

    # élargissement des zones
    pos_j1 = place_player(joueur_01, 1, 18, 1, 5)
    pos_j2 = place_player(joueur_02, 1, 18, 15, 19)
    spawn_zone_1 = expand_player_zone(pos_j1, joueur_01, 1)
    spawn_zone_2 = expand_player_zone(pos_j2, joueur_02, 2)
    joueurs_data = {1: {"spawn": pos_j1}, 2: {"spawn": pos_j2}}
    # Construire murailles
    construire_muraille_autour(murailles, ci, cj, taille_zone=3)        # cité centrale
    if pos_j1:
        construire_muraille_autour(murailles, pos_j1[0], pos_j1[1], taille_zone=3)  # spawn joueur 1
    if pos_j2:
        construire_muraille_autour(murailles, pos_j2[0], pos_j2[1], taille_zone=3)  # spawn joueur 2



    unites = {1: [], 2: []}
    def add_unite(player_id, base_pos, offsets):
        if base_pos:
            i, j = base_pos
            for di, dj in offsets:
                ni, nj = i + di, j + dj
                if 0 <= ni < ligne and 0 <= nj < colonne:
                    unites[player_id].append((ni, nj))
    add_unite(1, pos_j1, [(-1, 0), (0, 1), (1, 0)])
    add_unite(2, pos_j2, [(-1, 0), (1, 0), (0, -1)])

    # --- case_original avec is_terrain ---
    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = offset_x + j * taille
            y = offset_y + i * taille
            rect = pg.Rect(x, y, taille, taille)
            cell = grid[i][j]

            # détecter si c’est un terrain bloquant
            is_terrain = cell in terrains.values()

            if cell == terrains.get("eau"):
                texture = pg.transform.scale(textures["eau"], (taille, taille))
            elif cell == terrains.get("montagne"):
                texture = pg.transform.scale(textures["roche"], (taille, taille))
            elif cell == terrains.get("foret"):
                texture = pg.transform.scale(textures["foret"], (taille, taille))
            elif cell == terrains.get("bordure"):
                texture = pg.transform.scale(textures["sable"], (taille, taille))
            else:
                texture = pg.Surface((taille, taille))
                texture.fill(cell if cell else (191, 183, 161))

            case_original.append((rect, texture, grid_owner[i][j], cell, is_terrain))

    return BCOLOR, case_original, pos_j1, pos_j2, textures, taille, offset_x, offset_y, grid_points, joueurs_data, spawn_zone_1, spawn_zone_2, unites, grid, murailles


def handle_click(mouse_pos, case_original, joueur_id, joueurs, taille, offset_x, offset_y, grid_points, joueurs_data):
    """
    Gère le clic sur la carte.
    case_original contient maintenant des tuples (rect, surface, owner, cell_value, is_terrain)
    """
    if joueurs[joueur_id]["tickets"] <= 0:
        return False

    nrows = len(grid_points)
    ncols = len(grid_points[0]) if nrows > 0 else 0
    for idx, (rect, couleur, owner, cell, is_terrain) in enumerate(case_original):
        if rect.collidepoint(mouse_pos):
            i, j = divmod(idx, ncols)
            # empêcher d'acheter une case terrain / sa propre case / spawn personnel
            if couleur in textures.values() or owner == joueur_id or (i, j) == joueurs_data[joueur_id]["spawn"]:
                return False
            if not est_adjacent(case_original, idx, joueur_id):
                return False
            if owner != 0 and owner != joueur_id:
                if (i, j) == joueurs_data[owner]["spawn"]:
                    return "VICTOIRE", owner
                if owner in joueurs:
                    joueurs[owner]["points"] -= grid_points[i][j]
                    joueurs[owner]["points"] = max(0, joueurs[owner]["points"])
            new_color = joueurs[joueur_id]["color"]
            case_original[idx] = make_case(rect, new_color, joueur_id, cell, taille, is_terrain=False)
            joueurs[joueur_id]["tickets"] -= 1
            joueurs[joueur_id]["points"] += grid_points[i][j]
            return True
    return False


def est_adjacent(case_original, idx, joueur_id):
    largeur = int((len(case_original)) ** 0.5)
    i, j = divmod(idx, largeur)
    voisins = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    for vi, vj in voisins:
        if 0 <= vi < largeur and 0 <= vj < largeur:
            v_idx = vi * largeur + vj
            # case_original[v_idx] = (rect, surface, owner, cell, is_terrain)
            _, _, owner, _, _ = case_original[v_idx]
            if owner == joueur_id:
                return True
    return False


# ------------------------------------------------------- #
# Déplacements d’unités (drag & drop + zones de mouvement)
# ------------------------------------------------------- #
selected_unit = None
dragging = False
reachable_cells = []


def darker_color(color, factor=0.6):
    r, g, b = color
    return (int(r * factor), int(g * factor), int(b * factor))


def handle_unit_events(event, unites, joueur_actif, interface,
                       offset_x, offset_y, taille, grid_points, case_original, terrain_grid):
    """
    Sélection et déplacement des unités du joueur actif.
    """
    global selected_unit, reachable_cells, current_path, animating_move, dragging

    unite_size = int(taille * 0.7)
    mouse_x, mouse_y = pg.mouse.get_pos()
    grid_i = (mouse_y - offset_y) // taille
    grid_j = (mouse_x - offset_x) // taille

    # --- Clic gauche pressé : sélection de l'unité ---
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if not selected_unit:
            positions = unites[joueur_actif]
            for idx, (i, j) in enumerate(positions):
                ux = offset_x + j * taille + (taille - unite_size) // 2
                uy = offset_y + i * taille + (taille - unite_size) // 2
                rect_unit = pg.Rect(ux, uy, unite_size, unite_size)
                if rect_unit.collidepoint(mouse_x, mouse_y):
                    if interface.joueurs[joueur_actif]["tickets"] >= 1:
                        selected_unit = (joueur_actif, idx)

                        # ==> calcul correct des cellules atteignables :
                        # on passe grid_points (dimension) et on interdit les terrains (terrains.values()).
                        forbidden = list(terrains.values()) + [muraille_color]
                        reachable_cells = set(get_reachable_cells((i, j), 5, grid_points, forbidden, case_original, murailles))

                        current_path = [(i, j)]
                        dragging = True
                        return True

    # --- Drag souris : ajouter au chemin si adjacent ---
    if event.type == pg.MOUSEMOTION and dragging and selected_unit:
        joueur_id, idx = selected_unit
        nrows, ncols = len(terrain_grid), len(terrain_grid[0])
        if 0 <= grid_i < nrows and 0 <= grid_j < ncols:
            last_i, last_j = current_path[-1]
            if abs(grid_i - last_i) + abs(grid_j - last_j) == 1:  # case adjacente
                # --- Si on revient en arrière ---
                if len(current_path) > 1 and (grid_i, grid_j) == current_path[-2]:
                    current_path.pop()  # on enlève la dernière case
                    return True

                # --- Sinon on avance ---
                if (grid_i, grid_j) not in current_path and (grid_i, grid_j) in reachable_cells:
                    # Limite de 5 mouvements (donc 6 cases dans current_path)
                    if len(current_path) < 6:
                        current_path.append((grid_i, grid_j))
        return True

    # --- Relâcher clic gauche : valider déplacement ---
    if event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging:
        if selected_unit and len(current_path) > 1:
            joueur_id, idx = selected_unit
            animating_move = (joueur_id, idx, current_path, 0)
            interface.joueurs[joueur_id]["tickets"] -= 1
        # Reset sélection
        selected_unit = None
        dragging = False
        reachable_cells = []
        current_path = []
        return True

    # --- Clic droit : annuler sélection ---
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
        selected_unit = None
        dragging = False
        reachable_cells = []
        current_path = []
        return True

    return False


def draw_units(screen, unites, interface, offset_x, offset_y, taille):
    unite_size = int(taille * 0.7)

    # zones atteignables
    if reachable_cells and selected_unit:
        joueur_id, _ = selected_unit
        base_color = interface.joueurs[joueur_id]["color"]
        overlay = pg.Surface((taille, taille), pg.SRCALPHA)
        overlay.fill((*base_color, 100))
        for (i, j) in reachable_cells:
            x = offset_x + j * taille
            y = offset_y + i * taille
            screen.blit(overlay, (x, y))

    # unités
    for joueur_id, positions in unites.items():
        color = darker_color(interface.joueurs[joueur_id]["color"])
        for (i, j) in positions:
            x = offset_x + j * taille + (taille - unite_size) // 2
            y = offset_y + i * taille + (taille - unite_size) // 2
            pg.draw.rect(screen, color, (x, y, unite_size, unite_size), border_radius=4)

    # flèche / chemin prévisualisé
    if current_path:
        joueur_id = selected_unit[0] if selected_unit else None
        base_color = interface.joueurs[joueur_id]["color"] if joueur_id else (255, 255, 0)
        color = darker_color(base_color, 0.5)  # plus foncé
        for k in range(len(current_path)-1):
            i1, j1 = current_path[k]
            i2, j2 = current_path[k+1]
            x1 = offset_x + j1 * taille + taille // 2
            y1 = offset_y + i1 * taille + taille // 2
            x2 = offset_x + j2 * taille + taille // 2
            y2 = offset_y + i2 * taille + taille // 2
            pg.draw.line(screen, color, (x1, y1), (x2, y2), 3)

        if len(current_path) >= 2:
            i_end, j_end = current_path[-1]
            end_pos = (offset_x + j_end * taille + taille // 2,
                       offset_y + i_end * taille + taille // 2)
            i_prev, j_prev = current_path[-2]
            start_pos = (offset_x + j_prev * taille + taille // 2,
                         offset_y + i_prev * taille + taille // 2)
            draw_arrow(screen, start_pos, end_pos, color)

def draw_murailles(screen, murailles, case_original, ncols):
    gris = (100, 100, 100)
    epaisseur = 6  # épaisseur du mur

    for (i, j), (ni, nj) in murailles:
        rect1 = case_original[i * ncols + j][0]

        # Mur vers le haut
        if ni == i - 1 and nj == j:
            start = (rect1.left, rect1.top)
            end = (rect1.right, rect1.top)
        # Mur vers le bas
        elif ni == i + 1 and nj == j:
            start = (rect1.left, rect1.bottom)
            end = (rect1.right, rect1.bottom)
        # Mur vers la gauche
        elif ni == i and nj == j - 1:
            start = (rect1.left, rect1.top)
            end = (rect1.left, rect1.bottom)
        # Mur vers la droite
        elif ni == i and nj == j + 1:
            start = (rect1.right, rect1.top)
            end = (rect1.right, rect1.bottom)
        else:
            # au cas où un mur diagonal serait ajouté par erreur
            continue

        pg.draw.line(screen, gris, start, end, epaisseur)


def draw_arrow(screen, start_pos, end_pos, color=(255,255,0)):
    pg.draw.line(screen, color, start_pos, end_pos, 3)
    rotation = pg.math.Vector2(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]).angle_to((1,0))
    arrow = pg.Surface((20,10), pg.SRCALPHA)
    pg.draw.polygon(arrow, color, [(0,0), (20,5), (0,10)])
    arrow = pg.transform.rotate(arrow, -rotation)
    rect = arrow.get_rect(center=end_pos)
    screen.blit(arrow, rect)


def update_unit_animation(unites, interface, case_original, grid_points, taille, offset_x, offset_y, joueurs_data):
    """
    Met à jour l'animation / déplacement pas-à-pas d'une unité.
    On reçoit désormais joueurs_data afin de vérifier les positions de spawn pour la victoire.
    """
    global animating_move

    if animating_move:
        joueur_id, idx, path, step = animating_move

        # step correspond à l'indice actuel dans path ; si step == len(path)-1 on est arrivé
        if step < len(path)-1:
            next_i, next_j = path[step+1]
            # Mettre à jour la position logique de l'unité (phase de "step")
            unites[joueur_id][idx] = (next_i, next_j)

            # Capturer la case si nécessaire
            ncols = len(grid_points[0]) if grid_points else 0
            idx_case = next_i * ncols + next_j
            rect, couleur, owner, cell, is_terrain = case_original[idx_case]

            # Si la case appartient à l'adversaire, on la capture
            if owner != joueur_id and owner != -1:
                case_original[idx_case] = make_case(rect, interface.joueurs[joueur_id]["color"], joueur_id, cell, taille, is_terrain=False)
                interface.joueurs[joueur_id]["points"] += grid_points[next_i][next_j]
                if owner != 0:
                    interface.joueurs[owner]["points"] -= grid_points[next_i][next_j]
                    interface.joueurs[owner]["points"] = max(0, interface.joueurs[owner]["points"])

            # Supprimer éventuelle unité adverse présente sur la case
            for adv_id, adv_units in list(unites.items()):
                if adv_id != joueur_id:
                    # parcourir une copie (indices) pour éviter problème en supprimant
                    for adv_idx, (ai, aj) in list(enumerate(adv_units)):
                        if (ai, aj) == (next_i, next_j):
                            del adv_units[adv_idx]
                            break

            # Vérifier victoire : si l'unité atteint le spawn adverse
            for opponent_id, data in joueurs_data.items():
                if data and data.get("spawn"):
                    spawn_pos = data["spawn"]
                    # si on touche le spawn d'un opponent_id différent de joueur_id => joueur_id gagne
                    if opponent_id != joueur_id and (next_i, next_j) == tuple(spawn_pos):
                        afficher_victoire(pg.display.get_surface(), joueur_id,
                                         pg.display.get_surface().get_width(),
                                         pg.display.get_surface().get_height())
                        pg.quit()
                        sys.exit()

            # avancer l'animation (passer au step suivant)
            animating_move = (joueur_id, idx, path, step+1)

            # Mettre à jour la position logique de l'unité (confirmation)
            unites[joueur_id][idx] = (next_i, next_j)

        else:
            animating_move = None  # fin animation


def afficher_victoire(screen, gagnant, largeur, hauteur):
    font = pg.font.SysFont("arial", 72, bold=True)
    texte = font.render(f"Joueur {gagnant} a gagné !", True, (255, 215, 0))
    
    screen.fill((0, 0, 0))
    screen.blit(texte, (largeur // 2 - texte.get_width() // 2,
                        hauteur // 2 - texte.get_height() // 2))
    pg.display.flip()
    
    pg.time.delay(3000)  # Pause 3 secondes avant retour


def make_case(rect, couleur, owner, cell, taille, is_terrain=False):
    """Retourne un tuple (rect, surface, owner, cell, is_terrain) pour case_original"""
    surface = pg.Surface((taille, taille))
    surface.fill(couleur)
    return (rect, surface, owner, cell, is_terrain)


murailles = set()

def construire_muraille_autour(murailles, ci, cj, taille_zone=3):
    demi = taille_zone // 2
    min_i, max_i = ci - demi, ci + demi
    min_j, max_j = cj - demi, cj + demi

    # haut et bas
    for j in range(min_j, max_j+1):
        if j != cj:  # trou au centre
            murailles.add(((min_i, j), (min_i-1, j)))  # mur entre la case du haut et l’extérieur
            murailles.add(((max_i, j), (max_i+1, j)))  # mur entre la case du bas et l’extérieur

    # gauche et droite
    for i in range(min_i, max_i+1):
        if i != ci:  # trou au centre
            murailles.add(((i, min_j), (i, min_j-1)))  # mur gauche
            murailles.add(((i, max_j), (i, max_j+1)))  # mur droite

