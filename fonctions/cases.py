import pygame as pg
from collections import deque

# NOTE: on n'ouvre plus d'écran ici — laissé minimal pour garder ton style original.
# Récupère la taille actuelle de la fenêtre si nécessaire ailleurs.
ligne = 21
colonne = 21

# ----------------- COULEUR TERRAINS -------------------- #
terrains = {
    "eau" : (50, 100, 200),
    "montagne" : (120, 120, 120),
    "foret" : (200, 200, 150),
    "bordure" : (0, 42, 9),
}
# ------------------------------------------------------- #

# ----------------- COULEUR JOUEURS  -------------------- #
joueur_01 = (70, 130, 180)
joueur_02 = (178, 34, 3)
# ------------------------------------------------------- #


def get_reachable_cells(start, max_range, grid_points, forbidden_types, case_original):
    """
    BFS qui retourne l'ensemble des cellules atteignables (i,j) en évitant
    les cases dont la couleur est dans forbidden_types.
    - start: (i,j)
    - max_range: portée en nombre de déplacements (Manhattan BFS)
    - grid_points: matrice utilisée pour connaître la taille du grid
    - forbidden_types: liste de couleurs (ex: [terrains['eau'], terrains['montagne']])
    - case_original: liste de (rect, couleur, owner) comme dans create_map
    """
    reachable = set()
    queue = deque([ (start, 0) ])
    nrows = len(grid_points)
    ncols = len(grid_points[0]) if nrows > 0 else 0

    while queue:
        (i, j), dist = queue.popleft()
        if dist > max_range:
            continue
        if (i, j) in reachable:
            continue

        reachable.add((i, j))

        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols:
                idx = ni * ncols + nj
                rect, couleur, owner, cell = case_original[idx]
                if couleur not in forbidden_types:
                    queue.append(((ni, nj), dist+1))

    return reachable


def find_path(start, goal, grid_points, forbidden_types, case_original):
    """
    BFS (reconstruction de chemin) qui évite les couleurs dans forbidden_types.
    Retourne liste de (i,j) du start au goal inclus, ou None si impossible.
    """
    if start == goal:
        return [start]

    nrows = len(grid_points)
    ncols = len(grid_points[0]) if nrows > 0 else 0

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        i, j = current
        for di, dj in [(0,1),(0,-1),(1,0),(-1,0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols:
                neighbor = (ni, nj)
                if neighbor in came_from:
                    continue
                idx = ni * ncols + nj
                _, couleur, _ = case_original[idx]
                if couleur in forbidden_types:
                    continue
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return None

    # reconstruire
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path