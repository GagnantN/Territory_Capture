import pygame as pg, sys
from fonctions.Map import create_map, joueur_01, joueur_02, handle_click, afficher_victoire, handle_unit_events, draw_units, update_unit_animation # AJOUT
from fonctions.interface_joueurs import affichage_joueurs


pg.init()
clock = pg.time.Clock()


# ------------------------ ECRAN ------------------------ #
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
largeur, hauteur = screen.get_size()
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
font_timer = pg.font.SysFont("arial", 48, bold=True)
# ------------------------------------------------------- #



# ---------------------- BOUTONS ------------------------ #
# Bouton jouer
btn_jouer = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 200, 80)
# Bouton quitter
btn_quitter = pg.Rect(largeur//2 - 100, hauteur//2 + 60, 200, 80)
# Bouton menu
btn_menu = pg.Rect(20, 20, 120, 50)
# Bouton skip partie
btn_skip = pg.Rect(largeur//2 - 150, hauteur - 70, 300, 60)
# ------------------------------------------------------- #



# --------------- FONCTION AFFICHER MENU ---------------- #
def afficher_menu():
    # Fond semi-transparent
    menu_surface = pg.Surface((largeur, hauteur), pg.SRCALPHA)
    menu_surface.fill((50, 50, 50, 200)) # Gris semi-transparent
    screen.blit(menu_surface, (0,0))

    # Bouton quitter vers menu principal
    btn_quitter_jeu = pg.Rect(largeur//2 - 150, hauteur//2 - 40, 300, 80)
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
    BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y, grid_points, joueurs_data, spawn_zone_1, spawn_zone_2, unites, terrain_grid = create_map(screen)


    # Interface joueurs                                                 
    interface = affichage_joueurs(screen, joueur_01, joueur_02)

    # Ajouter les points des zones de spawn pour le joueur 1
    for ni, nj in spawn_zone_1:
        interface.joueurs[1]["points"] += grid_points[ni][nj]

    # Ajouter les points des zones de spawn pour le joueur 2
    for ni, nj in spawn_zone_2:
        interface.joueurs[2]["points"] += grid_points[ni][nj]




    running = True
    menu_actif = False
    retour_menu = False # Revenir au menu principal
    joueur_actif = 1
    interface.joueurs[joueur_actif]["tickets"] += 2 # Premier joueur commence avec 2 tickets

    ##### Chronos
    start_time, duree_tour, chrono, chrono_en_pause = pg.time.get_ticks(), 30, 30, 30
    duree_totale_partie, start_partie = 600, pg.time.get_ticks()
    pause_offset, pause_start = 0, None
    btn_quitter_jeu, btn_fermer_menu = None, None

    # Création de la map
    #WCOLOR, BCOLOR, walls = create_map(screen)


    while running:
        dt = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                menu_actif = not menu_actif
                if menu_actif:
                    chrono_en_pause = chrono # Figer le chrono
                    pause_start = pg.time.get_ticks()                   #####
                else:
                    # Reprendre le chrono correctement
                    start_time = pg.time.get_ticks() - (duree_tour - chrono_en_pause) * 1000

                    if pause_start is not None:
                        pause_offset += pg.time.get_ticks() - pause_start
                        pause_start = None

            if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION):
                # Gestion unités (drag & drop)
                moved = handle_unit_events(event, unites, joueur_actif, interface, offset_x, offset_y, taille, grid_points, case_original, terrain_grid)
                if moved:
                    continue  # on ne fait rien d’autre si une unité a bougé
                
                if menu_actif and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_quitter_jeu and btn_quitter_jeu.collidepoint(event.pos):
                        retour_menu = True
                        running = False
                    if btn_fermer_menu and btn_fermer_menu.collidepoint(event.pos):
                        menu_actif = False
                        # Reprendre le chrono à partir de la valeur figée
                        start_time = pg.time.get_ticks() - (duree_tour - chrono_en_pause) * 1000
                        # Ajuster chrono global
                        if pause_start is not None:
                            pause_offset += pg.time.get_ticks() - pause_start
                            pause_start = None
                
                else:
                    # Quand le menu est inactif
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # clic gauche
                        if btn_skip.collidepoint(event.pos):
                            joueur_actif = 2 if joueur_actif == 1 else 1
                            interface.joueurs[joueur_actif]["tickets"] += 2
                            start_time = pg.time.get_ticks()
                            chrono = duree_tour

                        if btn_menu.collidepoint(event.pos):
                            menu_actif = True
                            chrono_en_pause = chrono
                            pause_start = pg.time.get_ticks()

        # Chrono
        if not menu_actif :
            elapsed = (pg.time.get_ticks() - start_time) / 1000
            chrono = max(0, duree_tour - int(elapsed))

            if elapsed >= duree_tour:
                # Ajouter les tickets au joueur qui vient de finir son tour
                interface.joueurs[joueur_actif]["tickets"] += 2
                # Changer de joueur
                joueur_actif = 2 if joueur_actif == 1 else 1
                start_time = pg.time.get_ticks()  # Reset chronomètre
                chrono = duree_tour



        else:
            chrono = chrono_en_pause # Figé



        # Chrono global de la partie
        if pause_start is not None:
            elapsed_partie = int(pause_start - start_partie - pause_offset) // 1000
        
        else:
            elapsed_partie = int(pg.time.get_ticks() - start_partie - pause_offset) // 1000


        temps_restant = max(0, duree_totale_partie - int(elapsed_partie))
        minutes, secondes = divmod(int(temps_restant), 60)
        texte_temps = f"{minutes:02d}:{secondes:02d}"

        # Fin automatique
        if temps_restant <=0:
            retour_menu = True
            running = False


        # Affichage jeu
        screen.fill((24, 26, 32))


        # Dessiner les cases de la map
        for rect, couleur, owner in case_original :
            pg.draw.rect(screen, couleur, rect)  # remplissage
            pg.draw.rect(screen, BCOLOR, rect, 1) # bordure
            

        # Dessiner les joueurs
        if pos_joueur_1:
            i, j = pos_joueur_1
            # x = offset_x + j * (taille)
            # y = offset_y + i * (taille)
            pg.draw.rect(screen, (70, 130, 180), (offset_x + j*taille, offset_y + i*taille, taille, taille))  # joueur_01


        if pos_joueur_2:
            i, j = pos_joueur_2
            # x = offset_x + j * taille
            # y = offset_y + i * taille
            pg.draw.rect(screen, (178, 34, 3), (offset_x + j*taille, offset_y + i*taille, taille, taille))  # joueur_02

        # Dessiner les unités (drag & drop inclus)
        draw_units(screen, unites, interface, offset_x, offset_y, taille)
        
        # Dessiner les unités (drag & drop inclus)
        draw_units(screen, unites, interface, offset_x, offset_y, taille)

        update_unit_animation(unites, interface, case_original, grid_points, taille, offset_x, offset_y)






        # HUD des joueurs
        interface.draw(joueur_actif)


        # Chrono de tour
        txt_timer = pg.font.SysFont("arial",48,bold=True).render(str(chrono), True, (255, 255, 0))
        screen.blit(txt_timer, (largeur//2 - txt_timer.get_width()//2, 20))


        # Chrono global (fin de la partie)
        txt_fin_partie = font_timer.render(f"Fin de la partie : {texte_temps}", True, (255, 255, 255))
        screen.blit(txt_fin_partie, (20, hauteur - txt_fin_partie.get_height() - 20))


        # Bouton Menu en jeu
        pg.draw.rect(screen, BLEU, btn_menu, border_radius=10)
        txt_menu = font_bouton.render("Menu", True, BLANC)
        screen.blit(txt_menu, (btn_menu.centerx - txt_menu.get_width()//2,
                               btn_menu.centery - txt_menu.get_height()//2))
        

        # Bouton Skip (Si menu non actif)
        if not menu_actif:
            pg.draw.rect(screen, (24, 26, 32), btn_skip)
            pg.draw.rect(screen, (255, 255, 0), btn_skip, width=3, border_radius=12)
            txt_skip = font_bouton.render("Passer le tour", True, (255, 255, 0))
            screen.blit(txt_skip, (btn_skip.centerx - txt_skip.get_width()//2,
                                btn_skip.centery - txt_skip.get_height()//2))


        # Overlay menu
        if menu_actif:
            btn_quitter_jeu, btn_fermer_menu = afficher_menu()


        pg.display.flip()

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




