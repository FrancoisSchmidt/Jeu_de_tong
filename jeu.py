import numpy as np
import random as rd
import time
from ui import *     #Données de l'IHM

"""@auteurs : Pierre Savignac et François Schmidt"""

class Entite():             #Une entité a un nom et des points
    def __init__(self,nom):
        self.id=nom
        self.points = 0

class Joueur(Entite):       #Une entité peut être un joueur physique
    pass

class Ia(Entite):           #Ou un ordinateur
    def __init__(self):
        super().__init__(nom='Ordi')    #Dont le nom sera 'Ordi' par défaut




class Plateau(np.ndarray):
    def __new__(cls, xmax,ymax,cam,inter):
        return super(Plateau, cls).__new__(cls, (xmax, ymax)) #création du plateau sous forme d'un array

    """La classe plateau hérite d'un ndarray, ce qui permet d'y stocker les jetons de nourriture
    en tant qu'entiers de 1 à 5. A l'intérieur, le caméléon y est représenté sous la forme d'un 9.
    Le plateau est de taille 7x7 : 5x5 sont alloués aux jetons, les cases restantes entourent ce carré de
    5x5 et forment le contour sur lequel le caméléon pourra aller"""

    def __init__(self,xmax,ymax,cam,inter):
        self[:,:]=0
        self[0,0]=-1
        self[0,-1]=-1
        self[-1,0]=-1
        self[-1,-1]=-1              #Les -1 désignent les cases inaccessibles pour le caméléon
        self.c = cam
        self[self.c.pos[0],self.c.pos[1]]=9   #Le chiffre 9 désigne le caméléon
        self.choix=42               #Self.choix est initialisé à une valeur bidon
        self.menu=[]                #Le "menu" correspond à la ligne ou colonne de nourriture en face du caméléon
        self.coup_gagnant=False     #Permet de savoir si le choix peut faire gagner l'IA au tour n+1 (IA normale)
        self.coup_perdant=False     #Permet de savoir si le choix peut faire perdre l'IA au tour n+2 (IA difficile)
        self.coup_ultime=False
        self.annulation=False       #Sert a savoir si un joueur propose une hausse de mise et l'autre refuse
        self.rejouer=False          #Sert à jouer quand un joueur propose une hausse de mise et l'autre accepte
        self.ui=inter               #Self.ui est du type JeuUi(), la classe correspondant au menu


    def calcul_menu(self,x,y):
        """La fonction calcul_menu permet d'actualiser la ligne ou colonne qui est en face
        du caméléon, contenant ainsi les éléments qu'il peut manger"""
        self.menu = []
        if y == 0 or y == 6:
            for i in range(1, 6):
                self.menu.append(self[x, i])
        if x == 0 or x == 6:
            for i in range(1, 6):
                self.menu.append(self[i, y])


    def un_tour_joueur(self):
        """La méthode un_tour_joueur permet à un joueur de jouer un coup en lui demandant
        ce qu'il veut manger, et en vérifiant s'il peut le faire. Le cas échéant, cette méthode appelle
        la méthode bouger qui fera bouger le caméléon du nombre de jetons mangés.
        Cette méthode est utilisée dans le mode un joueur, et l'était dans le mode 2 joueurs sans mise que nous avons décidé de
        supprimer étant devenu obsolète"""
        self.calcul_menu(self.c.pos[0],self.c.pos[1])   #On initialise le menu

        manges = 0  #Compteur de jetons mangés afin de connaître de combien de cases avancer
        if self.c.pos[1] == 0 or self.c.pos[1] == 6:      #Si on est sur colonne de gauche ou de droite
            for i in range(1, 6):
                if self[self.c.pos[0], i] == self.ui.window2.choix_ui:   #Le choix est défini par le clic de souris. On le récupère dans la classe PlateauUi
                    self[self.c.pos[0], i] = 0                           #On efface les jetons qui on été mangés
                    manges += 1                                          #Pour chaque jeton mangé, on augmente ce compteur d'1
        if self.c.pos[0] == 0 or self.c.pos[0] == 6:      #Si on est sur ligne du haut ou du bas
            for i in range(1, 6):
                if self[i, self.c.pos[1]] == self.ui.window2.choix_ui:
                    self[i, self.c.pos[1]] = 0
                    manges += 1
        self.c.bouger(manges,self)                      #Appelle la méthode bouger de caméléon pour bouger de "manges" pas
        self.ui.window2.actualiser_jetons()             #Permet d'actualiser l'interface graphique (les jetons mangés disparaissent car sont égaux à 0)
        self.calcul_menu(self.c.pos[0],self.c.pos[1])   #On reactualise le menu du caméléon


    def un_tour_joueur_mise(self,a):
        """La méthode un_tour_joueur_mise permet à un joueur de jouer un coup comme dans la fonction
        un_tour_joueur, a la différence que celle-ci gère le système de mise.
        A chaque fois qu'on demande à un joueur ce qu'il peut manger, il a la possibilité d'écrire "Oui" et donc
        d'augmenter la mise en jeu. Le joueur adverse pourra décliner l'enchère (et le joueur proposant gagne
        autant de points que la précédente mise) ; ou accepter l'enchère (mise +1) et donc le proposant peut
        jouer (grace a self.rejouer qui deviendra True)"""
        self.calcul_menu(self.c.pos[0],self.c.pos[1])   #Actualisation du menu

        """Le code ci-dessous annoté correspond au code fonctionnant sur console. Maintenant que l'on a une IHM,
        il n'est de plus aucune utilité"""
        # self.annulation=False   #Initialisation de annulation
        # self.rejouer=False      #Et de rejouer
        # while (int(choix) not in self.menu or int(choix)==0 )and a.m.mise<5: #Mise max=5
        #     choix = input('Manger quoi ? Augmenter la mise ? [{Numéro}/Oui]')
        #     if choix=='Oui':    #S'il veut augmenter la mise
        #         accepte = input('Enchère acceptée ? [Oui/Non]') #On demande à l'adversaire s'il est d'accord
        #         if accepte == 'Oui':                        #Si oui
        #             a.m.incrementer_mise()                  #La mise +1
        #             print('La mise est de : ' + str(a.m))   #On affiche la mise
        #             self.rejouer=True                       #On permet au joueur qui a proposé de jouer son tour
        #             break                                   #On quitte la boucle while (car "Oui" n'est pas dans men)
        #         elif accepte == 'Non':                      #Si non
        #             self.annulation=True                    #Le proposeur a gagné les points de la mise précédente
        #             break                                   #On quitte la boucle while
        # if self.rejouer == True or a.m.mise==5:         #Si rejouer == True, on lui demande un choix de jeton à manger, sinon non
        #     while choix not in self.menu or choix == 0: #Puis meme principe que dans un_tour_joueur
        #         choix = int(input('Manger quoi ?'))     #On appelle pas la fonction un_tour_joueur car celle-ci fait

        manges = 0
        if self.c.pos[1] == 0 or self.c.pos[1] == 6:                        #Si on se situe la première ou dernière colonne
            for i in range(1, 6):
                if self[self.c.pos[0], i] == self.ui.window2.choix_ui:      #Le choix est défini par le clic de souris. On le récupère dans la classe PlateauUi
                    self[self.c.pos[0], i] = 0                              #On mange les jetons qui n'ont pas eu de chance
                    manges += 1                                             #Et on augmente le compteur
        if self.c.pos[0] == 0 or self.c.pos[0] == 6:
            for i in range(1, 6):
                if self[i, self.c.pos[1]] == self.ui.window2.choix_ui:
                    self[i, self.c.pos[1]] = 0
                    manges += 1

        if self.annulation==False:                          #Si annulation == True, le proposant a gagné les points -> pas besoin de faire jouer
            self.c.bouger(manges,self)                      #Si annulation==False, la mise est augmentée et le proposant peut jouer
            self.ui.window2.actualiser_jetons()             #Le choix est défini par le clic de souris. On le récupère dans la classe PlateauUi
            self.calcul_menu(self.c.pos[0], self.c.pos[1])  #On reactualise le menu du caméléon après le mouvement



    def un_tour_ia_facile(self):
        """@author : François"""
        """Permet à l'ordinateur en difficulté facile de jouer. Le jeton qu'il va manger est simplement
        choisi aléatoirement"""
        self.calcul_menu(self.c.pos[0],self.c.pos[1]) #On actualise le menu
        choix = 0

        while choix == 0:
            choix = rd.choice(self.menu) #L'ordi choisit un jeton dans le menu qui n'est pas un 0
        manges = 0
        if self.c.pos[1] == 0 or self.c.pos[1] == 6:
            for i in range(1, 6):
                if self[self.c.pos[0], i] == choix:
                    self[self.c.pos[0], i] = 0
                    manges += 1
        if self.c.pos[0] == 0 or self.c.pos[0] == 6:
            for i in range(1, 6):
                if self[i, self.c.pos[1]] == choix:
                    self[i, self.c.pos[1]] = 0
                    manges += 1
        self.c.bouger(manges,self)                  #Permet à l'ordi de bouger
        self.ui.window2.actualiser_jetons()
        self.ui.window2.info.setText("L'ordi a mangé "+str(manges)+ " "+str(self.ui.window2.type(choix,manges)))   #On indique dans l'IHM ce que l'ordi a mangé
        self.calcul_menu(self.c.pos[0],self.c.pos[1])  #Actualise le menu en face du caméléon



    def un_tour_ia_normale(self):
        """@author François"""
        """Permet à l'ordinateur en difficulté normale de jouer. Le jeton qu'il va manger n'est plus choisi
        aléatoirement. L'IA va jouer son coup de telle manière a essayer de faire perdre le joueur.
        L'ordi regarde tous les choix disponibles dans le menu, et pour chaque cas, il regarde si manger
        ce jeton peut faire perdre le joueur. Le cas échéant il choisit cette option, et le cas contraire
        il appelle la méthode un_tour_ia_facile afin de jouer aléatoirement"""
        self.calcul_menu(self.c.pos[0],self.c.pos[1]) #On actualise le menu
        ancien_menu=self.menu                         #L'ancien menu est en fait le menu actuel. Cependant le self.menu prendra la valeur du menu au coup n+1
        self.coup_gagnant=False                       #Si une option est trouvée pour faire perdre le joueur, coup_difficile=True
        for choix in ancien_menu:
            a_remettre = []       #Stocke les jetons mangés pour faire la projection. Si on mange pas on les remettra après
            manges_theorique = 0  #Même chose que pour les méthode précédentes, mais en théorie
            if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                for i in range(1, 6):
                    if self[self.c.pos[0], i] == choix:
                        manges_theorique += 1
                        self[self.c.pos[0], i] = 0           #On enlève ce choix théorique
                        a_remettre.append([self.c.pos[0],i]) #Mais on le stocke si on doit le remettre (si on choisi pas celui-la)
            if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                for i in range(1, 6):
                    if self[i, self.c.pos[1]] == choix:
                        manges_theorique += 1
                        self[i, self.c.pos[1]] = 0           #Pareil
                        a_remettre.append([i, self.c.pos[1]])

            position_theorique=self.c.projection(self.c.pos[0],self.c.pos[1],manges_theorique)
            #La fonction projection est définie dans la classe Caméléon, elle permet de retourner la position que le
            #caméléon aurait s'il avait bougé de "manges_theorique" pas

            self.calcul_menu(position_theorique[0],position_theorique[1]) #On calcul le menu théorique qui sera stocké dans self.menu

            if self.menu==[0.0,0.0,0.0,0.0,0.0] and choix!=0:             #On vérifie si le choix permet de gagner au tour n+1
                if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                    for i in range(1, 6):
                        if self[self.c.pos[0], i] == choix:
                            self[self.c.pos[0], i] = 0
                if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                    for i in range(1, 6):
                        if self[i, self.c.pos[1]] == choix:
                            self[i, self.c.pos[1]] = 0
                self.c.bouger(manges_theorique,self)                      #Le cas échéant, on fait le mouvement
                self.ui.window2.info.setText("L'ordi a mangé " + str(manges_theorique) + " " + str(self.ui.window2.type(choix, manges_theorique)))  #On indique dans l'IHM ce que l'ordi a mangé
                self.coup_gagnant = True                        #Coup_gagnant servira pour l'IA difficile
                break                                           #Et on sort du for

            #Remise des choix enlevés si l'option ne permet pas de faire gagner au coup suivant (pas de break activé)
            for w in a_remettre:
                self[w[0], w[1]] = choix

        self.calcul_menu(self.c.pos[0],self.c.pos[1])  #On réactualise le menu
        #Si aucun choix ne peut faire gagner l'IA, rien ne se passe à l'appelle de cette fonction
        #Le coup sera donc aléatoire, et la fonction un_tour_ia_facile sera appelée dans la classe arbitre



    def un_tour_ia_difficile(self):
        """@author François"""
        """L'IA difficile est planifiée pour être un peu plus élaborée.
        Elle va d'abord faire appel à l'IA normale afin de voir si elle peut faire un coup gagnant.
        Le cas échéant, elle le fait.
        Le cas contraire, elle va chercher à jouer (si elle le peut biensûr) un coup qui ne puisse pas lui faire perdre.
        Pour chaque possibilité, il suffit de regarder les choix du joueur pour voir si un menerait vers une ligne de 0
        Il faudra donc utiliser deux fois la fonction projection"""
        self.calcul_menu(self.c.pos[0],self.c.pos[1])   #Actualisation du menu
        self.un_tour_ia_normale()                       #On applique l'IA normale. S'il peut pas faire gagner, rien ne se passe.
        self.calcul_menu(self.c.pos[0],self.c.pos[1])   #Actualisation du menu (on est jamais trop prudent)
        premier_menu=self.menu                          #Premier menu est en fait le menu actuel. Cependant le self.menu prendra la valeur du menu anticipé au coup n+1

        if self.coup_gagnant==False: #Si l'IA ne peut pas gagner en jouant (si p.un_tour_ia_normale n'a pas aboutit)
            choix_perdants=[]        #Liste des choix qui feraient perdre l'IA
            for choix in premier_menu:
                self.coup_perdant=False
                a_remettre1 = []
                manges_theorique1 = 0  #Même chose que pour les méthodes précédentes
                if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                    for i in range(1, 6):
                        if self[self.c.pos[0], i] == choix:
                            manges_theorique1 += 1
                            self[self.c.pos[0], i] = 0              #On l'enlève
                            a_remettre1.append([self.c.pos[0], i])  #Mais on le stock si on doit le remettre
                if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                    for i in range(1, 6):
                        if self[i, self.c.pos[1]] == choix:
                            manges_theorique1 += 1
                            self[i, self.c.pos[1]] = 0
                            a_remettre1.append([i, self.c.pos[1]])
                position_theorique_n_plus_1 = self.c.projection(self.c.pos[0],self.c.pos[1],manges_theorique1)

                """La position_theorique_n_plus_1 est donc la ligne (non nulle) face à laquelle se retrouve le joueur.
                Nous allons donc regarder tous les choix possibles pour le joueur afin de voir si le joueur peut manger
                un type de jeton lui permettant de gagner """

                self.calcul_menu(position_theorique_n_plus_1[0],position_theorique_n_plus_1[1]) #On estime le nouveau menu
                second_menu=self.menu                                                           #Et on l'appelle secon_menu : c'est donc le menu du joueur

                for choix2 in second_menu:
                    a_remettre2 = []       #Stocke les jetons mangés pour faire la projection. Si on mange pas on les remettra
                    manges_theorique2 = 0  #Même chose que pour les méthode précédentes
                    if position_theorique_n_plus_1[1] == 0 or position_theorique_n_plus_1[1] == 6:
                        for i in range(1, 6):
                            if self[position_theorique_n_plus_1[0], i] == choix2:
                                manges_theorique2 += 1
                                self[position_theorique_n_plus_1[0], i] = 0
                                a_remettre2.append([position_theorique_n_plus_1[0], i])
                    if position_theorique_n_plus_1[0] == 0 or position_theorique_n_plus_1[0] == 6:
                        for i in range(1, 6):
                            if self[i, position_theorique_n_plus_1[1]] == choix2:
                                manges_theorique2 += 1
                                self[i, position_theorique_n_plus_1[1]] = 0
                                a_remettre2.append([i, position_theorique_n_plus_1[1]])

                    position_theorique_n_plus_2 = self.c.projection(position_theorique_n_plus_1[0],position_theorique_n_plus_1[1],manges_theorique2)
                    self.calcul_menu(position_theorique_n_plus_2[0],position_theorique_n_plus_2[1])
                    #Desormais self.menu correspond au menu que l'ordi se confronté au tour n+2
                    if self.menu == [0.0, 0.0, 0.0, 0.0, 0.0] and choix2 != 0: #On regarde si ça peut le mener à la défaite
                        self.coup_perdant = True                               #Le cas échéant coup_perdant=True

                    for w in a_remettre2:               #On remet la 2e série de choix en place
                        self[w[0], w[1]] = choix2

                if self.coup_perdant==True:
                    choix_perdants.append(choix)  #on ajoute le choix perdant à la liste (choix et pas choix2)

                for v in a_remettre1:
                    self[v[0], v[1]] = choix  #On remet la 1e série de choix en place
            #Fin du premier for

            #Maintenant on a une liste choix_perdants, de choix qu'il ne faut donc pas faire
            self.calcul_menu(self.c.pos[0], self.c.pos[1]) #On actualise le menu
            choix_final = 0
            if [i for i in self.menu if i not in choix_perdants and i!=0] ==[]: #Liste des choix sans les choix perdants et les 0
                choix_final = rd.choice([j for j in self.menu if j!=0])         #L'ordi a compris qu'il a perdu quoiqu'il fasse. Il joue au hasard
            else:
                choix_final = rd.choice([i for i in self.menu if i not in choix_perdants and i!=0])  #Il choisit un jeton dans le menu qui n'est pas un 0
            manges = 0                               #On fait jouer l'ordi
            if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                for i in range(1, 6):
                    if self[self.c.pos[0], i] == choix_final:
                        self[self.c.pos[0], i] = 0
                        manges += 1
            if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                for i in range(1, 6):
                    if self[i, self.c.pos[1]] == choix_final:
                        self[i, self.c.pos[1]] = 0
                        manges += 1
            self.c.bouger(manges,self)                   #Permet à l'ordi de bouger
            self.ui.window2.info.setText("L'ordi a mangé " + str(manges) + " " + str(self.ui.window2.type(choix_final, manges)))  #On indique dans l'IHM ce que l'ordi a mangé
            self.calcul_menu(self.c.pos[0], self.c.pos[1])  #Actualise le menu en face du caméléon



    def un_tour_ia_impossible(self):
        """@author François"""
        """L'IA très_difficile (notée impossible pour pas d'accents) est planifiée pour être encore plus élaborée.
        Elle va d'abord faire appel à l'IA normale afin de voir si elle peut faire un coup gagnant.
        Le cas échéant, elle le fait.
        Le cas contraire, elle va faire comme l'ia difficile -> chercher à jouer (si elle le peut biensûr) un coup 
        qui ne puisse pas lui faire perdre. Si le coup ferait perdre l'ordi, il est placé dans la liste des coups perdants.
        Cependant si le coup ne fait pas perdre, on fait encore une projection et on regarde si ce coup peur faire gagner
        au coup n+2 et donc d'avoir gagné au coup n+3. S'il y a une possibilité que le joueur face un mauvais choix
        et que l'ordi gagne ensuite, le choix est mis dans une liste choix_gagnant.
        Si l'ordi est sur de gagner au n+3 (parce que le joueur n'aura qu'un seul choix possible au n+2 par exemple), alors 
        ce choix sera mis dans choix_ultime.
        Les choix de choix_ultime primes sur ceux de choix_gagnants. Logique"""
        self.calcul_menu(self.c.pos[0], self.c.pos[1])  # Actualisation du menu
        self.un_tour_ia_normale()  # On applique l'IA normale. S'il peut pas faire gagner, rien ne se passe.
        self.calcul_menu(self.c.pos[0], self.c.pos[1])  # Actualisation du menu (on est jamais trop prudent)
        premier_menu = self.menu  # Premier menu est en fait le menu actuel. Cependant le self.menu prendra la valeur du menu anticipé au coup n+1

        if self.coup_gagnant == False:  #Si l'IA ne peut pas gagner en jouant (si p.un_tour_ia_normale n'a pas aboutit)
            choix_perdants = []  #Liste des choix qui feraient perdre l'IA
            choix_gagnants = []  #Liste des choix qui pourraient faire gagner l'IA
            choix_ultime =[]     #Liste des choix qui feront gagner l'IA
            for choix in premier_menu:   #Choix de l'ordi en premier_menu
                if choix!=0:             #Si le choix est différent de 0
                    self.coup_perdant = False  #Pour l'instant le coup n'est pas jugé perdant
                    self.coup_ultime = True    #Mais est jugé gagnant (self.coup_gagnant était deja prix)
                    a_remettre1 = []           #Pour remettre la première série de jetons mangés
                    manges_theorique1 = 0  #Même chose que pour les méthodes précédentes
                    if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                        for i in range(1, 6):
                            if self[self.c.pos[0], i] == choix:
                                manges_theorique1 += 1
                                self[self.c.pos[0], i] = 0
                                a_remettre1.append([self.c.pos[0], i])  #Mais on le stocke si on doit le remettre
                    if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                        for i in range(1, 6):
                            if self[i, self.c.pos[1]] == choix:
                                manges_theorique1 += 1
                                self[i, self.c.pos[1]] = 0
                                a_remettre1.append([i, self.c.pos[1]])
                    position_theorique_n_plus_1 = self.c.projection(self.c.pos[0], self.c.pos[1], manges_theorique1)

                    """La position_theorique_n_plus_1 est donc la ligne (non nulle) face à laquelle se retrouve le joueur.
                    Nous allons donc regarder tous les choix possibles pour le joueur afin de voir si le joueur peut manger
                    un type de jeton lui permettant de gagner """

                    self.calcul_menu(position_theorique_n_plus_1[0],position_theorique_n_plus_1[1])  # On estime le nouveau menu
                    second_menu = self.menu  # Et on l'appelle secon_menu : c'est donc le menu du joueur

                    for choix2 in second_menu:  # Choix possible du joueur
                        a_remettre2 = []  # Stocke les jetons mangés pour faire la projection. Si on mange pas on les remettra
                        if choix2 != 0:   #Si le choix du joueur est non nul
                            manges_theorique2 = 0  #Même chose que pour les méthode précédentes
                            if position_theorique_n_plus_1[1] == 0 or position_theorique_n_plus_1[1] == 6:
                                for i in range(1, 6):
                                    if self[position_theorique_n_plus_1[0], i] == choix2:
                                        manges_theorique2 += 1
                                        self[position_theorique_n_plus_1[0], i] = 0
                                        a_remettre2.append([position_theorique_n_plus_1[0], i])
                            if position_theorique_n_plus_1[0] == 0 or position_theorique_n_plus_1[0] == 6:
                                for i in range(1, 6):
                                    if self[i, position_theorique_n_plus_1[1]] == choix2:
                                        manges_theorique2 += 1
                                        self[i, position_theorique_n_plus_1[1]] = 0
                                        a_remettre2.append([i, position_theorique_n_plus_1[1]])

                            position_theorique_n_plus_2 = self.c.projection(position_theorique_n_plus_1[0],position_theorique_n_plus_1[1],manges_theorique2)
                            self.calcul_menu(position_theorique_n_plus_2[0], position_theorique_n_plus_2[1])
                            troisieme_menu = self.menu  #C'est donc le menu de l'ordi au tour n+2
                            # Desormais self.menu correspond au menu que l'ordi se confronté au tour n+2
                            if self.menu == [0.0, 0.0, 0.0, 0.0,0.0] and choix2 != 0:  # On regarde si ça peut le mener à la défaite de l'IA
                                self.coup_perdant = True  #Le cas échéant coup_perdant=True
                                self.coup_ultime=False    #Le coup est perdant, donc pas gagnant

                            if self.coup_perdant==False:  #Si le coup n'est pas perdant
                                for choix3 in troisieme_menu:  #Choix possibles de l'ordi
                                    a_remettre3 = []
                                    if choix3 != 0:
                                        manges_theorique3 = 0
                                        if position_theorique_n_plus_2[1] == 0 or position_theorique_n_plus_2[1] == 6:
                                            for i in range(1, 6):
                                                if self[position_theorique_n_plus_2[0], i] == choix3:
                                                    manges_theorique3 += 1
                                                    self[position_theorique_n_plus_2[0], i] = 0
                                                    a_remettre3.append([position_theorique_n_plus_2[0], i])
                                        if position_theorique_n_plus_2[0] == 0 or position_theorique_n_plus_2[0] == 6:
                                            for i in range(1, 6):
                                                if self[i, position_theorique_n_plus_2[1]] == choix3:
                                                    manges_theorique3 += 1
                                                    self[i, position_theorique_n_plus_2[1]] = 0
                                                    a_remettre3.append([i, position_theorique_n_plus_2[1]])
                                        position_theorique_n_plus_3 = self.c.projection(position_theorique_n_plus_2[0],position_theorique_n_plus_2[1],manges_theorique3)
                                        self.calcul_menu(position_theorique_n_plus_3[0], position_theorique_n_plus_3[1])  # Donc la on a le menu du joueur
                                        if self.menu == [0.0, 0.0, 0.0, 0.0,0.0] and choix2 != 0 and choix3 != 0:  # On regarde si ça peut le mener à la défaite du joueur
                                            self.coup_ultime = True   #Si oui, c'est un coup gagnant
                                        else:
                                            self.coup_ultime = False  #Si non, ce n'est pas un coup gagnant

                                    for x in a_remettre3:   #On remet la 3e série de choix en place
                                        self[x[0], x[1]] = choix3

                        for w in a_remettre2:  # On remet la 2e série de choix en place
                            self[w[0], w[1]] = choix2

                    uniq=True
                    doublons=[]
                    for i in second_menu:
                        if i in doublons and i!=0:
                            uniq=False
                        doublons.append(i)
                    #Si uniq==False, alors le menu est composé de doublons
                    #Si uniq==True alors le menu n'est pas composé de doublons
                    #Et donc le joueur n'a pas le choix et perdra. Ce type de choix est prioritaire

                    if self.coup_perdant == True:
                        choix_perdants.append(choix)  #On ajoute le choix perdant à la liste (choix et pas choix2) A NE PAS JOUER
                    if self.coup_ultime==True:        #Liste de choix à jouer
                        choix_gagnants.append(choix)
                    #Que des nombres différents dans second_menu: -> implique pas le choix donc victoire
                    if self.coup_ultime==True and uniq==True: #Un choix fatal
                        choix_ultime.append(choix)

                    uniq=False

                    for v in a_remettre1:
                        self[v[0], v[1]] = choix  # On remet la 1e série de choix en place
            # Fin du premier for

            print('Choix ultimes : ', choix_ultime)
            print('Choix gagnants : ', choix_gagnants)
            print('Choix perdants : ',choix_perdants)

            self.calcul_menu(self.c.pos[0], self.c.pos[1])  # On actualise le menu
            choix_final = 0
            if len(choix_ultime)>0:    #Choix prioritaire -> Fera gagné
                choix_final = rd.choice(choix_ultime)
            elif len(choix_gagnants)>0: #Choix second -> Fait peut-être gagner
                choix_final=rd.choice(choix_gagnants)
            else:  #Sinon on devra choisir un choix qui ne fait pas perdre au moins
                if [i for i in self.menu if i not in choix_perdants and i != 0] == []:  # Liste des choix sans les choix perdants et les 0
                    choix_final = rd.choice([j for j in self.menu if j != 0])  # L'ordi a compris qu'il a perdu quoiqu'il fasse. Il joue au hasard
                    print("J'admets ma défaite")
                else:
                    choix_final = rd.choice([i for i in self.menu if i not in choix_perdants and i != 0])  # Il choisit un jeton dans le menu qui n'est pas un 0
            manges = 0  # On fait jouer l'ordi
            if self.c.pos[1] == 0 or self.c.pos[1] == 6:
                for i in range(1, 6):
                    if self[self.c.pos[0], i] == choix_final:
                        self[self.c.pos[0], i] = 0
                        manges += 1
            if self.c.pos[0] == 0 or self.c.pos[0] == 6:
                for i in range(1, 6):
                    if self[i, self.c.pos[1]] == choix_final:
                        self[i, self.c.pos[1]] = 0
                        manges += 1
            self.c.bouger(manges, self)  #Permet à l'ordi de bouger
            self.ui.window2.info.setText("L'ordi a mangé " + str(manges) + " " + str(self.ui.window2.type(choix_final, manges)))  # On indique dans l'IHM ce que l'ordi a mangé
            self.calcul_menu(self.c.pos[0], self.c.pos[1])  #Actualise le menu en face du caméléon




