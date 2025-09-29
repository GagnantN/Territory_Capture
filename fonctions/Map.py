# fonctions/Map.py
import pygame as pg
import random
from fonctions.cases import terrains, get_reachable_cells, find_path

# ----------------- COULEUR JOUEURS -------------------- #
joueur_01 = (70, 130, 180)   # Bleu acier
joueur_02 = (178, 34, 3)     # Rouge brique
# ------------------------------------------------------- #
central_color = (255, 165, 0)
# ------------------------------------------------------- #

# ------------------------------------------------------- #
# Déplacements d’unités (sélection + animation + flèches)
# ------------------------------------------------------- #
selected_unit = None           # (joueur_id, idx)
reachable_cells = []           # cases atteignables
current_path = []              # chemin prévu (pour dessiner la flèche)
animating_move = None          # (joueur_id, idx, path, step)
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
                        return False
        return True

    def place_zone(color, size, zone_min_col=None, zone_max_col=None, attempts_limit=1000):
        attempts = 0
        while attempts < attempts_limit:
            attempts += 1
            i = random.randrange(ligne)
            j = random.randint(zone_min_col if zone_min_col is not None else 0,
                               zone_max_col if zone_max_col is not None else colonne - 1)
            if zone_min_col is not None and zone_max_col is not None:
                if not (zone_min_col <= j <= zone_max_col):
                    continue
            if not candidate_ok(i, j, color):
                continue
            zone = [(i, j)]
            grid[i][j] = color
            while len(zone) < size:
                frontier = []
                for (ci, cj) in zone:
                    for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                        ni, nj = ci + di, cj + dj
                        if zone_min_col is not None and zone_max_col is not None:
                            if not (zone_min_col <= nj <= zone_max_col):
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

    # center 3x3
    ci = ligne // 2
    cj = colonne // 2
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni, nj = ci + di, cj + dj
            if 0 <= ni < ligne and 0 <= nj < colonne:
                grid[ni][nj] = central_color
                grid_points[ni][nj] = 50

    areas = [
        (0, 4, "GAUCHE"),
        (5, 14, "CENTRE"),
        (15, 19, "DROITE"),
    ]
    for min_col, max_col, label in areas:
        for name, color in terrains.items():
            size = random.randint(4, 7)
            place_zone(color, size, zone_min_col=min_col, zone_max_col=max_col, attempts_limit=2000)

    def place_player(color, min_lin, max_lin, min_col, max_col):
        for _ in range(1000):
            i = random.randrange(min_lin, max_lin)
            j = random.randint(min_col, max_col)
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
                grid_owner[i][j] = 1 if color == joueur_01 else 2
                return (i, j)
        return None

    def expand_player_zone(grid, grid_owner, pos, color, owner_id, grid_points):
        if pos is None:
            return []
        i, j = pos
        captured_cells = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ni, nj = i + di, j + dj
                if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                    if grid[ni][nj] is None:
                        grid[ni][nj] = color
                        grid_owner[ni][nj] = owner_id
                        captured_cells.append((ni, nj))
        return captured_cells

    pos_joueur_1 = place_player(joueur_01, 1, 18, 1, 3)
    pos_joueur_2 = place_player(joueur_02, 1, 18, 16, 18)

    spawn_zone_1 = expand_player_zone(grid, grid_owner, pos_joueur_1, joueur_01, 1, grid_points)
    spawn_zone_2 = expand_player_zone(grid, grid_owner, pos_joueur_2, joueur_02, 2, grid_points)

    joueurs_data = {1: {"spawn": pos_joueur_1}, 2: {"spawn": pos_joueur_2}}

    unites = {1: [], 2: []}
    def add_unite(player_id, base_pos, offsets):
        if base_pos is None:
            return
        i, j = base_pos
        for di, dj in offsets:
            ni, nj = i + di, j + dj
            if 0 <= ni < ligne and 0 <= nj < colonne:
                unites[player_id].append((ni, nj))

    add_unite(1, pos_joueur_1, [(-1,0),(0,1),(1,0)])
    add_unite(2, pos_joueur_2, [(-1,0),(0,-1),(1,0)])

    case_original = []
    for i in range(ligne):
        for j in range(colonne):
            x = offset_x + j * taille
            y = offset_y + i * taille
            rect = pg.Rect(x, y, taille, taille)
            couleur = grid[i][j] if grid[i][j] is not None else (191, 183, 161)
            case_original.append((rect, couleur, grid_owner[i][j]))

    return BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y, grid_points, joueurs_data, spawn_zone_1, spawn_zone_2, unites, grid


