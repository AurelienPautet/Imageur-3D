# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:59:46 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""
import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
#import numpy as np
from numpy import meshgrid, sqrt, linspace, savetxt
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt


#************************************************************************
#*********** Création de l'objet bouclier dans repère Objet (O,X,Y,Z) ***
#************************************************************************
#Nb pixel Objet (échantillonnage objet)
NbHO = 1280
NbVO = 800
#Rayon sphere mm
R = 360;
#Recul sphere mm
a = 300;

#Coordonnées matricielles des pts M de l'objet
[X,Y] = meshgrid(linspace(-600,600,NbHO),linspace(-375,375,NbVO));

#Affixe de l'objet (mm)
Za2 = R**2 - X**2 - Y**2;
Z = sqrt((Za2>a**2)*Za2) - a + a*(Za2<=a**2);
#Enregistrement des coordonnées matricelles objet
savetxt('X.txt', X, fmt='%-7.6f')   
savetxt('Y.txt', Y, fmt='%-7.6f')
savetxt('Z.txt', Z, fmt='%-7.6f')  


#************************************************************************
#************************ Affichage de l'objet  *************************
#************************************************************************

z_min, z_max = 0, abs(Z).max()
plt.figure();
plt.pcolor(X,Y,Z, cmap='gray', vmin=z_min, vmax=z_max)
plt.title('Z (mm) - Objet bouclier simulé')
# set the limits of the plot to the limits of the data
plt.axis([X.min(), X.max(), Y.min(), Y.max()])
plt.colorbar()
plt.savefig("Objet1.png")
print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion