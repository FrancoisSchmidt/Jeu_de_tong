from jeu import *
from ui import *
import sys                                          #Pour l'interface
from PyQt5 import QtGui, QtCore, QtWidgets, uic     #Importations d'éléments de PyQt5
from pygame import mixer
import numpy as np
import unittest


#classes : Entite, Joueur(entite), Ia(entite), Plateau(nd.array), Cameleon, Nourriture, Arbitre, Mise


class TestJeu(unittest.TestCase):
    """Tests sur le plateau de jeu"""

    def setUp(self):
        app = QtWidgets.QApplication(sys.argv)  #Obligatoire sinon on ne peut créer aucune classe d'interface
        self.c = Cameleon()                                                     #Création d'un caméléon
        self.p = Plateau(7, 7, self.c, PlateauUi(self,Arbitre(self,self.c),1))  #Création d'un plateau
        self.a = Arbitre(self.p,self.c)                                         #Création d'un arbitre
        self.a.mise_en_place_jetons()                                           #On met en place aléatoirement les jetons sur le plateau
        self.ia = Ia()                                                          #On crée une IA
        self.m = Mise()                                                         #Et une mise


    def testInit_plateau(self):                             #Tests concernants le plateau
        self.assertEqual(self.c.pos,(3,0))                  #On regarde si le caméléon est au bon endroite au départ
        self.assertEqual(self.p[0, 0],-1)                   #On regarde si les coins sont bien à -1
        self.assertEqual(self.p[0, -1], -1)
        self.assertEqual(self.p[-1, 0], -1)
        self.assertEqual(self.p[-1, -1], -1)
        self.assertEqual(self.p[3, 0],9)                    #Et si le caméléon est bien représenté par un 9
        self.assertEqual(self.a.jetons_restants(),25)       #On regarde s'il reste bien 25 jetons (aucun jeton mangé)
        self.p.calcul_menu(self.c.pos[0],self.c.pos[1])     #On actualise le menu
        self.assertTrue(type(self.p.menu),'list')                   #Et on regarde si c'est bien une liste de 5 éléments
        self.assertEqual(len(self.p.menu),5)

    def testBouger(self):
        self.c.bouger(2, self.p)            #On fait bouger le caméléon de 2 cases
        self.assertEqual(self.p[3, 0],0)    #Et on vérifie qu'il l'a bien fait
        self.assertEqual(self.p[1, 0],9)

    def testProjection(self):               #Test de la méthode Projection permettant de retourner une position théorique du caméléon
        self.assertEqual(self.c.projection(self.c.pos[0],self.c.pos[1],2),(1,0))


    def testCalcul_menu(self):              #Test de la méthode calcul_menu
        self.p.calcul_menu(3, 0)            #On actualise le menu
        self.assertTrue((np.array(self.p[3,1:6]) == np.array(self.p.menu)).all())   #Et on vérifie que chacun des termes sont égaux
        self.p.calcul_menu(0, 2)            #Encore un pour la route
        self.assertTrue((np.array(self.p[1:6,2]) == np.array(self.p.menu)).all())

    def testInit_ia(self):                      #Création d'une IA
        self.assertTrue(self.ia.id == 'Ordi')   #Dont le nom sera Ordi

    def testInit_mise(self):                    #Test de création d'une mise
        self.assertEqual(self.m.mise, 1)        #Pour savoir si elle est initialisée à 1

    def test_incrementer_mise(self):            #Test de l'incrémentation de mise
        self.m.incrementer_mise()               #On l'augmente
        self.assertEqual(self.m.mise, 2)        #Elle doit passer à 2
        for i in range (6):                     #On l'augmente de 6
            self.m.incrementer_mise()
        self.assertEqual(self.m.mise, 5)        #Le plafond est à 5



if __name__ == "main":
    unittest.main()
