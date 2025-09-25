import pygame as pg

class affichage_joueurs: 
    def __init__(self, screen, joueur_1_color, joueur_2_color):
        self.screen = screen
        self.font = pg.font.SysFont("Arial", 24, bold=True)

        # Données des joueurs
        self.joueurs = {
            1: {"points": 0, "tickets": 0, "color": joueur_1_color, "nom": "joueur 1"},
            2: {"points": 0, "tickets": 0, "color": joueur_2_color, "nom": "joueur 2"}
        }



    # --------------------- LOGIQUE ------------------------- #
    def update_tickets(self):
        # Ajoute +2 tickets à chaque joueur (appelé à chaque tour)
        for j in self.joueurs.values():
            j["tickets"] += 15                                           ########## Change intial 2


    def add_points(self, joueur, amount):
        # Ajoute des points au joueur (1 ou 2)
        if joueur in self.joueurs:
            self.joueurs[joueur]["points"] += amount
    # ------------------------------------------------------- #



    # -------------------- AFFICHAGE ------------------------ #
    def draw(self, joueur_actif=None):                              #####
        # Affiche le menu à gauche et à droite de l'écran
        WIDTH, HEIGHT = self.screen.get_size()

        # # Joueur 1 (gauche)
        # self._draw_joueur(
        #     x=20,
        #     joueur=self.joueurs[1]
        # )

        # Joueur 1                                                  #####
        self._draw_joueur(20, self.joueurs[1], actif=(joueur_actif == 1))

        # Joueur 2                                                  #####
        self._draw_joueur(WIDTH - 200, self.joueurs[2], actif=(joueur_actif == 2))

        # # Joueur 2 (droite)
        # self._draw_joueur(
        #     x=WIDTH - 200, # Décalé sur la droite
        #     joueur=self.joueurs[2]
        # )



    def _draw_joueur(self, x, joueur, actif=False):                 #####
        # Affiche les infos d'un joueur
        y = 100 # Marge haut

        # Si joueur actif : couleur spéciale                        #####
        color_nom = (255, 255, 0) if actif else joueur["color"]

        titre = self.font.render(joueur["nom"], True, color_nom)    #####
        points = self.font.render(f"Points: {joueur['points']}", True, (255, 255, 255))
        tickets = self.font.render(f"Tickets: {joueur['tickets']}", True, (255, 255, 255))

        # Si actif : encadré autour
        if actif:
            pg.draw.rect(self.screen, (255, 215, 0), (x-10, y-10, 180, 120), 3, border_radius=8)

        self.screen.blit(titre, (x, y))
        self.screen.blit(points, (x, y + 40))
        self.screen.blit(tickets, (x, y + 80))
    # ------------------------------------------------------- #
