# Début du menu

import pygame as pg, sys


def page_accueil(screen, largeur, hauteur) :

    # Couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    BLEU = (0, 120, 215)

    # Police
    police_titre = pg.font.SysFont("arial", 60, bold=True)
    police_button = pg.font.SysFont("arial", 40)

    # Texte du titre
    titre = police_titre.render("Territory Capture", True, NOIR)

    # Boutton jouer
    button_rect = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 200, 80)

    clock = pg.time.Clock()
    en_cours = True

    while en_cours: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    en_cours = False # Démarre le jeu

    # Fond
    screen.fill(BLANC)

    # Titre
    screen.blit(titre, (largeur//2 - titre.get_width()//2, 100))

    # Bouton
    pg.draw.rect(screen, BLEU, button_rect, border_radius=15)
    texte_button = police_button.render("Jouer", True, BLANC)
    screen.blit(texte_button, (button_rect.centerx - texte_button.get_width()//2,
                               button_rect.centery - texte_button.get_height()//2))
    
    pg.display.flip()
    clock.tick(60)