class Cameleon():
    def __init__(self):
        self.nbre_coups=0
        self.pos = (3, 0)  # Position initiale du caméléon sur le plateau

    def bouger(self,pas,p):
        """La méthode bouger, prenant commme donnée le nombre de pas, permet au caméléon d'avancer.
        Comme nous sommes sur un plateau en ndarray, il est nécessaire de faire des disjonctions de cas
        pour savoir ou il se situe (a gauche, en haut, a droite ou en bas) et voir s'il devra changer
        de côté ou non"""

        p[self.pos[0],self.pos[1]]=0   #Caméléon éffacé sur le plateau

        if self.pos[1]==0:
            if pas<self.pos[0]:
                self.pos=(self.pos[0]-pas,0)
            elif pas==self.pos[0]:
                self.pos=(0,1)
            else:
                self.pos=(0,pas-self.pos[0]+1)

        elif self.pos[0]==0:
            if self.pos[1]+pas<=5:
                self.pos=(0,self.pos[1]+pas)
            elif self.pos[1]+pas==6:
                self.pos=(1,6)
            else:
                self.pos=(pas+self.pos[1]-5,6)

        elif self.pos[1]==6:
            if self.pos[0]+pas<=5:
                self.pos=(self.pos[0]+pas,6)
            elif self.pos[0]+pas==6:
                self.pos=(6,5)
            else:
                self.pos=(6,11-self.pos[0]-pas)

        elif self.pos[0]==6:
            if self.pos[1]==pas:
                self.pos=(5,0)
            elif pas<self.pos[1]:
                self.pos=(6,self.pos[1]-pas)
            else:
                self.pos=(5-(pas-self.pos[1]),0)

        p[self.pos[0],self.pos[1]]=9     #Position du caméléon mise a jour sur le plateau
        print(p)                         #Affichage su plateau actualisé dans la console (au cas ou vous voudriez revoir ce qui a été joué précédement)
        print('\n')


    def projection(self,x,y,pas):
        """Le caméléon ne bouge pas, on retourne seulement la position qu'il devrait avoir s'il faisait "pas" pas
        depuis la position (x,y)"""
        if y==0:
            if pas<x:
                return (x-pas,0)
            elif pas==x:
                return (0,1)
            else:
                return (0,pas-x+1)

        elif x==0:
            if y+pas<=5:
                return (0,y+pas)
            elif y+pas==6:
                return (1,6)
            else:
                return (pas+y-5,6)

        elif y==6:
            if x+pas<=5:
                return (x+pas,6)
            elif x+pas==6:
                return (6,5)
            else:
                return (6,11-x-pas)

        elif x==6:
            if y==pas:
                return (5,0)
            elif pas<y:
                return (6,y-pas)
            else:
                return (5-(pas-y),0)




