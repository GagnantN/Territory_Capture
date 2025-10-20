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


def get_reachable_cells(start, max_distance, grid_points, forbidden, case_original, murailles):
    """
    Retourne l'ensemble des cellules atteignables en fonction de la distance réelle (BFS).
    - start: (i,j)
    - max_distance: distance max (ex: 5)
    - forbidden: set des cellules interdites
    - murailles: set des segments de muraille
    """
    nrows = len(grid_points)
    ncols = len(grid_points[0])
    visited = set()
    reachable = set()
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited.add(start)

    # transformer murailles en ensemble de cellules bloquées
    murs_bloquants = set()
    for (a,b),(c,d) in murailles:
        murs_bloquants.add((a,b))
        murs_bloquants.add((c,d))

    while queue:
        i, j, dist = queue.popleft()
        if dist > 0:
            reachable.add((i, j))

        if dist < max_distance:
            for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                ni, nj = i + di, j + dj
                if (0 <= ni < nrows and 0 <= nj < ncols and
                    (ni, nj) not in visited and
                    (ni, nj) not in forbidden and
                    (ni, nj) not in murs_bloquants):

                    visited.add((ni, nj))
                    queue.append((ni, nj, dist+1))

    return reachable

from collections import deque

def bfs_path(start, goal, forbidden, nrows, ncols):
    """
    BFS pour trouver un chemin de start à goal en contournant les cases interdites.
    
    start, goal : tuple (i,j)
    forbidden : set de positions (i,j) bloquées (terrains, murailles)
    nrows, ncols : dimensions de la grille
    """
    queue = deque([start])
    visited = {start: None}  # dict pour reconstruire le chemin

    while queue:
        current = queue.popleft()
        if current == goal:
            # reconstruire le chemin depuis goal
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            return path[::-1]  # retourner dans l’ordre start -> goal

        i, j = current
        # voisins (haut, bas, gauche, droite)
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols and (ni,nj) not in forbidden:
                if (ni,nj) not in visited:
                    visited[(ni,nj)] = current
                    queue.append((ni,nj))
    
    # Aucun chemin trouvé
    return None
