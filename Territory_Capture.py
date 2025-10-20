import pygame as pg, sys
from fonctions.Map import create_map, joueur_01, joueur_02, textures, handle_click, afficher_victoire, handle_unit_events, draw_units, update_unit_animation, draw_murailles
from fonctions.interface_joueurs import affichage_joueurs

pg.init()
clock = pg.time.Clock()

# ------------------------ ECRAN ------------------------ #
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
largeur, hauteur = screen.get_size()

# Fond d'écran principal
background_image = pg.image.load("Images/Principal.png").convert()
background_image = pg.transform.scale(background_image, (largeur, hauteur))

for key, surf in textures.items():
    textures[key] = surf.convert()

largeur, hauteur = screen.get_size()
pg.display.set_caption("Territory Capture")
# ------------------------------------------------------- #


# ----------------------- COULEUR ----------------------- #
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 120, 215)
ROUGE = (200, 50, 50)
VERT = (50, 200, 50)
# ------------------------------------------------------- #


# ----------------------- POLICE ------------------------ #
font_titre = pg.font.SysFont("arial", 60, bold=True)
font_bouton = pg.font.SysFont("arial", 40)
font_timer = pg.font.SysFont("arial", 48, bold=True)
font_prix = pg.font.SysFont("arial", 28, bold=False)
# ------------------------------------------------------- #


