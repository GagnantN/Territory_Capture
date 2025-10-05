import pygame as pg
from collections import deque

ligne = 21
colonne = 21

# ----------------- COULEUR TERRAINS -------------------- #
terrains = {
    "eau": (50, 100, 200),
    "montagne": (120, 120, 120),
    "foret": (200, 200, 150),
    "bordure": (0, 42, 9),
}
# ------------------------------------------------------- #

# ----------------- COULEUR JOUEURS -------------------- #
joueur_01 = (70, 130, 180)
joueur_02 = (178, 34, 3)
# ------------------------------------------------------- #


def get_reachable_cells(start, max_range, grid_points, forbidden_types, case_original, murailles):
    """
    BFS qui retourne l'ensemble des cellules atteignables (i,j) en évitant :
    - les terrains interdits
    - les murailles (barrières entre deux cases)
    """
    reachable = set()
    queue = deque([(start, 0)])
    nrows = len(grid_points)
    ncols = len(grid_points[0]) if nrows > 0 else 0

    while queue:
        (i, j), dist = queue.popleft()
        if dist > max_range:
            continue
        if (i, j) in reachable:
            continue

        reachable.add((i, j))

        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols:
                continue

            # 🔒 Vérifier s’il y a une muraille entre (i,j) et (ni,nj)
            if ((i, j), (ni, nj)) in murailles or ((ni, nj), (i, j)) in murailles:
                continue

            idx = ni * ncols + nj
            _, _, _, _, is_terrain = case_original[idx]
            if not is_terrain:
                queue.append(((ni, nj), dist + 1))


    return reachable


def find_path(start, goal, grid_points, forbidden_types, case_original, murailles):
    """
    BFS (reconstruction de chemin) qui évite :
    - les terrains interdits
    - les murailles (barrières entre deux cases)
    Retourne une liste de (i,j) ou None si impossible.
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
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols:
                neighbor = (ni, nj)
                if neighbor in came_from:
                    continue

                # 🔒 Vérifier les murailles
                if ((i, j), (ni, nj)) in murailles or ((ni, nj), (i, j)) in murailles:
                    continue

                idx = ni * ncols + nj
                _, _, _, _, is_terrain = case_original[idx]
                if is_terrain:
                    continue
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return None

    # reconstruire chemin
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
