import pygame as pg, sys
from fonctions.Map import create_map, joueur_01, joueur_02, handle_click # AJOUT
from fonctions.interface_joueurs import affichage_joueurs




pg.init()
clock = pg.time.Clock()

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
btn_menu = pg.Rect(20, 20, 120, 50) # En haut à gauche      
# ------------------------------------------------------- #



# --------------- FONCTION AFFICHER MENU ---------------- #
def afficher_menu():
    # Fond semi-transparent
    menu_surface = pg.Surface((largeur, hauteur), pg.SRCALPHA)
    menu_surface.fill((50, 50, 50, 200)) # Gris semi-transparent
    screen.blit(menu_surface, (0,0))

    # Bouton quitter vers menu principal
    btn_quitter_jeu = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 300, 80)
    pg.draw.rect(screen, ROUGE, btn_quitter_jeu, border_radius=15)
    txt_quitter = font_bouton.render("Retour au menu", True, BLANC)
    screen.blit(txt_quitter, (btn_quitter_jeu.centerx - txt_quitter.get_width()//2,
                              btn_quitter_jeu.centery - txt_quitter.get_height()//2))
    
    # Petit bouton pour fermer le menu
    btn_fermer_menu = pg.Rect(largeur - 140, 20, 120, 50) # Coin supérieur droit
    pg.draw.rect(screen, BLEU, btn_fermer_menu, border_radius=10)
    txt_fermer = font_bouton.render("Fermer", True, BLANC)
    screen.blit(txt_fermer, (btn_fermer_menu.centerx - txt_fermer.get_width()//2,
                                btn_fermer_menu.centery - txt_fermer.get_height()//2))

    return btn_quitter_jeu, btn_fermer_menu
# ------------------------------------------------------- #



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
    # Maps
    BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y = create_map(screen)

    # Interface joueurs                                                 
    interface = affichage_joueurs(screen, joueur_01, joueur_02)


    running = True
    menu_actif = False
    retour_menu = False # Revenir au menu principal
    btn_menu = pg.Rect(20, 20, 120, 50)


    # Compteur de tours                                                 #####
    joueur_actif = 1
    interface.joueurs[joueur_actif]["tickets"] += 2 # Premier joueur commence avec 2 tickets
    start_time = pg.time.get_ticks()
    duree_tour = 30 # Secondes

    # Création de la map
    #WCOLOR, BCOLOR, walls = create_map(screen)

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menu_actif = not menu_actif

            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_menu.collidepoint(event.pos):
                    menu_actif = True # Ouvrir le menu

                if menu_actif :
                    btn_quitter_jeu, btn_fermer_menu = afficher_menu()

                    if event.type == pg.MOUSEBUTTONDOWN:
                        if btn_quitter_jeu.collidepoint(event.pos):
                            retour_menu = True
                            running = False

                        if btn_fermer_menu.collidepoint(event.pos):
                            menu_actif = False # Fermer le menu

                    if btn_quitter_jeu.collidepoint(event.pos):
                        retour_menu = True
                        running = False
                
                mouse_pos = pg.mouse.get_pos()
                handle_click(mouse_pos, case_original, joueur_01)  # par ex. joueur 1


        # Vérifier si 30 secondes écoulées                  #####
        elapsed = (pg.time.get_ticks() - start_time) / 1000
        chrono = max(0, duree_tour - int(elapsed))
        if elapsed >= duree_tour:
            # Changer de joueur
            joueur_actif = 2 if joueur_actif == 1 else 1
            interface.joueurs[joueur_actif]["tickets"] +=2
            start_time = pg.time.get_ticks() # Reset chronomètre


        # Affichage jeu
        screen.fill((24, 26, 32))


        # Dessiner les cases de la map
        for rect, couleur in case_original :
            pg.draw.rect(screen, couleur, rect)  # remplissage
            pg.draw.rect(screen, BCOLOR, rect, 1) # bordure
            

        # Dessiner les joueurs
        if pos_joueur_1:
            i, j = pos_joueur_1
            x = offset_x + j * (taille)
            y = offset_y + i * (taille)
            pg.draw.rect(screen, (70, 130, 180), (x, y, taille, taille))  # joueur_01


        if pos_joueur_2:
            i, j = pos_joueur_2
            x = offset_x + j * taille
            y = offset_y + i * taille
            pg.draw.rect(screen, (178, 34, 3), (x, y, taille, taille))  # joueur_02


        # HUD des joueurs                   #####
        interface.draw(joueur_actif)


        # Afficher chrono en haut           #####
        font_timer = pg.font.SysFont("arial", 48, bold=True)
        txt_timer = font_timer.render(str(chrono), True, (255, 255, 0))
        screen.blit(txt_timer, (largeur // 2 - txt_timer.get_width() // 2, 20))


        # Bouton Menu en jeu
        pg.draw.rect(screen, BLEU, btn_menu, border_radius=10)
        txt_menu = font_bouton.render("Menu", True, BLANC)
        screen.blit(txt_menu, (btn_menu.centerx - txt_menu.get_width()//2,
                               btn_menu.centery - txt_menu.get_height()//2))
        

        # Si menu actif, afficher overlay
        if menu_actif:
            btn_quitter_jeu = afficher_menu()


        pg.display.flip()
        # clock.tick(60)                    #####

    return retour_menu # Retourne l'etat pour savoir si on revint au menu principal 
# ------------------------------------------------------- #



# ------------------------ MAIN ------------------------- #
while True:
    page_accueil()
    retour = jeu()

    if not retour:
        break # Si le joueur ferme complètement, on sort
pg.quit()
sys.exit()
# ------------------------------------------------------- #




