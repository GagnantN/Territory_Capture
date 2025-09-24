import pygame as pg, sys
from fonctions.Map import create_map # AJOUT




pg.init()


# ------------------------ ECRAN ------------------------ #
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
largeur, hauteur = screen.get_size() # récupère la résolution réelle
pg.display.set_caption("Territory Capture")
# ------------------------------------------------------- #



# ----------------------- COULEUR ----------------------- #
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 120, 215)
ROUGE = (200, 50, 50)
# ------------------------------------------------------- #



# ----------------------- POLICE ------------------------ #
font_titre = pg.font.SysFont("arial", 60, bold=True)
font_bouton = pg.font.SysFont("arial", 40)
# ------------------------------------------------------- #



# ---------------------- BOUTONS ------------------------ #
btn_jouer = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 200, 80)
btn_quitter = pg.Rect(largeur//2 - 100, hauteur//2 + 60, 200, 80)
# ------------------------------------------------------- #

clock = pg.time.Clock()





# ------------------- MENU PRINCIPAL -------------------- #
def page_accueil():
    en_cours = True
    while en_cours:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_jouer.collidepoint(event.pos):
                    en_cours = False  # passer au jeu
                if btn_quitter.collidepoint(event.pos):
                    pg.quit()
                    sys.exit()

        screen.fill(BLANC)

        # Titre
        titre = font_titre.render("Territory Capture", True, NOIR)
        screen.blit(titre, (largeur//2 - titre.get_width()//2, 100))

        # Bouton Jouer
        pg.draw.rect(screen, BLEU, btn_jouer, border_radius=15)
        txt_jouer = font_bouton.render("Jouer", True, BLANC)
        screen.blit(txt_jouer, (btn_jouer.centerx - txt_jouer.get_width()//2,
                                btn_jouer.centery - txt_jouer.get_height()//2))

        # Bouton Quitter
        pg.draw.rect(screen, ROUGE, btn_quitter, border_radius=15)
        txt_quitter = font_bouton.render("Quitter", True, BLANC)
        screen.blit(txt_quitter, (btn_quitter.centerx - txt_quitter.get_width()//2,
                                  btn_quitter.centery - txt_quitter.get_height()//2))

        pg.display.flip()
        clock.tick(60)
# ------------------------------------------------------- #



# ------------------------ JEU -------------------------- #
def jeu():
    running = True

    # Création de la map
    WCOLOR, BCOLOR, walls = create_map(screen)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        screen.fill((24, 26, 32))

        # Dessiner les cases de la map
        for wall in walls:
            pg.draw.rect(screen, WCOLOR, wall)     # Mur plein
            pg.draw.rect(screen, BCOLOR, wall, 1)  # Contour



        pg.display.flip()
        clock.tick(60)
# ------------------------------------------------------- #

# ------------------------ MAIN ------------------------- #
page_accueil()
jeu()
pg.quit()
sys.exit()
# ------------------------------------------------------- #




# # Créer map
# from fonctions.Map import create_map
# # Page d'accueil
# from fonctions.menu_principal import page_accueil
# # Buttons Quitter
# from fonctions.boutons import button_rect, button_color, button_text_color, text_surface 




# -------------------- CONFIGURATION -------------------- #

# WIDTH, HEIGHT, FPS = 1500, 1000, 60


# ------------------------------------------------------- #



# ---------------------- MENU --------------------------- #
# page_accueil(screen, largeur, hauteur)
# # Quand le joueur clique sur "Jouer", on sort de la fonction et on continue ici
# ------------------------------------------------------- #



# --------------------- IMPORT -------------------------- #
# Maps
# WCOLOR, BCOLOR, walls = create_map(screen)
# ------------------------------------------------------- #



# ------------------- BOUCLE JEU ------------------------ #
# running = True
# while running:
#     dt = clock.tick(FPS) / 1000.0

#     for e in pg.event.get():
#         if e.type == pg.QUIT:
#             running = False

#         elif e.type == pg.MOUSEBUTTONDOWN:
#             if button_rect.collidepoint(e.pos):
#                 running = False # Quitter si clic sur le bouton

#         elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
#             running = False # Quitter avec Eshap


#     # Fond
#     screen.fill((24,26,32))

#     # Boutton quitter
#     pg.draw.rect(screen, button_color, button_rect, border_radius=10)
#     screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))

#     # Afficher la Map
#     for w in walls :
#         pg.draw.rect(screen, WCOLOR, w)     # Mur plein
#         pg.draw.rect(screen, BCOLOR, w, 1)  # Contour


#     pg.display.flip()
# ------------------------------------------------------- #



# ----------------------- Quitter ----------------------- #
# pg.quit(); 
# sys.exit()













# import sys

# pg.init()



# # ---------------- MENU ----------------
# def page_accueil():
#     en_cours = True
#     while en_cours:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 pg.quit()
#                 sys.exit()
#             if event.type == pg.MOUSEBUTTONDOWN:
#                 if btn_jouer.collidepoint(event.pos):
#                     en_cours = False  # passer au jeu
#                 if btn_quitter.collidepoint(event.pos):
#                     pg.quit()
#                     sys.exit()

#         screen.fill(BLANC)

#         # Titre
#         titre = font_titre.render("Territory Capture", True, NOIR)
#         screen.blit(titre, (largeur//2 - titre.get_width()//2, 100))

#         # Bouton Jouer
#         pg.draw.rect(screen, BLEU, btn_jouer, border_radius=15)
#         txt_jouer = font_bouton.render("Jouer", True, BLANC)
#         screen.blit(txt_jouer, (btn_jouer.centerx - txt_jouer.get_width()//2,
#                                 btn_jouer.centery - txt_jouer.get_height()//2))

#         # Bouton Quitter
#         pg.draw.rect(screen, ROUGE, btn_quitter, border_radius=15)
#         txt_quitter = font_bouton.render("Quitter", True, BLANC)
#         screen.blit(txt_quitter, (btn_quitter.centerx - txt_quitter.get_width()//2,
#                                   btn_quitter.centery - txt_quitter.get_height()//2))

#         pg.display.flip()
#         clock.tick(60)

# # ---------------- JEU ----------------
# def jeu():
#     running = True
#     while running:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False
#             if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
#                 running = False

#         screen.fill((24, 26, 32))
#         # Juste un carré de test
#         pg.draw.rect(screen, BLEU, (largeur//2 - 50, hauteur//2 - 50, 100, 100))

#         pg.display.flip()
#         clock.tick(60)

# # ---------------- MAIN ----------------
# page_accueil()
# jeu()
# pg.quit()
# sys.exit()
