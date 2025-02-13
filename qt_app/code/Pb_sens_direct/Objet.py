# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:59:46 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""
import time
from numpy import meshgrid, sqrt, linspace, savetxt
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
def create_and_display_object(progress_callback):
    progress_callback.emit(0)
    print("Début de la simulation de l'objet")  
    start_time = time.process_time()  # début mesure temps d'éxecusion

    # Nb pixel Objet (échantillonnage objet)
    NbHO = 1280
    NbVO = 800
    # Rayon sphere mm
    R = 360
    # Recul sphere mm
    a = 300
    progress_callback.emit(25)

    # Coordonnées matricielles des pts M de l'objet
    [X, Y] = meshgrid(linspace(-600, 600, NbHO), linspace(-375, 375, NbVO))

    # Affixe de l'objet (mm)
    Za2 = R**2 - X**2 - Y**2
    Z = sqrt((Za2 > a**2) * Za2) - a + a * (Za2 <= a**2)
    print("Calcul de la hauteur de chaque point")  

    # Enregistrement des coordonnées matricelles objet
    progress_callback.emit(50)
    print("Enregistrement des coordonnées matricelles dans les fichiers X.txt, Y.txt et Z.txt")  
    savetxt('X.txt', X, fmt='%-7.6f')
    savetxt('Y.txt', Y, fmt='%-7.6f')
    savetxt('Z.txt', Z, fmt='%-7.6f')
    progress_callback.emit(75)
    print("Creation de l'image de l'objet")  

    # Affichage de l'objet
    z_min, z_max = 0, abs(Z).max()
    plt.figure()
    plt.pcolor(X, Y, Z, cmap='gray', vmin=z_min, vmax=z_max)
    plt.title('Z (mm) - Objet bouclier simulé')
    # set the limits of the plot to the limits of the data
    plt.axis([X.min(), X.max(), Y.min(), Y.max()])
    plt.colorbar()
    plt.savefig("Objet1.png")
    #plt.show()
    progress_callback.emit(100)
    print("Fin de la simulation de l'objet")  

    print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion


"""
class fesse:
    def __init__(self):
        print("fesse")
        pass

    def emit(self,value):
        print("fesse")
        pass


create_and_display_object(fesse())"""