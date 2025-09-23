import pygame as pg

HEIGHT = 10
WIDTH = 2000

# ------------------- BOUTTON QUITTER ------------------- #
button_rect = pg.Rect(WIDTH * 0.9 , HEIGHT, 120, 40)
# Couleur
button_color = (200, 0, 0)
# Couleur du text
button_text_color = (255, 255, 255)
font = pg.font.SysFont(None, 30)
text_surface = font.render("Quitter", True, button_text_color)
# ------------------------------------------------------- #