def handle_click(mouse_pos, case_original, joueur_id, joueurs, taille, offset_x, offset_y, grid_points, joueurs_data):
    if joueurs[joueur_id]["tickets"] <= 0:
        return False

    nrows = len(grid_points)
    ncols = len(grid_points[0]) if nrows > 0 else 0
    for idx, (rect, couleur, owner) in enumerate(case_original):
        if rect.collidepoint(mouse_pos):
            i, j = divmod(idx, ncols)
            if couleur in terrains.values() or owner == joueur_id or (i, j) == joueurs_data[joueur_id]["spawn"]:
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
            case_original[idx] = (rect, new_color, joueur_id)
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
            _, _, owner = case_original[v_idx]
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
    Gère la sélection et le déplacement des unités.
    - clic gauche enfoncé sur unité = sélection + début drag
    - MOUSEMOTION pendant drag = prévisualiser chemin (current_path)
    - relâcher gauche = valider et lancer animating_move (si case atteignable)
    - clic droit = annuler sélection
    """
    global selected_unit, reachable_cells, current_path, animating_move, dragging

    unite_size = int(taille * 0.7)
    mouse_x, mouse_y = pg.mouse.get_pos()
    grid_i = (mouse_y - offset_y) // taille
    grid_j = (mouse_x - offset_x) // taille

    # --- clic gauche enfoncé : sélectionner / commencer drag ---
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        # si aucune unité sélectionnée -> tenter de sélectionner une unité du joueur actif
        if not selected_unit:
            for joueur_id, positions in unites.items():
                for idx, (i, j) in enumerate(positions):
                    ux = offset_x + j * taille + (taille - unite_size) // 2
                    uy = offset_y + i * taille + (taille - unite_size) // 2
                    rect_unit = pg.Rect(ux, uy, unite_size, unite_size)
                    if rect_unit.collidepoint(mouse_x, mouse_y):
                        if joueur_id == joueur_actif and interface.joueurs[joueur_id]["tickets"] >= 5:
                            selected_unit = (joueur_id, idx)
                            # forbidden = couleurs représentant obstacles (eau, montagne)
                            forbidden = [terrains["eau"], terrains["montagne"]]
                            # IMPORTANT : passer terrain_grid (couleurs) au lieu de grid_points
                            reachable_cells = set(get_reachable_cells((i, j), 5, terrain_grid, forbidden, case_original))
                            current_path = []
                            dragging = True
                            return False
            return False

    # --- mouvement souris pendant drag : prévisualiser chemin ---
    if event.type == pg.MOUSEMOTION and dragging and selected_unit:
        joueur_id, idx = selected_unit
        start = unites[joueur_id][idx]
        # vérifier limites
        nrows = len(terrain_grid)
        ncols = len(terrain_grid[0]) if nrows > 0 else 0
        if 0 <= grid_i < nrows and 0 <= grid_j < ncols and (grid_i, grid_j) in reachable_cells:
            forbidden = [terrains["eau"], terrains["montagne"]]
            path = find_path(start, (grid_i, grid_j), terrain_grid, forbidden, case_original)
            if path and len(path)-1 <= 5:
                current_path = path
            else:
                current_path = []
        else:
            current_path = []
        return False

    # --- relâcher clic gauche : valider déplacement si possible ---
    if event.type == pg.MOUSEBUTTONUP and event.button == 1 and dragging:
        dragging = False
        if selected_unit and current_path:
            joueur_id, idx = selected_unit
            # lancer l'animation pas-à-pas
            animating_move = (joueur_id, idx, current_path, 0)
            interface.joueurs[joueur_id]["tickets"] -= 5
            # reset sélection / zone
            selected_unit = None
            reachable_cells = []
            current_path = []
            return True
        # sinon annuler
        selected_unit = None
        reachable_cells = []
        current_path = []
        return False

    # --- clic droit annule sélection ---
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
        selected_unit = None
        reachable_cells = []
        current_path = []
        dragging = False
        return False

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
        color = interface.joueurs[joueur_id]["color"] if joueur_id else (255, 255, 0)
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


def draw_arrow(screen, start_pos, end_pos, color=(255,255,0)):
    pg.draw.line(screen, color, start_pos, end_pos, 3)
    rotation = pg.math.Vector2(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]).angle_to((1,0))
    arrow = pg.Surface((20,10), pg.SRCALPHA)
    pg.draw.polygon(arrow, color, [(0,0), (20,5), (0,10)])
    arrow = pg.transform.rotate(arrow, -rotation)
    rect = arrow.get_rect(center=end_pos)
    screen.blit(arrow, rect)


def update_unit_animation(unites, interface, case_original, grid_points, taille, offset_x, offset_y):
    global animating_move

    if animating_move:
        joueur_id, idx, path, step = animating_move

        # step correspond à l'indice actuel dans path ; si step == len(path)-1 on est arrivé
        if step < len(path)-1:
            next_i, next_j = path[step+1]
            # Mettre à jour la position logique de l'unité
            unites[joueur_id][idx] = (next_i, next_j)

            # Capturer la case si nécessaire
            ncols = len(grid_points[0]) if grid_points else 0
            idx_case = next_i * ncols + next_j
            rect, couleur, owner = case_original[idx_case]
            if owner != joueur_id:
                case_original[idx_case] = (rect, interface.joueurs[joueur_id]["color"], joueur_id)
                interface.joueurs[joueur_id]["points"] += grid_points[next_i][next_j]
                if owner != 0:
                    interface.joueurs[owner]["points"] -= grid_points[next_i][next_j]
                    interface.joueurs[owner]["points"] = max(0, interface.joueurs[owner]["points"])

            animating_move = (joueur_id, idx, path, step+1)
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
