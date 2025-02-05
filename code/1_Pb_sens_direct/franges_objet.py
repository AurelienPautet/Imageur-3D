# -*- coding: utf-8 -*-
"""
Created onTue Mar 20 09:59:46 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""
#**************************************************************************
#*********** Images projetée sur l'objet *********************************
#**************************************************************************
# 
import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, size, sin, cos, pi, array, concatenate
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
#On importe ndimage pour pouvoir utiliser la fonction d'interpolation map_coordinates
from scipy.ndimage import map_coordinates
from scipy.interpolate import griddata
from skimage import io

#Chargement de l'objet simulé dans repère Objet (O,X,Y,Z)
X = loadtxt('X.txt')
Y = loadtxt('Y.txt')
Z = loadtxt('Z.txt')

# X = loadtxt('X_toiture.txt')
# Y = loadtxt('Y_toiture.txt')
# Z = loadtxt('Z_toiture.txt')

# X = loadtxt('X_plan.txt')
# Y = loadtxt('Y_plan.txt')
# Z = loadtxt('Z_plan.txt')

#Chargement nombre de trame
N = loadtxt("N.txt")
N = int(N)
#Chargement coordonnées LCD
uE = loadtxt('uE.txt')
vE = loadtxt('vE.txt')

#taille LCD
NbVE = size(uE[:,0])
NbHE = size(vE[0,:]) 

#---------- Matrice de projection perspective émetteur ME ------------
#Angles du dispositif
alpha_d = 55 #[°]
beta_d = 85 #[°]
alpha = alpha_d*pi/180 #[rad]
beta = beta_d*pi/180 #[rad]

np.savetxt('angles.txt', (alpha_d, beta_d), fmt='%1.16e')

phiE = -pi/2 
thetaE = pi/2 + (alpha + beta)/2 
psiE = 0. 

#Distances ou composantes translation du dispositif (mm)
L = 950. # mm
t1E = 0. 
t2E = 0. 
t3E = sin(beta)/sin(alpha + beta)*L 
#Vecteur translation TE
TE = array([[t1E], [t2E], [t3E]])

#Matrice de rotation RE
r11E = cos(phiE)*cos(thetaE) 
r21E = sin(phiE)*cos(thetaE) 
r31E = -sin(thetaE)
 
r12E = cos(phiE)*sin(thetaE)*sin(psiE) - sin(phiE)*cos(psiE) 
r22E = sin(phiE)*sin(thetaE)*sin(psiE) + cos(phiE)*cos(psiE) 
r32E = cos(thetaE)*sin(psiE) 

r13E = cos(phiE)*sin(thetaE)*cos(psiE) + sin(phiE)*sin(psiE) 
r23E = sin(phiE)*sin(thetaE)*cos(psiE) - cos(phiE)*sin(psiE) 
r33E = cos(thetaE)*cos(psiE) 

RE = array([[r11E, r12E, r13E], [r21E, r22E, r23E], [r31E, r32E, r33E]])

#Facteurs d'échelle du LCD (mm-1)
kuE = 100.723 # [mm-1]
kvE = 100.723 # [mm-1]

#Focale emetteur (mm)
fE = 20.28 
# fE = 16.9

#Paramètres intrinsèques
alphauE = -kuE*fE # []
alphavE = kvE*fE # []

#Centre axe optique sur LCD
u0E = NbVE/2 - 0.5  
v0E = NbHE/2 - 0.5 

#Matrice ICE
ICE = array([[alphauE, 0, u0E, 0], [0, alphavE, v0E, 0], [0, 0, 1, 0]])

#Matrice AE
RETE = concatenate((RE,TE),axis=1)
intermed = array([(0, 0, 0, 1)])
AE = concatenate((RETE, intermed),axis=0)

#Matrice ME
ME = ICE.dot(AE)
np.savetxt('ME.txt', ME, fmt='%-7.9f')


#------ Calcul des images de franges objet pour les N trames ------
for k in range (N):
    #------ Chargement des images d'intensité IE du LCD ---
    Nomtrame='Trame' + str(k+1) + '.bmp'
    ima = io.imread(Nomtrame)

    #Projection émetteur
    sEuE1 = ME[0,0]*X + ME[0,1]*Y + ME[0,2]*Z + ME[0,3]
    # sEuE1 = array(sEuE1)
    
    sEvE1 = ME[1,0]*X + ME[1,1]*Y + ME[1,2]*Z + ME[1,3]
    # sEvE1 = array(sEvE1)
    
    sE = ME[2,0]*X + ME[2,1]*Y + ME[2,2]*Z + ME[2,3] 
    # sE = array(sE)
    
    uE1 = sEuE1/sE 
    vE1 = sEvE1/sE 
    
    #Détermination de l'image(trame) projetée dans rep Objet
    #Interpolation de données régulièrement maillées typiquement avec un meshgrid en utilisant la fonction map_coordinates
    coord = [uE1,vE1]
    r = map_coordinates(ima[:,:,0], coord) #, order = 1
    g = 0*r
    b = 0*r 
    # Im = np.stack((r,g,b),2)
    Im = np.dstack((r,g,b))
    del ima
    #enregistrement
    A = 'I' + str(k+1) + '.bmp' 
    io.imsave(A,Im)
    # plt.figure(k)
    # io.imshow(Im)
    
#Affichage
Nom_figure = 'Fig franges sur objet'+ str(k+1) +'.jpg'
plt.figure(),  plt.pcolor(X,Y,Im[:,:,0],  cmap='Greys'), plt.xlabel('X mm'),  plt.ylabel('Y mm'),  plt.title('Image projetée I(M)') 
# plt.figure(1).savefig(Nom_figure)

print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion
