# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 08:28:41 2017
MAJ octobre 2023
@author: Elisabeth Lys
"""
import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
#from skimage import io, transform
from skimage import io
# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, zeros, ones

#Chargement nombre d'image
N = loadtxt('N.txt', np.int32)

#Chargement abscisses et ordonnées récepteur zoom
uRzoomvect = loadtxt('uRzoomvect.txt')
vRzoomvect = loadtxt('vRzoomvect.txt')

#Chargement abscisses et ordonnées récepteur zoom
uRzoom = loadtxt('uRzoom.txt')
vRzoom = loadtxt('vRzoom.txt')
NbVRzoom = len(uRzoomvect)
NbHRzoom = len(vRzoomvect)

#Numéro base décimale de la frange à localiser
C = 12
#Numéro base binaire de la frange à localiser
Cbin = np.binary_repr(C, N)

# taille des matrice uRzoom : lignes colonnes
i = len(uRzoom)
j = len(uRzoom[0])

#On créé la matrice IRzoom
IRzoom = zeros((i,j,N))

#On charge les images IRZoom et on les binarises
for k in range (0,N):
    #------ Chargement des images d'intensité IRZoom de l'objet dans le repere recepteur ---  
    Nom = 'IRZoom' + str(k+1) + '.bmp'
    img = io.imread(Nom)
    # Seuillage de l'image
    threshold = 125
    idx = img[:,:,0] > threshold
    img[idx,0] = 255
    IRz = (img/255)
    #Matrice normalisée  
    # On enregistre les IRzoom_1 2 3 ... dans IR_zoom
    IRzoom[:,:,k] = IRz[:,:,0]
    IRzoom = IRzoom.astype(int) # on passe du type float au type int

#    #Libération mémoire
    Nom = None
    R = None
    
# ----------------------Localisation de la frange C 
    
#On initialise les variales LClogic et LC
LClogic = ones((NbHRzoom,NbVRzoom), dtype=bool) 
LC = zeros((NbHRzoom,NbVRzoom), dtype=int)

# On transforme le nombre binaire en une liste dont on peut chercher les éléments un à un
tabCbin = list(map(int, Cbin))#Attention modification de la fonction avec Python3/ python2

# Localisation de la frange C 
LClogic = IRzoom[:,:,0] == tabCbin[0]
for l in range (1,N):
    LClogic = LClogic & (IRzoom[:,:,l] == tabCbin[l])
 
#Matrice de localisation numérique 
LC = LClogic*1
   
# affichage 
plt.figure()
plt.imshow(LC, cmap = plt.get_cmap('gray'))
plt.title('Image frange C = 12')
plt.xlabel('vR pixels')
plt.ylabel('uR pixels')
plt.show()
# plt.figure(1).savefig('Localisation_Frange _12.png') 

print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion