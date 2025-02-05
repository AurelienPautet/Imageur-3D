# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 09:26:41 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""

#**************************************************************************
#**** Mire damier projetee par emetteur sur recepteur ********************
#**************************************************************************
#***************************** Python **********************************

import time
start_time  =  time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, ones, concatenate, cos, sin, pi, array, meshgrid, linspace, transpose, uint8
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
# permet d'utiliser griddata
from scipy import interpolate
from skimage import io
from scipy import ndimage

#Chargement des angles du dispositif
[alpha_d,beta_d] = loadtxt('angles.txt')

#-------- Creation de l'objet de calibration -----------------------------
#Nb pixel Objet (échantillonnage simulation)
NbHO = 1280
NbVO = 800

#Coordonnees matricielles des pts M de l'objet
[X,Y] = meshgrid(linspace(-600,600,NbHO),linspace(-375,375,NbVO))
Z = 0.*ones((NbVO,NbHO), dtype = float) #[mm]
# Z = 100.*ones((NbVO,NbHO), dtype = float) #[mm]

#Taille LCD (pixel)
NbHE = 1280 #horizontal
NbVE = 800  #vertical

#Coordonnees matricielles des pts mE du LCD
xE = linspace(0,NbHE-1,NbHE)
yE = linspace(0,NbVE-1,NbVE)
vE,uE = meshgrid(xE,yE)

#Taille CCD (pixel)
NbHR = 1920  #horizontal
NbVR = 1080  #vertical

#coordonnees matricielles des pts mR du CCD
xx = linspace(0,NbHR-1,NbHR)
yy = linspace(0,NbVR-1,NbVR)
vR,uR = meshgrid(xx,yy)

#---------- Matrice de projection perspective emetteur ME ------------


#Angles du dispositif
alpha = alpha_d*pi/180
beta = beta_d*pi/180

phiE = -pi/2 #[rad]
thetaE = pi/2+(alpha+beta)/2 #[rad]
psiE = 0 #[rad]

#Distances ou composantes translation du dispositif
L = 950 #[mm]
t1E = 0 #[mm]
t2E = 0 #[mm]
t3E = sin(beta)/sin(alpha+beta)*L #[mm]

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

#Vecteur translation TE
TE = transpose(array([[t1E, t2E, t3E]]))
#print(TE.shape) 
#print(TE)

#Facteurs d'echelle du LCD
kuE = 100.723 #[mm-1]
kvE = 100.723 #[mm-1]

#Focale emetteur (mm)
fE = 20.28 
# fE = 16.9 #[mm]

#Paramètres intrinseques
alphauE = -kuE*fE #[]
alphavE = kvE*fE #[]

#Centre axe optique sur LCD
u0E = NbVE/2 - 0.5; #[pixel]
v0E = NbHE/2 - 0.5; #[pixel]

#Matrice ICE
ICE = array([[alphauE, 0, u0E, 0], [0, alphavE, v0E, 0], [0, 0, 1, 0]])

#Matrice AE
RETE = concatenate((RE,TE),axis=1)
intermed = array([(0, 0, 0, 1)])
AE = concatenate((RETE, intermed),axis=0)
#print(AE)

#Matrice ME
ME = ICE.dot(AE)
np.savetxt('ME.txt', ME, fmt='%-7.9f')


#---------- Matrice de projection perspective récepteur MR ------------
#Angles du dispositif

phiR = -pi/2 #[rad]
thetaR = -pi/2-(alpha+beta)/2 #[rad]
psiR = 0 #[rad]

#Distances ou composantes translation du dispositif
L = 950 #[mm]
t1R = 0 #[mm]
t2R = 0 #[mm]
t3R = sin(alpha)/sin(alpha+beta)*L #[mm]

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

#Vecteur translation TR
TR = transpose(array([[t1R, t2R, t3R]]))
#print(TR.shape) 
#print(TR)

#Facteurs d'echelle du CCD (mm-1)
kuR = 454.545 #[mm-1]
kvR = 454.545 #[mm-1]

#Focale recepteur
fR = 3.67 #[mm]

#Parametres intrinseques
alphauR = -kuR*fR #[]
alphavR = kvR*fR #[]

