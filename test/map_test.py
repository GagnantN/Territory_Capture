import unittest
import pygame as pg
import sys
import os
import traceback

# 🧭 On ajoute le dossier racine du projet (Territory_Capture) au sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

# 🧪 ⚡ On "mock" le chargement des images pour les tests :
# Cela évite que Pygame cherche les fichiers réels (Eau.png, Foret.png, etc.)
pg.image.load = lambda path: pg.Surface((10, 10))

# --- 🧱 Initialisation Pygame en mode test ---
pg.display.init()
pg.display.set_mode((1, 1))  # fenêtre minimale invisible pour les tests

# --- 🧪 Import des fonctions à tester depuis Map.py ---
from fonctions.Map import darker_color, make_case, est_adjacent, get_forbidden_cells, construire_muraille_autour, handle_click


class TestMapFunctions(unittest.TestCase):

    def setUp(self):
        """Préparation d'une mini grille 3x3 pour les tests"""
        self.taille = 20
        self.offset_x = 0
        self.offset_y = 0
        self.color_player = (100, 100, 255)

        # Création de 9 cases factices
        self.case_original = []
        for i in range(3):
            for j in range(3):
                rect = pg.Rect(j * self.taille, i * self.taille, self.taille, self.taille)
                # owner = 0 par défaut
                self.case_original.append(make_case(rect, (200, 200, 200), 0, None, self.taille, False))

        # Joueurs fictifs
        self.joueurs = {
            1: {"tickets": 3, "points": 0, "color": self.color_player},
            2: {"tickets": 3, "points": 0, "color": (255, 0, 0)},
        }

        # Spawns fictifs
        self.joueurs_data = {
            1: {"spawn": (1, 1)},
            2: {"spawn": (2, 2)},
        }

    def run_with_result(self, func):
        """Helper pour exécuter chaque test avec affichage ✅ ou ❌"""
        try:
            func()
            print(f"✅ {func.__doc__}")
        except Exception as e:
            print(f"❌ {func.__doc__} → {e}")
            traceback.print_exc()
            raise  # Important pour que unittest signale bien l'échec

    # --- 🎨 TESTS DES FONCTIONS ---

    def test_darker_color(self):
        """darker_color : la couleur est bien assombrie"""
        self.run_with_result(self._test_darker_color)

    def _test_darker_color(self):
        color = (100, 100, 100)
        expected = (60, 60, 60)
        self.assertEqual(darker_color(color), expected)

    def test_make_case(self):
        """make_case : tuple correctement formé"""
        self.run_with_result(self._test_make_case)

    def _test_make_case(self):
        rect = pg.Rect(0, 0, 20, 20)
        result = make_case(rect, (255, 0, 0), 1, "cellule", 20, False)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[2], 1)
        self.assertFalse(result[4])

    def test_est_adjacent_true(self):
        """est_adjacent : True quand une case voisine appartient au joueur"""
        self.run_with_result(self._test_est_adjacent_true)

    def _test_est_adjacent_true(self):
        idx_centre = 4
        idx_gauche = 3
        rect, surf, _, cell, terrain = self.case_original[idx_gauche]
        self.case_original[idx_gauche] = make_case(rect, self.color_player, 1, cell, self.taille, False)
        self.assertTrue(est_adjacent(self.case_original, idx_centre, 1))

    def test_est_adjacent_false(self):
        """est_adjacent : False si aucune case voisine n'appartient au joueur"""
        self.run_with_result(self._test_est_adjacent_false)

    def _test_est_adjacent_false(self):
        idx_centre = 4
        self.assertFalse(est_adjacent(self.case_original, idx_centre, 1))

    def test_get_forbidden_cells(self):
        """get_forbidden_cells : terrains et murailles bien détectés"""
        self.run_with_result(self._test_get_forbidden_cells)

    def _test_get_forbidden_cells(self):
        terrain_grid = [
            ["foret", None],
            [None, None],
        ]
        murailles = {((0, 0), (0, 1))}
        forbidden = get_forbidden_cells(terrain_grid, murailles)
        self.assertIn((0, 0), forbidden)
        self.assertIn((0, 1), forbidden)

    def test_construire_muraille_autour(self):
        """construire_muraille_autour : murs bien ajoutés"""
        self.run_with_result(self._test_construire_muraille_autour)

    def _test_construire_muraille_autour(self):
        murailles = set()
        construire_muraille_autour(murailles, 5, 5, taille_zone=3)
        self.assertTrue(len(murailles) > 0)
        for a, b in murailles:
            self.assertIsInstance(a, tuple)
            self.assertIsInstance(b, tuple)

    def test_handle_click_capture(self):
        """handle_click : capture une case neutre adjacente"""
        self.run_with_result(self._test_handle_click_capture)

    def _test_handle_click_capture(self):
        """handle_click : capture une case neutre adjacente"""
        # On met la case du joueur au centre (1,1)
        idx_centre = 4
        rect, surf, _, cell, terrain = self.case_original[idx_centre]
        self.case_original[idx_centre] = make_case(rect, self.color_player, 1, cell, self.taille, False)

        # La case neutre qu'on veut capturer (1,2)
        idx_cible = 5
        rect, surf, _, cell, terrain = self.case_original[idx_cible]
        self.case_original[idx_cible] = make_case(rect, (200,200,200), 0, cell, self.taille, False)

        mouse_pos = (rect.x + 1, rect.y + 1)  # clique à l'intérieur de la case neutre
        grid_points = [[10, 10, 10], [10, 10, 10], [10, 10, 10]]

        result = handle_click(mouse_pos, self.case_original, 1, self.joueurs,
                            self.taille, self.offset_x, self.offset_y,
                            grid_points, self.joueurs_data)
        self.assertTrue(result)
        self.assertEqual(self.joueurs[1]["points"], 10)



if __name__ == "__main__":
    print("🚀 Lancement des tests unitaires Map.py...\n")
    unittest.main(verbosity=0)  # On masque le runner standard pour n'afficher que nos ✅ / ❌