# ---------------------- BOUTONS ------------------------ #
btn_jouer = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 200, 80)
btn_quitter = pg.Rect(largeur//2 - 100, hauteur//2 + 60, 200, 80)
btn_menu = pg.Rect(20, 20, 120, 50)
btn_skip = pg.Rect(largeur//2 - 150, hauteur - 70, 300, 60)
btn_bonus = pg.Rect(0, 0, 250, 60)
btn_creer_unite = pg.Rect(0, 0, 250, 60)
# ------------------------------------------------------- #


# ------------------------ MENU ------------------------- #
def afficher_menu():
    menu_surface = pg.Surface((largeur, hauteur), pg.SRCALPHA)
    menu_surface.fill((50, 50, 50, 200))
    screen.blit(menu_surface, (0,0))

    btn_quitter_jeu = pg.Rect(largeur//2 - 150, hauteur//2 - 40, 300, 80)
    pg.draw.rect(screen, ROUGE, btn_quitter_jeu, border_radius=15)
    txt_quitter = font_bouton.render("Retour au menu", True, BLANC)
    screen.blit(txt_quitter, (btn_quitter_jeu.centerx - txt_quitter.get_width()//2,
                              btn_quitter_jeu.centery - txt_quitter.get_height()//2))
    
    btn_fermer_menu = pg.Rect(largeur - 140, 20, 120, 50)
    pg.draw.rect(screen, BLEU, btn_fermer_menu, border_radius=10)
    txt_fermer = font_bouton.render("Fermer", True, BLANC)
    screen.blit(txt_fermer, (btn_fermer_menu.centerx - txt_fermer.get_width()//2,
                                btn_fermer_menu.centery - txt_fermer.get_height()//2))

    return btn_quitter_jeu, btn_fermer_menu
# ------------------------------------------------------- #


# -------------------- PAGE ACCUEIL --------------------- #
def page_accueil():
    en_cours = True
    while en_cours:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if btn_jouer.collidepoint(event.pos):
                    en_cours = False
                if btn_quitter.collidepoint(event.pos):
                    pg.quit()
                    sys.exit()

        # screen.fill(BLANC)
        screen.blit(background_image, (0, 0))

        # titre = font_titre.render("Territory Capture", True, NOIR)
        # screen.blit(titre, (largeur//2 - titre.get_width()//2, 100))

        pg.draw.rect(screen, BLEU, btn_jouer, border_radius=15)
        txt_jouer = font_bouton.render("Jouer", True, BLANC)
        screen.blit(txt_jouer, (btn_jouer.centerx - txt_jouer.get_width()//2,
                                btn_jouer.centery - txt_jouer.get_height()//2))

        pg.draw.rect(screen, ROUGE, btn_quitter, border_radius=15)
        txt_quitter = font_bouton.render("Quitter", True, BLANC)
        screen.blit(txt_quitter, (btn_quitter.centerx - txt_quitter.get_width()//2,
                                  btn_quitter.centery - txt_quitter.get_height()//2))

        pg.display.flip()
        clock.tick(60)
# ------------------------------------------------------- #


# ------------------------- JEU ------------------------- #
def jeu():
    BCOLOR, case_original, pos_joueur_1, pos_joueur_2, terrains, taille, offset_x, offset_y, grid_points, joueurs_data, spawn_zone_1, spawn_zone_2, unites, terrain_grid, murailles = create_map(screen)

    interface = affichage_joueurs(screen, joueur_01, joueur_02)

    mode_creation_unite = False
    unite_ghost_pos = None

    # Ajouter points zones spawn
    for ni, nj in spawn_zone_1:
        interface.joueurs[1]["points"] += grid_points[ni][nj]
    for ni, nj in spawn_zone_2:
        interface.joueurs[2]["points"] += grid_points[ni][nj]

    running = True
    menu_actif = False
    retour_menu = False
    joueur_actif = 1
    interface.joueurs[joueur_actif]["tickets"] += 2

    for j in interface.joueurs.values():
        j["bonus_tour_suivant"] = 0

    start_time = pg.time.get_ticks()
    duree_tour = 30
    chrono = duree_tour
    chrono_en_pause = chrono
    duree_totale_partie = 600
    start_partie = pg.time.get_ticks()
    pause_offset = 0
    pause_start = None
    btn_quitter_jeu, btn_fermer_menu = None, None


    while running:
        dt = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    menu_actif = not menu_actif

                    if menu_actif:
                        chrono_en_pause = chrono
                        pause_start = pg.time.get_ticks()

                    else:
                        start_time = pg.time.get_ticks() - (duree_tour - chrono_en_pause) * 1000

                        if pause_start is not None:
                            pause_offset += pg.time.get_ticks() - pause_start
                            pause_start = None

                if event.key == pg.K_SPACE and not menu_actif:
                    joueur_actif = 2 if joueur_actif == 1 else 1
                    mode_creation_unite = False                                                                         ###############
                    interface.joueurs[joueur_actif]["tickets"] += 2 + interface.joueurs[joueur_actif]["bonus_tour_suivant"]
                    interface.joueurs[joueur_actif]["bonus_tour_suivant"] = 0
                    start_time = pg.time.get_ticks()
                    chrono = duree_tour

            if event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION):
                mouse_pos = pg.mouse.get_pos()

                # Drag & drop unit events
                handle_unit_events(event, unites, joueur_actif, interface,
                                   offset_x, offset_y, taille, grid_points, case_original, terrain_grid)
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                    if menu_actif:

                        if btn_quitter_jeu and btn_quitter_jeu.collidepoint(mouse_pos):
                            retour_menu = True
                            running = False

                        elif btn_fermer_menu and btn_fermer_menu.collidepoint(mouse_pos):
                            menu_actif = False
                            start_time = pg.time.get_ticks() - (duree_tour - chrono_en_pause) * 1000

                            if pause_start is not None:
                                pause_offset += pg.time.get_ticks() - pause_start
                                pause_start = None

                    else:

                        if btn_menu.collidepoint(mouse_pos):
                            menu_actif = True
                            chrono_en_pause = chrono
                            pause_start = pg.time.get_ticks()

                        elif btn_skip.collidepoint(mouse_pos):
                            joueur_actif = 2 if joueur_actif == 1 else 1
                            mode_creation_unite = False                                                                             ###############
                            interface.joueurs[joueur_actif]["tickets"] += 2 + interface.joueurs[joueur_actif]["bonus_tour_suivant"]
                            interface.joueurs[joueur_actif]["bonus_tour_suivant"] = 0
                            start_time = pg.time.get_ticks()
                            chrono = duree_tour

                        elif btn_bonus.collidepoint(mouse_pos):
                            joueur = interface.joueurs[joueur_actif]
                            if joueur["points"] >= 100:
                                joueur["points"] -= 100
                                joueur["bonus_tour_suivant"] += 1

                        elif btn_creer_unite.collidepoint(mouse_pos) and not mode_creation_unite:
                            joueur = interface.joueurs[joueur_actif]
                            if joueur["points"] >= 500:
                                joueur["points"] -= 500
                                mode_creation_unite = True

                        elif mode_creation_unite:
                            # Vérifie si clic sur case appartenant au joueur actif est vide
                            mx, my = mouse_pos
                            grid_i = (my - offset_y) // taille
                            grid_j = (mx - offset_x) // taille
                            nrows = len(grid_points)
                            ncols = len(grid_points[0])
                            if 0 <= grid_i < nrows and 0 <= grid_j < ncols:
                                idx_case = grid_i * ncols + grid_j
                                rect, couleur, owner, cell, is_terrain = case_original[idx_case]
                                if owner == joueur_actif and not is_terrain:
                                    # Vérifie si aucune unité est déjà là
                                    deja_unite = any((grid_i, grid_j) in positions for positions in unites.values())
                                    if not deja_unite:
                                        unites[joueur_actif].append((grid_i, grid_j))
                                        mode_creation_unite = False
                        
                        else:
                            handle_click(mouse_pos, case_original, joueur_actif, interface.joueurs,
                                         taille, offset_x, offset_y, grid_points, joueurs_data)



        if not menu_actif:
            elapsed = (pg.time.get_ticks() - start_time) / 1000
            chrono = max(0, duree_tour - int(elapsed))

            if elapsed >= duree_tour:
                joueur_actif = 2 if joueur_actif == 1 else 1
                mode_creation_unite = False
                interface.joueurs[joueur_actif]["tickets"] += 2 + interface.joueurs[joueur_actif]["bonus_tour_suivant"]
                interface.joueurs[joueur_actif]["bonus_tour_suivant"] = 0
                start_time = pg.time.get_ticks()

        else:
            chrono = chrono_en_pause

        if pause_start is not None:
            elapsed_partie = int(pause_start - start_partie - pause_offset) // 1000

        else:
            elapsed_partie = int(pg.time.get_ticks() - start_partie - pause_offset) // 1000

        temps_restant = max(0, duree_totale_partie - int(elapsed_partie))
        minutes, secondes = divmod(int(temps_restant), 60)
        texte_temps = f"{minutes:02d}:{secondes:02d}"

        if temps_restant <= 0:
            retour_menu = True
            running = False

        screen.fill((24, 26, 32))

        # Afficher map
        for rect, texture, owner, cell, is_terrain in case_original:
            screen.blit(texture, rect.topleft)
            pg.draw.rect(screen, BCOLOR, rect, 1)

        # Dessiner murailles
        draw_murailles(screen, murailles, case_original, len(grid_points[0]))

        # Joueurs
        if pos_joueur_1:
            i, j = pos_joueur_1
            pg.draw.rect(screen, (70, 130, 180), (offset_x + j*taille, offset_y + i*taille, taille, taille))

        if pos_joueur_2:
            i, j = pos_joueur_2
            pg.draw.rect(screen, (178, 34, 3), (offset_x + j*taille, offset_y + i*taille, taille, taille))

        draw_units(screen, unites, interface, offset_x, offset_y, taille)
        # <-- IMPORTANT : on passe maintenant joueurs_data pour la détection de spawn/victoire
        update_unit_animation(unites, interface, case_original, grid_points, taille, offset_x, offset_y, joueurs_data)

        # HUD
        interface.draw(joueur_actif)
        txt_timer = pg.font.SysFont("arial",48 ,bold=True).render(str(chrono), True, (255, 255, 0))
        screen.blit(txt_timer, (largeur//2 - txt_timer.get_width()//2, 20))
        txt_fin_partie = font_timer.render(f"Fin de la partie : {texte_temps}", True, (255, 255, 255))
        screen.blit(txt_fin_partie, (20, hauteur - txt_fin_partie.get_height() - 20))

        pg.draw.rect(screen, BLEU, btn_menu, border_radius=10)
        txt_menu = font_bouton.render("Menu", True, BLANC)
        screen.blit(txt_menu, (btn_menu.centerx - txt_menu.get_width()//2,
                               btn_menu.centery - txt_menu.get_height()//2))

        if not menu_actif:
            pg.draw.rect(screen, (24, 26, 32), btn_skip)
            pg.draw.rect(screen, (255, 255, 0), btn_skip, width=3, border_radius=12)
            txt_skip = font_bouton.render("Passer le tour", True, (255, 255, 0))
            screen.blit(txt_skip, (btn_skip.centerx - txt_skip.get_width()//2,
                                btn_skip.centery - txt_skip.get_height()//2))

            if joueur_actif == 1:
                btn_bonus.topleft = (50, hauteur//2 - 30)
            else:
                btn_bonus.topright = (largeur - 50, hauteur//2 - 30)


            # Affichage Bouton (+1 tickets)
            pg.draw.rect(screen, VERT, btn_bonus, border_radius=12)
            txt_bonus = font_bouton.render("+1 ticket", True, BLANC)
            screen.blit(txt_bonus, (btn_bonus.centerx - txt_bonus.get_width()//2,
                                    btn_bonus.centery - txt_bonus.get_height()//2))
            
            # Affichage (100 pts)
            btn_bonus_prix = btn_bonus.copy()
            btn_bonus_prix.width //= 2 # Moitié de la largeur

            if joueur_actif == 1:
                # Affichage à droite pour joueur 1
                btn_bonus_prix.x += btn_bonus.width +20 # Décalage horiozontal

            else:
                # Prix à gauche pour joueur 2
                btn_bonus_prix.x -= btn_bonus_prix.width + 20

            pg.draw.rect(screen, (80, 80, 80), btn_bonus_prix, border_radius=12)
            txt_prix_bonus = font_prix.render("100 pts", True, BLANC)
            screen.blit(txt_prix_bonus, (btn_bonus_prix.centerx - txt_prix_bonus.get_width()//2,
                             btn_bonus_prix.centery - txt_prix_bonus.get_height()//2))


            if joueur_actif == 1:
                btn_creer_unite.topleft = (50, hauteur//2 + 50)

            else:
                btn_creer_unite.topright = (largeur - 50, hauteur//2 + 50)
            

            # ----- Bouton unité ----- 
            if mode_creation_unite:
                # Bouton actif : fond gris + bordure bleue
                pg.draw.rect(screen, (60, 60, 60), btn_creer_unite, border_radius=12)
                pg.draw.rect(screen, BLEU, btn_creer_unite, width=3, border_radius=12)

            else: 
                # Bouton normal
                pg.draw.rect(screen, (100, 100, 255), btn_creer_unite, border_radius=12)


            # Affichage Bouton (+1 unité)
            if mode_creation_unite:
                pg.draw.rect(screen, (60, 60, 60), btn_creer_unite, border_radius=12)
                pg.draw.rect(screen, BLEU, btn_creer_unite, width=3, border_radius=12)

            else:
                pg.draw.rect(screen, (100, 100, 255), btn_creer_unite, border_radius=12)

            txt_creer = font_bouton.render("+1 unité", True, BLANC)
            screen.blit(txt_creer, (btn_creer_unite.centerx - txt_creer.get_width()//2,
                                    btn_creer_unite.centery - txt_creer.get_height()//2))

            # Affichage (500 pts)
            btn_unite_prix = btn_creer_unite.copy()
            btn_unite_prix.width //= 2 # Moitié de la largeur

            if joueur_actif == 1:
                # Affichage à droite pour joueur 1
                btn_unite_prix.x += btn_creer_unite.width + 20

            else:
                # Affichage à gauche pour joueur 2
                btn_unite_prix.x -= btn_unite_prix.width + 20



            pg.draw.rect(screen, (80, 80, 80), btn_unite_prix, border_radius=12)
            txt_prix_unite = font_prix.render("500 pts", True, BLANC)
            screen.blit(txt_prix_unite, (btn_unite_prix.centerx - txt_prix_unite.get_width()//2,
                                        btn_unite_prix.centery - txt_prix_unite.get_height()//2))


        if menu_actif:
            btn_quitter_jeu, btn_fermer_menu = afficher_menu()

        if mode_creation_unite:
            mx, my = pg.mouse.get_pos()
            grid_i = (my - offset_y) // taille
            grid_j = (mx - offset_x) // taille
            nrows = len(grid_points)
            ncols = len(grid_points[0])
            
            if 0 <= grid_i < nrows and 0 <= grid_j < ncols:
                x = offset_x + grid_j * taille + (taille * 0.15)
                y = offset_y + grid_i * taille + (taille * 0.15)
                unite_size = int(taille * 0.7)
                pg.draw.rect(screen, interface.joueurs[joueur_actif]["color"],
                             (x, y, unite_size, unite_size), 2)

        pg.display.flip()

    return retour_menu
# ------------------------------------------------------- #


# ------------------------ MAIN ------------------------- #
while True:
    page_accueil()
    retour = jeu()
    if not retour:
        break

pg.quit()
sys.exit()
# ------------------------------------------------------- #