#Centre axe optique sur CCD
u0R = NbVR/2 - 0.5 #[pixel]
v0R = NbHR/2 - 0.5 #[pixel]

#Matrice ICR
ICR = array([[alphauR, 0, u0R, 0], [0, alphavR, v0R, 0], [0, 0, 1, 0]])

#Matrice AR
RRTR = concatenate((RR,TR),axis=1)
intermed = array([(0, 0, 0, 1)])
AR = concatenate((RRTR, intermed),axis=0)
#print(AR)

#Matrice MR
MR = ICR.dot(AR)

#------------- Image de la mire projetee sur l'objet  -------------
#------ Chargement des images d'intensite IE du LCD ---
Nom = 'Mire_damier.bmp'    
ima = io.imread(Nom)
ima = ima[:, :, 0]
IdE = (ima/255)#matrice numeric normalisee

#Projection de l'emetteur
sEuE1 = ME[0,0]*X + ME[0,1]*Y + ME[0,2]*Z + ME[0,3]
sEuE1 = array(sEuE1)
sEvE1 = ME[1,0]*X + ME[1,1]*Y + ME[1,2]*Z + ME[1,3]
sEvE1 = array(sEvE1)
sE = ME[2,0]*X + ME[2,1]*Y + ME[2,2]*Z + ME[2,3]
sE = array(sE)

uE1 = sEuE1/sE
vE1 = sEvE1/sE

#Determination de l'image projetee dans rep Objet (interpolation)
coord = [uE1,vE1]
Id = ndimage.map_coordinates(IdE, coord )

# Seuillage de l'image
threshold = 0.5
idx = Id[:,:] < threshold 
Id[idx] = 0
idx2 = Id[:,:] > threshold  
Id[idx2] = 1

#On cherche les nan pour les remplacer par des 0, pour ne pas perturber la conversion RGB
where_are_NaNs = np.isnan(Id)
Id[where_are_NaNs] = 0

#enregistrement intensite Objet Id

#Libération mémoire
A = None
B = None

#Intensite mire damier objet

A = "Id.bmp"
r = 255*Id    
g = 0*Id
b = 0*Id
B = np.dstack((r,g,b))
B = uint8(B)
#enregistrement
io.imsave(A,B)

#Projection sur recepteur
sRuR1 = MR[0,0]*X + MR[0,1]*Y + MR[0,2]*Z + MR[0,3]
sRuR1 = array(sRuR1)
sRvR1 = MR[1,0]*X + MR[1,1]*Y + MR[1,2]*Z + MR[1,3]
sRvR1 = array(sRvR1)
sR = MR[2,0]*X + MR[2,1]*Y + MR[2,2]*Z + MR[2,3]
sR = array(sR)

uR1 = sRuR1/sR
vR1 = sRvR1/sR

##Determination de l'image projetee dans rep recepteur
IdR = interpolate.griddata((uR1.flatten(),vR1.flatten()),Id.flatten(),(uR,vR), method='nearest')# method='cubic'

#Enregistrement intensite recepteur IdR
# Seuillage de l'image
threshold = 0.5
idrx = IdR[:,:] < threshold 
IdR[idrx] = 0
idrx2 = IdR[:,:] > threshold  
IdR[idrx2] = 1

#On cherche les nan pour les remplacer par des 0, pour ne pas perturber la conversion RGB
where_are_NaNs = np.isnan(IdR)
IdR[where_are_NaNs] = 0

#enregistrement intensite recepteur IdR

#Libération mémoire
A = None
B = None

#Intensite mire damier objet
A = "IdR_calibemet.bmp"
# A = "IdR100_calibemet.bmp"
r = 255*IdR    
g = 0*IdR
b = 0*IdR
B = np.dstack((r,g,b))
B = uint8(B)
#enregistrement
io.imsave(A,B)

# ------- Affichage ------
# plt.figure()
# plt.pcolor(vR,uR,IdR, cmap='gray') #
# plt.title('Image IdR - image projetée dans le repère récepteur')
# plt.xlabel('vR pixels')
# plt.ylabel('uR pixels')

# plt.figure()
# plt.pcolor(X,Y,Id, cmap='gray') #
# plt.title('Image Id - Image projetée dans le repère objet')
# plt.xlabel('X mm')
# plt.ylabel('Y mm')
    
print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion








