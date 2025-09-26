import pygame as pg, sys
from fonctions.Map import create_map, joueur_01, joueur_02, handle_click, afficher_victoire
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
VERT = (50, 200, 50)
# ------------------------------------------------------- #



# ----------------------- POLICE ------------------------ #
font_titre = pg.font.SysFont("arial", 60, bold=True)
font_bouton = pg.font.SysFont("arial", 40)
font_timer = pg.font.SysFont("arial", 48, bold=True)
# ------------------------------------------------------- #



# ---------------------- BOUTONS ------------------------ #
# Bouton Jouer
btn_jouer = pg.Rect(largeur//2 - 100, hauteur//2 - 40, 200, 80)

# Bouton Quitter
btn_quitter = pg.Rect(largeur//2 - 100, hauteur//2 + 60, 200, 80)

# Bouton Menu
btn_menu = pg.Rect(20, 20, 120, 50)

# Bouton Skip partie
btn_skip = pg.Rect(largeur//2 - 150, hauteur - 70, 300, 60)

# Bouton Bonus
btn_bonus = pg.Rect(0, 0, 250, 60)  
# ------------------------------------------------------- #



# --------------- FONCTION AFFICHER MENU ---------------- #
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
                    en_cours = False
                if btn_quitter.collidepoint(event.pos):
                    pg.quit()
                    sys.exit()

        screen.fill(BLANC)

        titre = font_titre.render("Territory Capture", True, NOIR)
        screen.blit(titre, (largeur//2 - titre.get_width()//2, 100))

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



# ------------------------ JEU -------------------------- #
def jeu():
    BCOLOR, case_original, pos_joueur_1, pos_joueur_2, taille, offset_x, offset_y, grid_points, joueurs_data = create_map(screen)
    interface = affichage_joueurs(screen, joueur_01, joueur_02)

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
                    interface.joueurs[joueur_actif]["tickets"] += 2 + interface.joueurs[joueur_actif]["bonus_tour_suivant"]
                    interface.joueurs[joueur_actif]["bonus_tour_suivant"] = 0
                    start_time = pg.time.get_ticks()
                    chrono = duree_tour


            if event.type == pg.MOUSEBUTTONDOWN:
                if menu_actif:
                    if btn_quitter_jeu and btn_quitter_jeu.collidepoint(event.pos):
                        retour_menu = True
                        running = False
                    if btn_fermer_menu and btn_fermer_menu.collidepoint(event.pos):
                        menu_actif = False
                        start_time = pg.time.get_ticks() - (duree_tour - chrono_en_pause) * 1000
                        if pause_start is not None:
                            pause_offset += pg.time.get_ticks() - pause_start
                            pause_start = None
                
                else:
                    if btn_menu.collidepoint(event.pos):
                        menu_actif = True
                        chrono_en_pause = chrono
                        pause_start = pg.time.get_ticks()
                        continue
                    
                    if btn_skip.collidepoint(event.pos):
                        joueur_actif = 2 if joueur_actif == 1 else 1
                        interface.joueurs[joueur_actif]["tickets"] += 2 + interface.joueurs[joueur_actif]["bonus_tour_suivant"]
                        interface.joueurs[joueur_actif]["bonus_tour_suivant"] = 0
                        start_time = pg.time.get_ticks()
                        chrono = duree_tour

                    if btn_bonus.collidepoint(event.pos):
                        joueur = interface.joueurs[joueur_actif]
                        if joueur["points"] >= 100:
                            joueur["points"] -= 100
                            joueur["bonus_tour_suivant"] += 1

                    mouse_pos = pg.mouse.get_pos()
                    resultat = handle_click(mouse_pos, case_original, joueur_actif, interface.joueurs,
                                            taille, offset_x, offset_y, grid_points, joueurs_data)

                    if isinstance(resultat, tuple) and resultat[0] == "VICTOIRE":
                        gagnant = joueur_actif
                        afficher_victoire(screen, gagnant, largeur, hauteur)
                        return True

        if not menu_actif:
            elapsed = (pg.time.get_ticks() - start_time) / 1000
            chrono = max(0, duree_tour - int(elapsed))

            if elapsed >= duree_tour:
                joueur_actif = 2 if joueur_actif == 1 else 1
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

        if temps_restant <=0:
            retour_menu = True
            running = False

        screen.fill((24, 26, 32))

        for rect, couleur, owner in case_original:
            pg.draw.rect(screen, couleur, rect)
            pg.draw.rect(screen, BCOLOR, rect, 1)
            
        if pos_joueur_1:
            i, j = pos_joueur_1
            pg.draw.rect(screen, (70, 130, 180), (offset_x + j*taille, offset_y + i*taille, taille, taille))

        if pos_joueur_2:
            i, j = pos_joueur_2
            pg.draw.rect(screen, (178, 34, 3), (offset_x + j*taille, offset_y + i*taille, taille, taille))

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

            # Bouton bonus du côté du joueur actif
            if joueur_actif == 1:
                btn_bonus.topleft = (50, hauteur//2 - 30)
            else:
                btn_bonus.topright = (largeur - 50, hauteur//2 - 30)

            pg.draw.rect(screen, VERT, btn_bonus, border_radius=12)
            txt_bonus = font_bouton.render("+1 Ticket", True, BLANC)
            screen.blit(txt_bonus, (btn_bonus.centerx - txt_bonus.get_width()//2,
                                    btn_bonus.centery - txt_bonus.get_height()//2))

        if menu_actif:
            btn_quitter_jeu, btn_fermer_menu = afficher_menu()

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