"""Nous nous sommes rendus compte qu'une classe Nourriture pour gérer les jetons n'était
finallement pas très pertinante. Nous l'avons donc supprimée"""
# class Nourriture():
#     nombre_nourriture=0
#     liste=[]
#     def __init__(self,couleur):
#         if couleur in ['rouge', 'vert', 'bleu', 'jaune', 'gris']:
#             self.type=couleur
#         else:
#             self.type = rd.choice(['rouge', 'vert', 'bleu', 'jaune', 'gris'])
#         Nourriture.nombre_nourriture+=1
#
#     def __str__(self):
#         return self.type



class Arbitre():
    """Grosse classe qui va avoir pour but de superviser le jeu. C'est l'arbitre qui prend en compte
    le nombre de joueurs et leur nom, c'est lui qui réparti aléatoirement les jetons sur le plateau,
    c'est lui qui compte le nombre de jetons restants et enfin c'est lui qui lance les parties"""
    def __init__(self,plat,cam):
        self.nbre_joueurs=0           #Les noms de ces variables semblent claires
        self.liste_joueurs=[]
        self.liste_jetons=[]
        self.compteur=0               #Utilisé pour la mise en place des jetons
        self.difficulte_ia='Normale'  #Difficulté IA standard
        self.m=Mise()                 #La mise est affectée à l'arbitre, c'est lui qui gère ça
        self.p=plat                   #Correspond au plateau crée
        self.c=cam                    #Ainsi qu'au caméléon


    """Cette méthode permettait de récupérer les noms des joueurs. Comme elle fonctionne avec des input(),
    elle n'était donc pas compatible avec l'IHM
    La fenêtre pour rentrer les noms la remplace"""
    # def mise_en_place_joueurs(self):
    #     """Méthode permettant de choisir le mode de jeu et de renseigner le nom des joueurs"""
    #     self.liste_joueurs = []
    #     #self.nbre_joueurs = input('Nombre de joueurs ?')
    #     self.nbre_joueurs = int(self.nbre_joueurs)
    #     if self.nbre_joueurs != 1 and self.nbre_joueurs != 2 and self.nbre_joueurs!=3 and self.nbre_joueurs!=4:
    #         raise AttributeError
    #     else:
    #         if self.nbre_joueurs == 1: #Mode solo
    #             name=input('Nom')
    #             j1 = Joueur(name)
    #             self.liste_joueurs.append(j1)
    #         elif self.nbre_joueurs == 2 or self.nbre_joueurs==4: #Mode 2 joueurs. 2 sans mise. Et 4 avec mise
    #             name1 = input('Nom joueur 1')
    #             name2 = input('Nom joueur 2')
    #             j1 = Joueur(name1)
    #             j2 = Joueur(name2)
    #             self.liste_joueurs.append(j1)
    #             self.liste_joueurs.append(j2)
    #         elif self.nbre_joueurs == 3: #Mode 2 joueurs contre l'IA
    #             name=input('Nom')
    #             j1 = Joueur(name)
    #             j2 = Ia()
    #             self.liste_joueurs.append(j1)
    #             self.liste_joueurs.append(j2)
    #             tableau=['Facile', 'Normale', 'Difficile']
    #             self.difficulte_ia='a'
    #             while self.difficulte_ia not in tableau: #choisi la difficulté de l'IA
    #                 self.difficulte_ia=input("Difficulté de l'IA ? [Facile, Normale, Difficile]")


    def mise_en_place_jetons(self):
        """Méthode qui met en place les jetons de manière alatoire sur le plateau
        5 jetons de chaque"""
        self.liste_jetons = []
        self.compteur = 0
        for i in range(5):  #On met 5 jetons de chaque dans la liste
            self.liste_jetons.append('rouge')
            self.liste_jetons.append('vert')
            self.liste_jetons.append('bleu')
            self.liste_jetons.append('jaune')
            self.liste_jetons.append('gris')
        rd.shuffle(self.liste_jetons) #Permet de mélanger la liste de jetons qui sera repartie dans le plateau
        for i in range(1, 6):
            for j in range(1, 6):
                if self.liste_jetons[self.compteur] == 'rouge':
                    self.p[i, j] = 1
                if self.liste_jetons[self.compteur] == 'bleu':
                    self.p[i, j] = 2
                if self.liste_jetons[self.compteur] == 'vert':
                    self.p[i, j] = 3
                if self.liste_jetons[self.compteur] == 'jaune':
                    self.p[i, j] = 4
                if self.liste_jetons[self.compteur] == 'gris':
                    self.p[i, j] = 5
                self.compteur += 1      #Compteur servira pour vérifier qu'il y a bien 25 jetons sur le plateau


    def jetons_restants(self):
        """Méthode permettant de calculer le nombre de jetons restants en parcourant
        simplement le plateau de jeu a la fin de la partie.
        Utile pour le mode un joueur"""
        jetons=0
        for i in range(1, 6):
            for j in range(1, 6):
                if self.p[i,j]!=0:
                    jetons+=1
        return jetons



    """La méthode joueur servait avant à lancer les parties sur console. Ne fonctionnant pas très bien avec IHM (de par ses boucles while notamment,
    nous avons décidé de la supprimer, et de la remplacer par les méthodes PlateauUi.play() et PlateauUi.mousePressEvent()"""
    # def jouer(self):
    #     """Grosse méthode.
    #     Permer de lancer la partie. On regarde d'abord le type de jeu (de 1 à 4), et en fonction de ce dernier,
    #     on met en place les conditions d'arrêt de fin de partie, ainsi que les "scores" à afficher, comme
    #     le nombre de jetons restant ou le joueur qui a gagné"""
    #
    #     if self.nbre_joueurs==1: #Mode solo
    #
    #         print(self.p)
    #         self.p.un_tour_joueur()
    #
    #         while self.p.menu != [0.0,0.0,0.0,0.0,0.0]: #Condition de défaite -> se retrouver avec un menu nul
    #             self.p.un_tour_joueur()
    #         print('Jeu terminé')
    #         print('Il vous reste '+str(self.jetons_restants())+' jetons')
    #         if self.jetons_restants()==0:
    #             print('Vous avez gagné !')
    #
    #
    #
    #     elif self.nbre_joueurs==2: #Mode 2 joueurs sans mise
    #         print(self.p)
    #         while True: #Tant qu'une condition de défaite n'est pas remplie
    #             if self.p.menu == [0.0,0.0,0.0,0.0,0.0]: #Si le premier joueur est face aux 0
    #                 print('Partie terminée')
    #                 print("C'est "+str(self.liste_joueurs[1].id)+ ' qui gagne') #C'est le 2e joueur qui gagne
    #                 break
    #             else:
    #                 print(str(self.liste_joueurs[0].id) + ' à toi de jouer') #Si condition d'arret pas remplie
    #                 self.p.un_tour_joueur() #Le joueur joue
    #
    #             if self.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]: #On fait de même pour le tour du joueur 2
    #                 print('Partie terminée')
    #                 print("C'est " + str(self.liste_joueurs[0].id) + ' qui gagne')
    #                 break
    #             else:
    #                 print(str(self.liste_joueurs[1].id) + ' à toi de jouer')
    #                 self.p.un_tour_joueur()
    #
    #
    #     elif self.nbre_joueurs == 4: #Mode 2 joueurs avec système de mise
    #         manche=1 #Initialisation de manches
    #         while self.liste_joueurs[0].points<5 and self.liste_joueurs[1].points<5: #Le jeu s'arrête une fois qu'un joueur a 5 points
    #             print('\n')
    #             print('Manche ' + str(manche)) #Affichage numéro de manche
    #             print('Scores :')              #Affichage des scores
    #             print(str(self.liste_joueurs[0].id)+' : '+str(self.liste_joueurs[0].points)+ ' points')
    #             print(str(self.liste_joueurs[1].id)+' : '+str(self.liste_joueurs[1].points)+ ' points')
    #             manche+=1
    #             self.m.mise=1                    #Initialisation de la mise à 1
    #             self.mise_en_place_jetons()      #On remet en place les jetons
    #             self.p.calcul_menu(self.c.pos[0],self.c.pos[1]) #On recalcule le menu
    #             print(self.p)                         #Affichage du plateau
    #             while True: #Tant qu'une condition de défaite n'est pas remplie
    #                 if self.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:
    #                     print('Manche terminée')
    #                     print(str(self.liste_joueurs[1].id) + ' a gagné ' + str(self.m) + ' points')
    #                     self.liste_joueurs[1].points+=self.m.mise #Si le joueur 1 a une ligne de 0, le joueur 2 gagne autant de points que la mise
    #                     break
    #                 else:
    #                     print(str(self.liste_joueurs[0].id) + ' à toi de jouer')
    #                     self.p.un_tour_joueur_mise(self) #Sinon ca joue
    #                     if self.p.annulation==True:  #Si annulation est passe True dans la méthode un_tour_joueur_mise, c'est que le joueur 1 a proposé une enchère et le 2 a refusé
    #                         print('Manche terminée')
    #                         print(str(self.liste_joueurs[0].id) + ' a gagné ' + str(self.m) + ' points')
    #                         self.liste_joueurs[0].points += self.m.mise #Le joueur 1 remporte donc la mise précédant la demande d'enchère
    #                         break
    #
    #                 if self.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]: #Même processus avec le joueur 2
    #                     print('Manche terminée')
    #                     print(str(self.liste_joueurs[0].id) + ' a gagné ' + str(self.m) + ' points')
    #                     self.liste_joueurs[0].points+=self.m.mise
    #                     break
    #                 else:
    #                     print(str(self.liste_joueurs[1].id) + ' à toi de jouer')
    #                     self.p.un_tour_joueur_mise(self)
    #                     if self.p.annulation==True:
    #                         print('Manche terminée')
    #                         print(str(self.liste_joueurs[1].id) + ' a gagné ' + str(self.m) + ' points')
    #                         self.liste_joueurs[1].points += self.m.mise
    #                         break
    #
    #         #Si on est sorti de la boucle, c'est qu'un joueur a depassé les 5 points
    #         #On cherche a savoir lequel c'est pour dire qu'il a gagné
    #         print('Scores :')  # Affichage des scores
    #         print(str(self.liste_joueurs[0].id) + ' : ' + str(self.liste_joueurs[0].points) + ' points')
    #         print(str(self.liste_joueurs[1].id) + ' : ' + str(self.liste_joueurs[1].points) + ' points')
    #         if self.liste_joueurs[0].points>=5:
    #             print("\nC'est " + self.liste_joueurs[0].id + " qui remporte la partie. Félicitations !")
    #         elif self.liste_joueurs[1].points>=5:
    #             print("\nC'est " + self.liste_joueurs[1].id + " qui remporte la partie. Félicitations !")
    #
    #
    #     elif self.nbre_joueurs == 3: #Mode un joueur plus une IA
    #         #Exactememnt meme principe que pour le mode deux joueurs sans mise
    #         #Sauf que le niveau de difficulté rentre en compte
    #         self.p.calcul_menu(self.c.pos[0], self.c.pos[1])  #On recalcule le menu
    #         print(self.p)
    #         while True:
    #             if self.p.menu == [0.0,0.0,0.0,0.0,0.0]:
    #                 print('\n')
    #                 print('Partie terminée')
    #                 print("C'est l'Ordi qui gagne")
    #                 break
    #             else:
    #                 print(str(self.liste_joueurs[0].id) + ' à toi de jouer')
    #                 self.p.un_tour_joueur()
    #                 print('\n')
    #
    #
    #             if self.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:
    #                 print('Partie terminée')
    #                 print("C'est " + str(self.liste_joueurs[0].id) + ' qui gagne')
    #                 break
    #             else:
    #                 print(str(self.liste_joueurs[1].id) + ' à toi de jouer')
    #                 time.sleep(2)
    #                 if self.difficulte_ia=='Facile':      #Si IA facile, on appelle la fonction IA facile
    #                     self.p.un_tour_ia_facile()
    #                 elif self.difficulte_ia=='Normale':   #Si IA normale, on appelle la fonction IA normale
    #                     self.p.un_tour_ia_normale()
    #                     if self.p.coup_gagnant==False:         #Si on a pas trouvé de choix gagnant
    #                         self.p.un_tour_ia_facile()         #On joue aléatoirement grâce à al fonction IA Normale
    #                 elif self.difficulte_ia=='Difficile': #Si IA difficile, on appelle la fonction IA difficile
    #                     self.p.un_tour_ia_difficile()




class Mise():
    """Classe servant à gérer le système de mise"""
    def __init__(self):
        self.mise=1         #Initialisé à 1

    def incrementer_mise(self): #Permet d'augmenter la mise d'un
        if self.mise<5:         #Si elle n'est pas supérieure à 5 (car seulement 5 points sont nécessaires pour gagner)
            self.mise+=1

    def __str__(self):          #Affichage de la mise
        return str(self.mise)




# if __name__ == "__main__":
#     """Servait quand on voulait lancer le jeu sur console
#     Malheureusement ne fonctionne plus car adapté pour l'IHM"""
#     c = Cameleon()              #Création du caméléon
#     p = Plateau(7, 7, c)        #Création du plateau
#     a = Arbitre(p,c)              #Création de l'arbitre (et donc de la mise)
#     a.mise_en_place_joueurs()
#     a.mise_en_place_jetons()
#     a.jouer()                   #Lancement de la partie (préalablement on demande le type de jeu)