# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 19:06:20 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""

#**************************************************************************
#***********  Mire damier dans repere emetteur ***************************
#**************************************************************************
#***************************** Python **********************************

import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import zeros, sin, pi, linspace, savetxt, uint8

# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
from skimage import io

#Nombre de carreaux 
p = 8 #horizontaux
q = 8 #verticaux


#----- Paramètre emetteur LCD ---------------
#Taille LCD en pixel 
NbHE = 1280 #horizontal
NbVE = 800  #vertical
#Coordonnées matricielles des pts mE du LCD
xx = linspace(0, NbHE - 1, NbHE)
yy = linspace(0, NbVE - 1, NbVE)

    
#Coordonnées matricielles des pts mE du LCD
vE,uE = np.meshgrid(xx,yy)
savetxt('uE.txt', uE, fmt='%-7.7f')
savetxt('vE.txt', vE, fmt='%-7.7f')


#Création de la mire damier
#Intensite mire damier objet
B = zeros((NbVE,NbHE), dtype = float)
IdE = 1*((sin(uE*q*pi/NbVE)*sin(vE*p*pi/NbHE)) < 0)

#Enregistrement
A = "Mire_damier.bmp"
r = 255*IdE   
g = 0*IdE
b = 0*IdE

B = np.dstack((r,g,b))
B = uint8(B)
io.imsave(A,B) 

# Affichage
#plt.figure()
#plt.pcolor(vE,uE,IdE, cmap='gray') #
#plt.title('Mire damier IdE(mE)')
#plt.xlabel('vE pixels')
#plt.ylabel('uE pixels')
print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion