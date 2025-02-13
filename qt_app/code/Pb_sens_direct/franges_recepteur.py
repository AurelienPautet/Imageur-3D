# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:59:46 2018
MAJ octobre 2023
@author: Lys Elisabeth
"""

#**************************************************************************
#*********************  Images vues par le recepteur *********************
#**************************************************************************

import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, linspace, sin, cos, pi, array, concatenate, savetxt, meshgrid, isnan
from skimage import io
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd

# Chargement de l'objet simulé dans repère Objet (O,X,Y,Z)
X = loadtxt('X.txt')
Y = loadtxt('Y.txt')
Z = loadtxt('Z.txt')

# Chargement de l'objet simulé dans repère Objet (O,X,Y,Z)
# X = loadtxt('X_toiture.txt')
# Y = loadtxt('Y_toiture.txt')
# Z = loadtxt('Z_toiture.txt')

# Chargement de l'objet simulé dans repère Objet (O,X,Y,Z)
# X = loadtxt('X_plan.txt')
# Y = loadtxt('Y_plan.txt')
# Z = loadtxt('Z_plan.txt')

#Chargement des angles du dispositif
[alpha_d,beta_d] = loadtxt('angles.txt')


#Chargement nombre de trame
N = loadtxt('N.txt')
N = int(N)
#--------- Paramètres CCD -------------
#Taille CCD (pixel)
NbHR = 1920  #en horizontal
NbVR = 1080   #en vertical

#coordonnées matricielles des pts mR du CCD
xx = linspace(0,NbHR-1,NbHR)
yy = linspace(0,NbVR-1,NbVR)
    
#Coordonnées matricielles des pts mE du LCD
vR,uR = meshgrid(xx,yy)

#Zoom récepteur sur 1:1080x1:1400 au lieu de 1:1080x1:1920

zoom = 1500
# zoom = NbHR # Pour ne pas faire de zoom
uRzoomvect = linspace(0,zoom-1,zoom) # linspace(0,1299,1300)
vRzoomvect = linspace(0,NbVR-1,NbVR)


savetxt('uRzoomvect.txt', uRzoomvect, fmt='%-7.0f')
savetxt('vRzoomvect.txt', vRzoomvect,fmt='%-7.0f')
[vRzoom,uRzoom] = meshgrid(uRzoomvect,vRzoomvect)
savetxt('uRzoom.txt', uRzoom, fmt='%-7.0f')
savetxt('vRzoom.txt', vRzoom, fmt='%-7.0f')

#---------- Matrice de projection perspective récepteur MR ------------
#Angles du dispositif
alpha = alpha_d*pi/180
beta = beta_d*pi/180
phiR = -pi/2
thetaR = -pi/2-(alpha+beta)/2
psiR = 0.

#Distances ou composantes translation du dispositif (mm)
L = 950. # mm
t1R = 0.
t2R = 0.
t3R = sin(alpha)/sin(alpha+beta)*L
#Vecteur translation TR
TR = np.transpose(array([[t1R, t2R, t3R]]))

#Matrice de rotation RR
r11R = cos(phiR)*cos(thetaR)
r21R = sin(phiR)*cos(thetaR)
r31R = -sin(thetaR)
r12R = cos(phiR)*sin(thetaR)*sin(psiR) - sin(phiR)*cos(psiR)
r22R = sin(phiR)*sin(thetaR)*sin(psiR) + cos(phiR)*cos(psiR)
r32R = cos(thetaR)*sin(psiR)
r13R = cos(phiR)*sin(thetaR)*cos(psiR) + sin(phiR)*sin(psiR)
r23R = sin(phiR)*sin(thetaR)*cos(psiR) - cos(phiR)*sin(psiR)
r33R = cos(thetaR)*cos(psiR)

RR = array([[r11R, r12R, r13R], [r21R, r22R, r23R], [r31R, r32R, r33R]])


#Facteurs d'échelle du CCD (mm-1) = 1/TaillePixel
kuR = 454.545
kvR = 454.545

#Focale recepteur (mm)
fR = 3.67

#Paramètres intrinsèques
alphauR = -kuR*fR
alphavR = kvR*fR

#Centre axe optique sur CCD
u0R = NbVR/2 - 0.5
v0R = NbHR/2 - 0.5

#Matrice ICR
ICR = array([[alphauR, 0, u0R, 0], [0, alphavR, v0R, 0], [0, 0, 1, 0]])

#Matrice AR
RRTR = concatenate((RR,TR),axis = 1)
intermed = array([(0, 0, 0, 1)])
AR = concatenate((RRTR, intermed),axis=0)

#Matrice MR
MR = ICR.dot(AR)
savetxt('MR.txt', MR, fmt='%-7.9f')

 #--------- Projection sur récepteur ------------
sRuR1 = MR[0,0]*X + MR[0,1]*Y + MR[0,2]*Z + MR[0,3]
sRuR1 = array(sRuR1)
sRvR1 = MR[1,0]*X + MR[1,1]*Y + MR[1,2]*Z + MR[1,3]
sRvR1 = array(sRvR1)
sR = MR[2,0]*X + MR[2,1]*Y + MR[2,2]*Z + MR[2,3]
sR = array(sR)
uR1 = sRuR1/sR
vR1 = sRvR1/sR

#--- Calcul des images récepteur IR pour les N trames ---
#Libération mémoire
# sRuR1 = None
# sRvR1 = None
# sR = None
# X = None
# Y = None
# Z= None

del sRuR1, sRvR1, sR, X, Y, Z   
for k in range (N):
    #------ Chargement des images d'intensité I de l'objet ---
    Nom='I' + str(k+1) + '.bmp'    
    ima = io.imread(Nom)
    
    #Calcul de l'inage de réception IR
    # on utilise "interpolate.griddata" à la place de "ndimage.map_coordinates" car vR1 et uR1 
    # pas directement issus d'un "meshgrid" - Cette fonction est plus lente que map_coordinates, il faut compter 10s par image
   
    #Détermination de l'image projetée dans rep Objet
    r = griddata((uR1.flatten(),vR1.flatten()),ima[:,:,0].flatten(),(uR,vR), method='linear')#.astype(np.uint8)
    # Remplace tous les NaN par des 0
    r[isnan(r)] = 0
    r = r.astype(np.uint8)
    g = r*0
    b = r*0

    IR = np.dstack((r,g,b))
    del ima
    #enregistrement
    A = 'IRZoom' + str(k+1) + '.bmp'    
    IRzoom = IR[:,0:zoom]# IR[:,:]
    io.imsave(A,IRzoom)
    
    # plt.figure(k)
    # io.imshow(IRzoom)
    
    #Affichage des images zoom
#    Nom_figure = 'Fig image recepteur zoom'+ str(k+1) +'.png'
    # plt.figure(k),  plt.pcolor(vRzoom,uRzoom,IRzoom[:,:,0],  cmap='Greys'), plt.xlabel('vR pixels'),  plt.ylabel('uR pixels'),  plt.title('Image IR(mR) ZOOM') 
#    plt.figure(1).savefig(Nom_figure)    
    
    #Libération mémoire
    # A = None
    # IRzoom = None
    # IR = None    
    del IR, IRzoom, r, g, b
print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion