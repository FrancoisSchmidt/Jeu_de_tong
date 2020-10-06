import sys                                          #Pour l'interface
import os                                           #Pour la suppression du fichier de sauvegarde
from jeu import *                                   #Importation des éléments de jeu.py qui gèrent le gameplay
from PyQt5 import QtGui, QtCore, QtWidgets, uic     #Importations d'éléments de PyQt5
from pygame import mixer                            #Pour gérer la musique de fond
mixer.init()                                        #On initialise un mixer
mixer.music.load('jungle.mp3')                      #On charge la musique de fond

"""@auteurs : Pierre Savignac et François Schmidt"""


class JeuUi(QtWidgets.QMainWindow):
    """La classe JeuUi correspond à la fenêtre de départ qui permet de choisir à quel mode de jeu
    on veut jouer, de reprendre une partie sauvegardée, ou d'afficher les règles"""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('interface.ui', self)                      #Chargement de l'interface associée
        self.ui.bouton_un_joueur.clicked.connect(self.un_joueur)        #Bouton pour le mode 1 joueur
        self.ui.bouton_deux_joueurs.clicked.connect(self.deux_joueurs)  #Bouton pour le mode 2 joueurs avec mise
        self.ui.bouton_ia_facile.clicked.connect(self.ia_facile)        #Bouton pour le mode IA facile
        self.ui.bouton_ia_normale.clicked.connect(self.ia_normale)      #Bouton pour le mode IA normale
        self.ui.bouton_ia_difficile.clicked.connect(self.ia_difficile)  #Bouton pour le mode IA difficile
        self.ui.bouton_ia_impossible.clicked.connect(self.ia_impossible)#Bouton pour le mode IA très difficile
        self.ui.regle.clicked.connect(self.regles_jeu)                  #Bouton pour afficher les règles du jeu
        self.ui.sauveg.clicked.connect(self.recup_sauv)                 #Bouton pour reprendre la partie sauvegardée

        self.ui.actionSupprimer_la_sauvegarde.triggered.connect(self.suppr) #Dans onglet options permettant de supprimer la sauvegarde
        self.ui.actionQuitter.triggered.connect(self.close)                 #Dans onglet options pour quitter le jeu

        self.c = Cameleon()                      #Création du caméléon
        self.p = Plateau(7, 7, self.c,self)      #Création du plateau avec les dimensions, le caméléon et l'interface en paramètres
        self.a = Arbitre(self.p,self.c)          #Création de l'arbitre (et donc de la mise) avec le plateau et le caméléon en paramètres

        self.window2 = PlateauUi(self.p, self.a, 1)   #Cette fenêtre est le plateau de jeu qui s'ouvrira une fois le mode choisi (initialisé mode 1 joueur)

        palette = QtGui.QPalette()     #Ces 4 lignes servent pour l'image d'arrière plan
        pixmap = QtGui.QPixmap("fond_cameleon.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)

        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")   #Importation de la police "Jungle Roar" dans python grace à QtGui
        self.label_2.setFont(QtGui.QFont('Jungle Roar',pointSize=28))    #Le titre de la fenêtre sera écrit avec cette police


    def un_joueur(self):
        self.window2 = PlateauUi(self.p, self.a,1) #Plateau avec un 1 en paramètre pour plateau 1 joueur
        self.window2.show()                        #On l'affiche
        self.a.mise_en_place_jetons()              #On choisi une disposition aléatoire de jetons
        self.window2.actualiser_jetons()           #On place les jetons sur le plateau
        self.a.nbre_joueurs=1                      #Pour que window2.play() sache quel mode de jeu a été choisi
        self.close()                               #Fermeture du menu de selection
        mixer.music.play()                         #Permet de lancer la musique de fond

    def deux_joueurs(self):
        NamesUi(self).show()     #On ouvre la fenêtre pour rentrer les noms des 2 joueurs
        self.close()             #Fermeture du menu de selection

    def ia_facile(self):
        self.window2 = PlateauUi(self.p, self.a, 1)     #Même principe que la méthode un_joueur()
        self.window2.show()
        self.a.mise_en_place_jetons()
        self.window2.actualiser_jetons()
        self.a.nbre_joueurs = 3
        self.a.difficulte_ia='Facile'
        self.close()
        mixer.music.play()

    def ia_normale(self):
        self.window2 = PlateauUi(self.p, self.a, 1)     #Même principe que la méthode un_joueur()
        self.window2.show()
        self.a.mise_en_place_jetons()
        self.window2.actualiser_jetons()
        self.a.nbre_joueurs = 3
        self.a.difficulte_ia='Normale'
        self.close()
        mixer.music.play()

    def ia_difficile(self):
        self.window2 = PlateauUi(self.p, self.a, 1)     #Même principe que la méthode un_joueur()
        self.window2.show()
        self.a.mise_en_place_jetons()
        self.window2.actualiser_jetons()
        self.a.nbre_joueurs = 3
        self.a.difficulte_ia='Difficile'
        self.close()
        mixer.music.play()

    def ia_impossible(self):
        self.window2 = PlateauUi(self.p, self.a, 1)  # Même principe que la méthode un_joueur()
        self.window2.show()
        self.a.mise_en_place_jetons()
        self.window2.actualiser_jetons()
        self.a.nbre_joueurs = 3
        self.a.difficulte_ia = 'Impossible'
        self.close()
        mixer.music.play()

    def suppr(self):    #Méthode permettant de supprimer le fichier de sauvegarde
        try:
            os.remove('sauvegarde.txt')
        except Exception:
            pass

    def regles_jeu(self):
        ReglesUi().show()    #Affiche la fenêtre des règles du jeu
        self.close()         #Ferme la fenêtre du menu

    def recup_sauv(self):       #Cette méthode sert à relancer une partie sauvegardée
        fichier=True
        try:                                    #On essaye d'ouvrir le fichier de sauvegarde s'il existe
            f = open('sauvegarde.txt', 'r')
        except EnvironmentError:
            fichier=False
        if fichier==True:                                       #S'il existe
            self.p[self.p.c.pos[0], self.p.c.pos[1]] = 0        #On efface l'ancien caméléon sur le plateau
            f = open('sauvegarde.txt', 'r')                     #On ouvre le fichier de sauvegarde en mode lecture
            typ_interface = int(f.readline())                   #La première ligne est un entier correspondant au type de partie
            a = f.readline()                                    #La deuxième ligne correspond à la position du caméléon '30" pour (3,0)
            self.p.c.pos = (int(a[0]), int(a[1]))               #On replace le caméléon en conséquence
            self.p[self.p.c.pos[0], self.p.c.pos[1]] = 9        #Et on l'affiche sur la plateau
            plato = f.readline()                                #Composition du plateau
            compteur = 0
            for i in range(1, 6):
                for j in range(1, 6):
                    self.p[i, j] = plato[compteur]              #On reconstitue le plateau tel qu'il était
                    compteur += 1
            ia=f.readline()                                     #Difficulté de l'IA (Normale si c'est pas un mode avec ia)
            if typ_interface == 1:                              #Si c'est un mode solo
                self.window2 = PlateauUi(self.p, self.a, 1)     #Plateau avec un 1 en paramètre pour plateau 1 joueur
                self.window2.show()                             #On l'affiche
                self.window2.actualiser_jetons()                #On place les jetons sur le plateau
                self.a.nbre_joueurs = 1                         #Pour que window2.play() sache quel mode de jeu a été choisi
                self.close()                                    #Fermeture du menu de selection
            if typ_interface==3:                 #Pareil pour le mode avec ia
                self.window2 = PlateauUi(self.p, self.a, 1)
                self.window2.show()
                self.window2.actualiser_jetons()
                self.a.nbre_joueurs = 3
                self.a.difficulte_ia = ia
                self.close()
            if typ_interface==4:                    #Si c'est le mode 2 joueurs, des lignes supplémentaires on été écrites
                j1 = f.readline()                   #Le nom de joueur 1
                j2 = f.readline()                   #Le nom du joueur 2
                tour=int(f.readline())              #La variable tour_joueur pour savoir à qui c'est de jouer
                miz=int(f.readline())               #L'état de la mise
                deja_miz=eval(f.readline())         #Le booléen deja_mise. eval() permet de transformer 'True' en True de type booléen
                recet=eval(f.readline())            #Le booléen a_reset
                geton=int(f.readline())             #La variable jeton_mise
                pts1=int(f.readline())              #Le nombre de points du joueur 1
                pts2=int(f.readline())              #Le nombre de points du joueur 2
                topik=f.readline()                  #La phrase écrite en bas à droite
                self.a.liste_joueurs = [Joueur(j1[:-1]), Joueur(j2[:-1])]   #On crée les joueurs dans la liste de joueurs de l'arbitre de window2
                self.a.liste_joueurs[0].points=pts1                         #On leur redonne leurs points
                self.a.liste_joueurs[1].points=pts2
                self.window2 = PlateauUi(self.p, self.a,2)  #2 en paramètre pour charger le plateau de 2 joueurs

                self.window2.tour_joueur = tour             #On remet dans les bonnes variable les valeurs de ces variables
                self.window2.a.m.mise=miz
                self.window2.deja_mise=deja_miz
                self.window2.a_reset=recet
                self.window2.jeton_mise=geton
                self.window2.topic.setText(topik)
                self.window2.actu_sauvegarde()              #La méthode actu_sauvegarde est dans la classe PlateauUi et permet d'actualiser tous ces changements

                self.window2.show()                         #Affichage du plateau
                self.window2.actualiser_jetons()            #Affichage de ces derniers
                self.a.nbre_joueurs = 4                     #Nbre_joueurs=4 pour le mode 2 joueurs avec mise
                self.window2.repaint()                      #Actualisation de l'interface
                self.close()                                #Fermeture du menu
            mixer.music.play()

            self.window2.sauv=True      #Pour indiquer qu'on a chargé une partie sauvegardée
            f.close()   #Fermeture du fichier de sauvegarde que l'on a ouvert



class NamesUi(QtWidgets.QMainWindow):
    """Classe d'une fenêtre permettant de rentrer les noms des deux joueurs qui vont s'affronter dans le mode 2 joueurs"""
    def __init__(self,ui):
        QtWidgets.QMainWindow.__init__(self)
        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")  #Importation de la police "Jungle Roar". Bizarrement, il faut la mettre dans chaque classe... Et cela ne fonctionne pas en dehors d'une classe
        self.ui = uic.loadUi('names.ui', self)                          #On charge le bon fichier pour l'interface
        self.ui.bouton_jouer.clicked.connect(self.jouer)                #Pour le bouton jouer qui lancera la fenêtre avec le plateau
        self.fenetre=ui                                                 #self.fenetre -> fenêtre ouverte avant celle-ci, de type JeuUi

        self.n1.setFont(QtGui.QFont('Jungle Roar', pointSize=19))       #Certains textes seront écrits avec cette police pour faire joli
        self.n2.setFont(QtGui.QFont('Jungle Roar', pointSize=19))
        self.label_2.setFont(QtGui.QFont('Jungle Roar', pointSize=22))

        palette = QtGui.QPalette()   #Ces 4 lignes servent pour l'image d'arrière plan
        pixmap = QtGui.QPixmap("fond_names.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)


    def jouer(self):
        #Lorsqu'on clique sur le bouton jouer
        name1 = self.nom_joueur_1.toPlainText()     #On récupère les noms des joueurs
        name2 = self.nom_joueur_2.toPlainText()
        self.fenetre.a.liste_joueurs = [Joueur(name1), Joueur(name2)]        #On crée les joueurs dans la liste de joueurs de l'arbitre de window2
        self.fenetre.window2 = PlateauUi(self.fenetre.p, self.fenetre.a, 2)  #2 en paramètre pour charger le plateau de 2 joueurs
        self.fenetre.window2.show()                                          #Affichage du plateau
        self.fenetre.a.mise_en_place_jetons()                                #Mise en place des jetons
        self.fenetre.window2.actualiser_jetons()                             #Affichage de ces derniers
        self.fenetre.a.nbre_joueurs = 4                                      #Nbre_joueurs=4 pour le mode 2 joueurs avec mise
        self.close()                                                         #On ferme cette fenêtre
        mixer.music.play()                                                   #On lance la musique de fond



class PlateauUi(QtWidgets.QMainWindow):
    """Plateau de jeu"""
    def __init__(self,plat,arb,typ):
        QtWidgets.QMainWindow.__init__(self)
        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")    #On importe la police dans cette classe

        if typ==1:
            self.ui = uic.loadUi('plat.ui', self)                           #Si typ==1, alors on charge le plateau 1 joueur
            self.titre.setFont(QtGui.QFont('Jungle Roar', pointSize=28))
            self.ui.actionSauvegarder_et_quitter.triggered.connect(self.sauvegarder_j1) #Onglet du menu permettant de sauvegarder en mode 1 joueur
        if typ==2:
            self.ui = uic.loadUi('plat2.ui', self)                          #Sinon, on charge le plateau 2 joueurs qui est différent
            self.nom_j1.setFont(QtGui.QFont('Jungle Roar', pointSize=16))
            self.nom_j2.setFont(QtGui.QFont('Jungle Roar', pointSize=16))
            self.ui.actionSauvegarder_et_quitter.triggered.connect(self.sauvegarder_j2) #Onglet du menu permettant de sauvegarder en mode 2 joueurs

        self.ui.actionRetour_menu.triggered.connect(self.retour_menu)      #Si on clique sur l'onglet retour menu, la méthode retour_menu se lancera (devinez ce qu'elle va faire..)

        self.c_rouge = QtGui.QPixmap('insect_rouge.png')            #On charge les images des jetons
        self.c_vert = QtGui.QPixmap('insect_vert.png')
        self.c_jaune = QtGui.QPixmap('insect_jaune.png')
        self.c_bleu = QtGui.QPixmap('insect_bleu.png')
        self.c_gris = QtGui.QPixmap('insect_gris.png')
        self.c_mort = QtGui.QPixmap('insect_mort.png')

        self.c_cameleon = QtGui.QPixmap('camé.jpg')             #On charge les images du caméléon
        self.cameleon_haut= QtGui.QPixmap('cam_haut.png')
        self.cameleon_bas= QtGui.QPixmap('cam_bas.png')
        self.cameleon_gauche= QtGui.QPixmap('cam_gauche.png')
        self.cameleon_droite= QtGui.QPixmap('cam_droite.png')

        self.c_vide = QtGui.QPixmap('vide.jpg')     #On charge quelques images utiles
        self.c_rien = QtGui.QPixmap('rien.png')     #Un png sans fond
        self.jeton= QtGui.QPixmap('jeton_mise.png')
        self.haut= QtGui.QPixmap('branche_bas.png')        #Les contours du terrain avec des branches pour le délimiter
        self.bas= QtGui.QPixmap('branche_haut.png')
        self.droite= QtGui.QPixmap('branche_gauche.png')
        self.gauche= QtGui.QPixmap('branche_droite.png')

        palette = QtGui.QPalette()    #Ces 4 lignes servent pour l'image d'arrière plan (elles n'ont pas changé)
        pixmap = QtGui.QPixmap("arrierPlanBlanchi2.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)

        self.p = plat  #On récupère le plateau provenant de window en argument de la classe
        self.a = arb   #De même pour l'arbitre

        if typ == 2:   #Si c'est le plateau 2 joueurs
            self.nom_j1.setText(str(self.a.liste_joueurs[0].id))                    #On affiche le nom des joueurs au bon endroit
            self.nom_j2.setText(str(self.a.liste_joueurs[1].id))
            self.indic.setFont(QtGui.QFont('Jungle Roar', pointSize=18))            #Avec la jolie police
            self.indic.setText(str(self.a.liste_joueurs[0].id)+', a toi de jouer')  #On indique à qui c'est de jouer
            self.ui.mise_j1.clicked.connect(self.miser_j1)                          #On paramètre les boutons pour les mises
            self.ui.mise_j2.clicked.connect(self.miser_j2)
            self.score_j1.setFont(QtGui.QFont('Jungle Roar', pointSize=14))         #Et encore de la modification de police
            self.score_j2.setFont(QtGui.QFont('Jungle Roar', pointSize=14))
            self.affichage_mise.setFont(QtGui.QFont('Jungle Roar', pointSize=20))
            self.topic.setFont(QtGui.QFont('Jungle Roar', pointSize=16))

        self.choix_ui=42                 #On initalise le choix de ce que le joueur veut manger à un valeur bidon
        self.resultats=ScoresUi(self)    #Resultats sera l'interface qui affichera les résultats
        self.mise=MiseUi(self)           #Mise sera l'interface pour accepter ou refuser une augmentation de mise
        self.peut_jouer=True             #Permet de savoir si le joueur peut jouer (et qu'il clique pas partout pendant le tour de l'ordi pour tout faire planter)
        self.a_reset=False               #Permet de savoir si la méthode PlateauUi.reset() a été utilisée

        self.tour_joueur = 1  #Permet de savoir à qui c'est le tour
        self.deja_mise=False  #Permet de savoir si on a deja fait une surrenchère de mise ce tour
        self.jeton_mise=0     #Indique où est le jeton de mise (0 au milieur, 1 joueur 1, et 2 joueur 2)
        self.sauv=False       #Permet de savoir si on joue une partie sauvegardée


    def actu_sauvegarde(self):
        """Pour réinitialiser le plateau correctement lorsqu'on relance une partie
        que l'on a sauvegardée"""
        if self.tour_joueur % 2 == 1 or self.tour_joueur == 1:
            self.indic.setText(str(self.a.liste_joueurs[0].id) + ', a toi de jouer')  #On indique à qui c'est de jouer
        else:
            self.indic.setText(str(self.a.liste_joueurs[1].id) + ', a toi de jouer')
        self.affichage_mise.setText('Mise : ' + str(self.a.m))    #On affiche la nouvelle valeur de mise
        if self.jeton_mise==0:
            self.jeton_j1.setPixmap(self.c_rien)  #On supprime le jeton de mise sur le plateau
            self.jeton_j2.setPixmap(self.c_rien)
        elif self.jeton_mise==1:                  #Et on le remet où il faut
            self.jeton_j1.setPixmap(self.jeton.scaled(self.jeton_j1.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))  # On supprime le jeton de mise sur le plateau
            self.jeton_j2.setPixmap(self.c_rien)
        elif self.jeton_mise==2:
            self.jeton_j1.setPixmap(self.c_rien)
            self.jeton_j2.setPixmap(self.jeton.scaled(self.jeton_j2.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.score_j1.setText('Score : ' + str(self.a.liste_joueurs[0].points))     #On actualise les scores
        self.score_j2.setText('Score : ' + str(self.a.liste_joueurs[1].points))
        self.sauv=True  #On indique que joue une partie sauvegardée
        self.repaint()  #On actualise l'affichage


    def sauvegarder_j1(self):                   #Sauvegarde d'un plateau type 1
        f=open('sauvegarde.txt','w')            #On ouvre/crée le fichier de sauvegarde
        f.write(str(self.a.nbre_joueurs)+'\n')  #On écrit le type
        f.write(str(self.p.c.pos[0])+str(self.p.c.pos[1])+'\n')     #La position du caméléon
        for i in range(1,6):
            for j in range(1,6):
                f.write(str(int(self.p[i,j])))  #La composition du plateau de jeu
        f.write('\n'+self.a.difficulte_ia)      #La difficulté de l'ia ('normale' si mode 1 joueur)
        f.close()                               #On ferme le fichier
        self.retour_menu()                      #Et on appelle la méthode self.retour_menu() qui retourne au menu

    def sauvegarder_j2(self):                   #Pareil qu'au dessus
        f=open('sauvegarde.txt','w')
        f.write(str(self.a.nbre_joueurs)+'\n')
        f.write(str(self.p.c.pos[0])+str(self.p.c.pos[1])+'\n')
        for i in range(1,6):
            for j in range(1,6):
                f.write(str(int(self.p[i,j])))
        f.write('\n'+self.a.difficulte_ia+'\n')
        f.write(self.a.liste_joueurs[0].id)     #Mais on enregistre quelques données en plus comme les noms de joueurs
        f.write('\n')
        f.write(self.a.liste_joueurs[1].id)
        f.write('\n')
        f.write(str(self.tour_joueur))          #A qui c'est de jouer
        f.write('\n')
        f.write(str(self.a.m.mise))             #La mise
        f.write('\n')
        f.write(str(self.deja_mise))            #La variable booléenne deja_mise
        f.write('\n')
        f.write(str(self.a_reset))              #La variable booléenne a_reset
        f.write('\n')
        f.write(str(self.jeton_mise))           #L'entier jeton mise
        f.write('\n')
        f.write(str(self.a.liste_joueurs[0].points))    #Le nombre de points des joueurs
        f.write('\n')
        f.write(str(self.a.liste_joueurs[1].points))
        f.write('\n')
        f.write(str(self.topic.text()))         #La phrase écrite en bas à droite
        f.close()
        self.retour_menu()                      #Et on retourne au menu


    def retour_menu(self):      #Cette fonction permet de retourner à l'écran titre pendant la partie
        self.close()            #On ferme la fenêtre plateau
        JeuUi().show()          #Et on réouvre un nouveau menu


    def mousePressEvent(self, event):
        """Méthode qui se lance quand on clique et qui retourne des coordonées"""
        if event.button() == QtCore.Qt.LeftButton:
            self.info.setText(' ')              #On réinitialise ce champs de texte
            coords = [event.x(), event.y()]     #Coordonées du clic
            if self.peut_jouer==True:           #Si on peut jouer
                l = 215                         #Ordonnée du coin haut gauche du plateau
                L = 345                         #Abscisse du coin haut droit du plateau
                i = 0
                j = 0
                while coords[0] > L + j * 83:   #83 car 80 pixels de largeur de case + 3 pixels d'interstice entre 2 cases
                    j += 1
                while coords[1] > l + i * 83:
                    i += 1
                #i et j sont la ligne et la colonne de l'endroit cliqué
                if i==self.p.c.pos[0] and j==self.p.c.pos[1]:                       #Si on clique sur le caméléon
                    self.info.setText("Ne te mange pas toi même s'il te plaît")     #On affiche un petit message rigolo (dédicace à Marceau Michel)
                if (i >= 1 and i <= 5) and (j >= 1 and j <= 5) and self.peut_jouer == True:     #Si on clique sur une case dans le plateau et qu'on peut jouer
                    if self.p.c.pos[0] == i:            #Si on mange dans une ligne
                        self.choix_ui = self.p[i, j]    #Le choix est le type de jeton sur lequel on clique. C'est ici que le choix prend sa valeur !
                        if self.p[i, j] != 0:           #Et si c'est pas un jeton déjà mangé
                            self.play()                 #On peut jouer
                    elif self.p.c.pos[1] == j:          #Si on mange dans une colonne
                        self.choix_ui = self.p[i, j]    #La même
                        if self.p[i, j] != 0:
                            self.play()
                else:       #Si on clique en dehors du plateau
                    pass    #Bah on fait rien


    def play(self):
        """Méthode qui remplace la méthode Arbitre.jouer() permettant donc d'articuler le jeu.
        Elle appelle les méthode de la classe Arbitre de jeu.py qui ont été conçues pour faire fonctionner le jeu"""
        if self.a.nbre_joueurs==1:          #Si c'est le mode 1 joueur
            self.p.un_tour_joueur()         #On fait jouer en appelant Plateau.un_tour_joueur()
            self.actualiser_jetons()        #On actualise les jetons
            if self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:  #Si on se retrouve face à une ligne/colonne de 0
                self.resultats.show()                       #On affiche la fenêtre résultat parce que la partie est terminée
                if self.a.jetons_restants()==0:                                                                     #S'il reste 0 jetons
                    self.resultats.message.setText('Vous gagnez !')                                             #On affiche qu'il a gagné
                else:                                                                                               #Sinon
                    self.resultats.message.setText('Il vous reste ' + str(self.a.jetons_restants()) + ' jetons')    #On affiche le nombre de jetons restants

        elif self.a.nbre_joueurs==3:  #Mode avec IA
            self.p.un_tour_joueur()   #On fait jouer le joueur
            self.actualiser_jetons()  #On actualise le plateau
            self.repaint()            #On rafraîchit l'interface --> permet au joueur de jouer, attendre (avec l'actualisation puis le time.sleep), puis l'ordi joue
            if self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:      #Si on est face a une ligne de 0
                self.resultats.show()                           #On ouvre la fenêtre de résultat car on a gagné
                self.resultats.message.setText("Vous gagnez")   #Avec la message suivant
            else:                                       #Sinon, c'est au tour de l'ordi
                self.peut_jouer=False                   #Peut_jouer=False pour pas que le joueur clique partout et interfere avec le plateau quand l'ordi joue
                self.ui.info.setText("L'ordi joue")     #On précise que l'ordi joue
                self.repaint()                          #On actualise l'interface pour que le message s'affiche
                time.sleep(1)                           #On attends une seconde pour que le joueur se rende compte de ce qui a été joué
                if self.a.difficulte_ia == 'Facile':    #Si l'IA est facile
                    self.p.un_tour_ia_facile()          #On appelle cette fonction
                if self.a.difficulte_ia == 'Normale':   #Si l'IA est normale
                    self.p.un_tour_ia_normale()         #On appelle celle la
                    if self.p.coup_gagnant == False:    #Si on a pas trouvé de choix gagnant Arbitre.coup_gagnant est faux
                        self.p.un_tour_ia_facile()      #Donc on joue au hasard en appelant l'IA dacile
                if self.a.difficulte_ia == 'Difficile': #Si l'IA est difficile
                    self.p.un_tour_ia_difficile()       #On appelle cette fonction
                if self.a.difficulte_ia == 'Impossible':#Si l'IA est très difficile
                    self.p.un_tour_ia_impossible()      #On appelle cette fonction
                self.actualiser_jetons()                #On actualise le plateau
                if self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:      #Si on se retrouve face a une ligne/colonne de 0
                    self.resultats.show()                           #On affiche la fenêtre résultats
                    self.resultats.message.setText("L'ordi gagne")  #Et on dit que l'ordi gagne
                self.peut_jouer = True                              #Le joueur peut rejouer

        elif self.a.nbre_joueurs==4:         #Mode deux joueurs avec mise
            self.a_reset=False               #a_reset initialisé à False
            if self.tour_joueur%2==1 or self.tour_joueur==1:  #Si c'est au tour du joueur 1
                self.p.un_tour_joueur_mise(self.a)            #On appelle la fonction Plateau.un_tout_joueur_mise pour le tour du J1
                self.actualiser_jetons()                      #On actualise le plateau
                self.indic.setText(str(self.a.liste_joueurs[1].id)+', a toi de jouer')                                  #On indique que c'est au joueur 2 de joueur
                if self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0] and (self.a.liste_joueurs[0].points+self.a.m.mise)>=5:    #Si le joueur 2 perd la manche et que le joueur 1 a plus de 5 points
                    self.a.liste_joueurs[0].points += self.a.m.mise                                                     #On augmente les points du joueur 1
                    self.score_j1.setText('Score : ' + str(self.a.liste_joueurs[0].points))                             #On actualise son score
                    if self.a.m.mise>1:
                        self.topic.setText(str(self.a.liste_joueurs[0].id) + ' a gagne ' + str(self.a.m.mise) + ' points') #On précise que le joueur 1 a gagné tant de points
                    else:
                        self.topic.setText(str(self.a.liste_joueurs[0].id) + ' a gagne ' + str(self.a.m.mise) + ' point')  #On précise que le joueur 1 a gagné tant de points
                    self.resultats.show()                                                                                  #On affiche la fenêtre de résultats
                    self.resultats.message.setText(str(self.a.liste_joueurs[0].id)+" gagne avec : "+str(self.a.liste_joueurs[0].points)+" points") #On indique que le joueur 1 a remporté la partie
                elif self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:                                                                                   #Si le joueur 2 perd la manche mais le joueur n'a pas les 5 points pour gagner la partie
                    self.peut_jouer=False
                    self.repaint()
                    time.sleep(0.5)
                    self.peut_jouer=True
                    self.a.liste_joueurs[0].points+=self.a.m.mise                                                                                  #On augmente les points du joueur 1
                    self.score_j1.setText('Score : '+str(self.a.liste_joueurs[0].points)) #On actualise son score
                    if self.a.m.mise>1:
                        self.topic.setText(str(self.a.liste_joueurs[0].id)+' a gagne '+str(self.a.m.mise)+' points')    #On affiche combien de points il a gagné
                    else:
                        self.topic.setText(str(self.a.liste_joueurs[0].id)+' a gagne '+str(self.a.m.mise)+' point')    #On affiche combien de points il a gagné
                    self.reset()       #On reset le plateau

            if self.tour_joueur%2==0:  #Strictement identique que le if au dessus mais avec le joueur 2
                self.p.un_tour_joueur_mise(self.a)
                self.actualiser_jetons()
                self.indic.setText(str(self.a.liste_joueurs[0].id)+', a toi de jouer')
                if self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0] and (self.a.liste_joueurs[1].points+self.a.m.mise)>=5:
                    self.a.liste_joueurs[1].points += self.a.m.mise
                    self.score_j2.setText('Score : ' + str(self.a.liste_joueurs[1].points))
                    if self.a.m.mise>1:
                        self.topic.setText(str(self.a.liste_joueurs[1].id)+' a gagne '+str(self.a.m.mise)+' points')
                    else:
                        self.topic.setText(str(self.a.liste_joueurs[1].id)+' a gagne '+str(self.a.m.mise)+' point')
                    self.resultats.show()
                    self.resultats.message.setText(str(self.a.liste_joueurs[1].id)+" gagne avec : "+str(self.a.liste_joueurs[1].points)+" points")
                elif self.a.p.menu == [0.0, 0.0, 0.0, 0.0, 0.0]:
                    self.peut_jouer=False
                    self.repaint()
                    time.sleep(0.5)
                    self.peut_jouer=True
                    self.a.liste_joueurs[1].points+=self.a.m.mise
                    self.score_j2.setText('Score : '+str(self.a.liste_joueurs[1].points))
                    if self.a.m.mise>1:
                        self.topic.setText(str(self.a.liste_joueurs[1].id)+' a gagne '+str(self.a.m.mise)+' points')
                    else:
                        self.topic.setText(str(self.a.liste_joueurs[1].id)+' a gagne '+str(self.a.m.mise)+' point')
                    self.reset()
            if self.a_reset==False:     #Si ça n'a pas été reset, on augmente tour_joueur pour qu'au prochain apppel, c'est le joueur suivant qui joue
                self.tour_joueur += 1   #Parce que dans le reset, on remet le numéro de joueur à 1
            self.p.annulation=False     #On reinitialise : annulation,
            self.p.rejouer=False        #Rejouer,
            self.deja_mise=False        #Et deja mise
            self.affichage_mise.setText('Mise : ' + str(self.a.m)) #Et on met à jour la mise


    def reset(self):
        self.a_reset=True                           #On indique que le plateau a été réinitialisé
        self.a.m.mise=1                             #On remet la mise à 1
        self.jeton_mise=0                           #On remet le jeton de mise au milieu
        self.jeton_j1.setPixmap(self.c_rien)        #On supprime le jeton de mise sur le plateau
        self.jeton_j2.setPixmap(self.c_rien)
        self.indic.setText(str(self.a.liste_joueurs[0].id) + ' a toi de jouer')  #On le précise sur l'interface
        self.a.mise_en_place_jetons()                               #On remet des jetons aléatoirement
        self.a.p.calcul_menu(self.a.c.pos[0], self.a.c.pos[1])      #On recalcule le menu
        self.actualiser_jetons()                                    #On actualise le plateau
        self.tour_joueur=1                                          #On redemande au joueur 1 de jouer
        self.repaint()                                              #Et on actualise l'interface


    def miser_j1(self):
        if (self.tour_joueur==1 or self.tour_joueur%2==1) and self.a.m.mise<5 and self.deja_mise==False and (self.jeton_mise==0 or self.jeton_mise==2): #Si c'est le tour du joueur 1 et qu'il a pas déja misé
            self.deja_mise=True                        #On dit qu'il a misé
            self.jeton_mise=1                          #Le joueur 1 a le jeton de mise et ne peut plus surrencherir
            self.jeton_j1.setPixmap(self.jeton.scaled(self.jeton_j1.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))        #On place le jeton sur l'emplacement en dessous du score du Joueur 1
            self.jeton_j2.setPixmap(self.c_rien)       #Rien pour le joueur 2
            self.mise.acc.setText(str(self.a.liste_joueurs[1].id) + " acceptes-tu l'augmentation de mise ?")  #Texte pour la phrase sur la fenêtre de mise
            self.mise.show()                           #On affiche la fenêtre des mises


    def miser_j2(self): #Pareil mais pour le joueur 2
        if self.tour_joueur%2==0 and self.a.m.mise<5 and self.deja_mise==False and (self.jeton_mise==1 or self.jeton_mise==0):
            self.deja_mise=True
            self.jeton_mise=2
            self.jeton_j2.setPixmap(self.jeton.scaled(self.jeton_j2.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
            self.jeton_j1.setPixmap(self.c_rien)
            self.mise.acc.setText(str(self.a.liste_joueurs[0].id) + " acceptes-tu l'augmentation de mise ?")
            self.mise.show()


    def couleur(self, i, j):
        """Cette méthode permet de retourner la couleur en fonction du numéro présent sur le plateau"""
        if self.p[i, j] == 1:  #Les différentes couleurs
            return self.c_rouge
        if self.p[i, j] == 2:
            return self.c_vert
        if self.p[i, j] == 3:
            return self.c_jaune
        if self.p[i, j] == 4:
            return self.c_bleu
        if self.p[i, j] == 5:
            return self.c_gris

        if self.p[i, j] == 9 and i==0:  #Le caméléon en fonction de s'il est en haut, en bas, à gauche ou à droite du plateau
            return self.cameleon_haut
        if self.p[i, j] == 9 and i==6:
            return self.cameleon_bas
        if self.p[i, j] == 9 and j==0:
            return self.cameleon_gauche
        if self.p[i, j] == 9 and j==6:
            return self.cameleon_droite

        if self.p[i,j]==-1:       #Les coins du plateau
            return self.c_rien

        if self.p[i,j] ==0 and i!=0 and i!=6 and j!=0 and j!=6:  #Les cases vides de l'intérieur du plateau (jeton retourné)
            return self.c_mort
        if self.p[i,j] ==0 and i==0:      #Les contours du plateau
            return self.bas
        if self.p[i, j] == 0 and i==6:
            return self.haut
        if self.p[i, j] == 0 and j==0:
            return self.droite
        if self.p[i, j] == 0 and j==6:
            return self.gauche


    def type(self, num, manges):
        """Sert à retourner ce que l'ordi à mangé. Utilisé dans les méthode Plateau.un_tour_ia_facile/normale/difficile"""
        if num == 1 and manges == 1:
            return 'rouge'
        if num == 2 and manges == 1:
            return 'vert'
        if num == 3 and manges == 1:
            return 'jaune'
        if num == 4 and manges == 1:
            return 'bleu'
        if num == 5:
            return 'gris'
        if num == 1 and manges != 1:
            return 'rouges'
        if num == 2 and manges != 1:
            return 'verts'
        if num == 3 and manges != 1:
            return 'jaunes'
        if num == 4 and manges != 1:
            return 'bleus'


    def actualiser_jetons(self):
        """Charge les images des jetons sur le plateau"""
        self.label_1.setPixmap(self.couleur(0,0).scaled(self.label_1.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))  #Appelle la méthode PlateauUi.couleur() au dessus pour savoir quel fichier charger
        self.label_2.setPixmap(self.couleur(0, 1).scaled(self.label_2.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation)) #Le.scaled permet de redimensionner l'image à la taille du Qlabel
        self.label_3.setPixmap(self.couleur(0, 2).scaled(self.label_3.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_4.setPixmap(self.couleur(0, 3).scaled(self.label_4.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_5.setPixmap(self.couleur(0, 4).scaled(self.label_5.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_6.setPixmap(self.couleur(0, 5).scaled(self.label_6.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_7.setPixmap(self.couleur(0, 6).scaled(self.label_7.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_8.setPixmap(self.couleur(1, 0).scaled(self.label_8.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_9.setPixmap(self.couleur(1, 1).scaled(self.label_9.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_10.setPixmap(self.couleur(1, 2).scaled(self.label_10.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_11.setPixmap(self.couleur(1, 3).scaled(self.label_11.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_12.setPixmap(self.couleur(1, 4).scaled(self.label_12.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_13.setPixmap(self.couleur(1, 5).scaled(self.label_13.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_14.setPixmap(self.couleur(1, 6).scaled(self.label_14.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_15.setPixmap(self.couleur(2, 0).scaled(self.label_15.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_16.setPixmap(self.couleur(2, 1).scaled(self.label_16.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_17.setPixmap(self.couleur(2, 2).scaled(self.label_17.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_18.setPixmap(self.couleur(2, 3).scaled(self.label_18.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_19.setPixmap(self.couleur(2, 4).scaled(self.label_19.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_20.setPixmap(self.couleur(2, 5).scaled(self.label_20.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_21.setPixmap(self.couleur(2, 6).scaled(self.label_21.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_22.setPixmap(self.couleur(3, 0).scaled(self.label_22.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_23.setPixmap(self.couleur(3, 1).scaled(self.label_23.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_24.setPixmap(self.couleur(3, 2).scaled(self.label_24.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_25.setPixmap(self.couleur(3, 3).scaled(self.label_25.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_26.setPixmap(self.couleur(3, 4).scaled(self.label_26.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_27.setPixmap(self.couleur(3, 5).scaled(self.label_27.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_28.setPixmap(self.couleur(3, 6).scaled(self.label_28.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_29.setPixmap(self.couleur(4, 0).scaled(self.label_29.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_30.setPixmap(self.couleur(4, 1).scaled(self.label_30.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_31.setPixmap(self.couleur(4, 2).scaled(self.label_31.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_32.setPixmap(self.couleur(4, 3).scaled(self.label_32.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_33.setPixmap(self.couleur(4, 4).scaled(self.label_33.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_34.setPixmap(self.couleur(4, 5).scaled(self.label_34.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_35.setPixmap(self.couleur(4, 6).scaled(self.label_35.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_36.setPixmap(self.couleur(5, 0).scaled(self.label_36.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_37.setPixmap(self.couleur(5, 1).scaled(self.label_37.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_38.setPixmap(self.couleur(5, 2).scaled(self.label_38.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_39.setPixmap(self.couleur(5, 3).scaled(self.label_39.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_40.setPixmap(self.couleur(5, 4).scaled(self.label_40.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_41.setPixmap(self.couleur(5, 5).scaled(self.label_41.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_42.setPixmap(self.couleur(5, 6).scaled(self.label_42.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_43.setPixmap(self.couleur(6, 0).scaled(self.label_43.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_44.setPixmap(self.couleur(6, 1).scaled(self.label_44.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_45.setPixmap(self.couleur(6, 2).scaled(self.label_45.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_46.setPixmap(self.couleur(6, 3).scaled(self.label_46.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_47.setPixmap(self.couleur(6, 4).scaled(self.label_47.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_48.setPixmap(self.couleur(6, 5).scaled(self.label_48.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))
        self.label_49.setPixmap(self.couleur(6, 6).scaled(self.label_49.size(),QtCore.Qt.IgnoreAspectRatio,QtCore.Qt.SmoothTransformation))




class MiseUi(QtWidgets.QMainWindow):
    """Interface pour l'augmentation de mise
    On rappelle que lorsqu'on créé un arbitre, une mise a.m est créée"""
    def __init__(self,ui):
        QtWidgets.QMainWindow.__init__(self)
        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")  #On importe la police pour cette classe
        self.ui = uic.loadUi('mises.ui', self)                          #On charge le bon fichier
        self.ui.accept.clicked.connect(self.accepter)                   #Bouton accepter
        self.ui.refuse.clicked.connect(self.refuser)                    #Bouton refuser
        self.mere=ui                                                    #Interface de type PlateauUi

        palette = QtGui.QPalette()  #Ces 4 lignes servent pour l'image d'arrière plan
        pixmap = QtGui.QPixmap("fond_mise.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)

        self.acc.setFont(QtGui.QFont('Jungle Roar', pointSize=10))

    def accepter(self):                                                     #Si le second joueur accepte la surrenchère de mise
        self.mere.a.m.incrementer_mise()                                    #On augmente la mise de 1
        self.mere.affichage_mise.setText('Mise : ' + str(self.mere.a.m))    #On affiche la nouvelle valeur de mise
        self.repaint()                                                      #On actualise l'interface
        self.rejouer=True                                                   #On demande au joueur qui a proposé l'enchère de rejouer
        self.close()                                                        #On ferme cette fenêtre


    def refuser(self):          #Si le second joueur refuse
        self.annulation=True    #Annulation devient True
        if self.mere.tour_joueur==1 or self.mere.tour_joueur%2==1:    #Si c'est le tour du joueur 1
            self.mere.a.liste_joueurs[0].points+=self.mere.a.m.mise   #Le joueur 2 refuse du coup le joueur 1 gagne les points de la mise
            if self.mere.a.m.mise >1:                                 #On affiche le nombre de points gagnés
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[0].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' points')
            else:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[0].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' point')
        if self.mere.tour_joueur%2==0:                                #Même chose pour le joueur 2
            self.mere.a.liste_joueurs[1].points+=self.mere.a.m.mise
            if self.mere.a.m.mise >1:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[1].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' points')
            else:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[1].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' point')

        if (self.mere.tour_joueur==1 or self.mere.tour_joueur%2==1) and (self.mere.a.liste_joueurs[0].points) >= 5:  #Dans le cas où le refus entraine la victoire du joueur 1
            self.mere.score_j1.setText('Score : ' + str(self.mere.a.liste_joueurs[0].points))                        #On actualise les scores
            if self.mere.a.m.mise >1:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[0].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' points')
            else:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[0].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' point')
            self.mere.resultats.show()                                                                                                                              #On affiche la fenêtre réultat
            self.mere.resultats.message.setText(str(self.mere.a.liste_joueurs[0].id) + " gagne avec : " + str(self.mere.a.liste_joueurs[0].points) + " points")     #Et son nombre de points
        elif (self.mere.tour_joueur%2==0)  and (self.mere.a.liste_joueurs[1].points) >= 5:          #Pareil si le refus entraîne la victoire du joueur 2
            self.mere.score_j2.setText('Score : ' + str(self.mere.a.liste_joueurs[1].points))
            if self.mere.a.m.mise >1:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[1].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' points')
            else:
                self.mere.topic.setText(str(self.mere.a.liste_joueurs[1].id) + ' a gagne ' + str(self.mere.a.m.mise) + ' point')
            self.mere.resultats.show()
            self.mere.resultats.message.setText(str(self.mere.a.liste_joueurs[1].id) + " gagne avec : " + str(self.mere.a.liste_joueurs[1].points) + " points")
        else:                                                                                       #Si le refus n'entraîne pas une victoire
            self.mere.reset()                                                                       #Manche suivante, on reset le plateau
            self.mere.score_j1.setText('Score : ' + str(self.mere.a.liste_joueurs[0].points))       #On actualise les scores
            self.mere.score_j2.setText('Score : ' + str(self.mere.a.liste_joueurs[1].points))
            self.mere.affichage_mise.setText('Mise : 1')                                            #La mise est de nouveau à 1
        self.mere.deja_mise = False                                                                 #Deja_mise redevient faux
        self.repaint()                                                                              #Actualisation de l'interface
        self.close()                                                                                #Fermeture de la fenêtre de mise



class ScoresUi(QtWidgets.QMainWindow):
    def __init__(self,ui):
        QtWidgets.QMainWindow.__init__(self)
        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")  #On importe la police
        self.ui = uic.loadUi('scores.ui', self)                         #On charge le bon fichier d'interface
        self.ui.rejouer.clicked.connect(self.menu)                      #Bouton rejouer
        self.ui.quit.clicked.connect(self.quitter)                      #Bouton quitter
        self.message.setText(' ')                                       #Le message est initialisé à rien
        self.message.setFont(QtGui.QFont('Jungle Roar', pointSize=16))  #Avec la nouvelle police
        self.fermer=ui                                                  #Fermer est l'interface de type PlateauUi() qu'il faudra fermer en appuyanty sur quitter ou rejouer

        palette = QtGui.QPalette()    #Ces 4 lignes servent pour l'image d'arrière plan
        pixmap = QtGui.QPixmap("fond_scores.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)


    def menu(self):             #Si on clique sur rejouer
        self.close()            #Cette fenêtre se ferme
        JeuUi().show()          #Un nouveau menu se rouvre
        self.fermer.close()     #Le plateau se ferme
        if self.fermer.sauv==True:  #Si c'est une partie sauvegardée qu'on fini, alors on la supprime
            try:
                os.remove('sauvegarde.txt')
            except Exception:
                pass
        mixer.music.rewind()    #On remet la musique de fond au début


    def quitter(self):          #Si on clique sur fermer
        self.close()            #On ferme cette fenêtre
        self.fermer.close()     #Et on ferme le plateau
        if self.fermer.sauv==True:  #Si c'est une partie sauvegardée qu'on fini, alors on la supprime
            try:
                os.remove('sauvegarde.txt')
            except Exception:
                pass
        mixer.music.rewind()    #On remet la musique de fond au début



class ReglesUi(QtWidgets.QMainWindow):
    """Permet d'afficher l'image avec les règles du jeu"""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        QtGui.QFontDatabase.addApplicationFont("Jungle Roar Bold.ttf")    #On importe la nouvelle police
        self.ui = uic.loadUi('regles.ui', self)                           #On charge le bon fichier d'interface
        self.ui.actionRetour_au_menu.triggered.connect(self.retour_menu)  #Pour retourner au menu

        palette = QtGui.QPalette()  #Ces 4 lignes servent pour l'image d'arrière plan
        pixmap = QtGui.QPixmap("fond_regles.jpg")
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)


    def retour_menu(self):      #Pour retourner au menu
        self.close()            #On ferme la fenêtre des règles
        JeuUi().show()          #Et on ouvre un nouveau menu



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = JeuUi()    #On crée un menu que l'on appelle window
    window.show()       #On l'ouvre
    sys.exit(app.exec_())