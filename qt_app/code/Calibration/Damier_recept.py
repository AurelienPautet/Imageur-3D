# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:42:08 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""

#**************************************************************************
#****** Mire damier posee sur l'objet projetee sur recepteur *************
#**************************************************************************
import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import ones, concatenate, cos, sin, pi, array, meshgrid, linspace, transpose, uint8, isnan
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
# permet d'utiliser griddata
from scipy.interpolate import griddata
from skimage import io

#----------------------Creation de la mire damier objet  ------------------

#Nombre de carreaux 
p = 8 #horizontaux
q = 8 #verticaux



#Nb pixel Objet mire (echantillonnage simulation)
NbHO = 1280
NbVO = 800

#Taille objet mire
LX = 995  #[mm]
LY = 622  #[mm]

#Coordonnées matricielles des pts M de l'objet mire
[X,Y] = meshgrid(linspace(-LX/2,LX/2,NbHO),linspace(-LY/2,LY/2,NbVO))

Z = 0*ones((NbVO,NbHO), dtype = float) #[mm]
# Z = 100.*ones((NbVO,NbHO), dtype = float); #[mm]

#Intensite mire damier objet

IdO = np.empty((NbVO,NbHO))
IdO = 1*(sin(X*p*pi/LX)*(sin(Y*q*pi/LY))>0) #Seuil sur multiplication sinus 


#Enregistrement de l'image Mire_damier_objet
A = "Mire_damier_objet.bmp"
r0 = 255*IdO   
g0 = 0*IdO
b0 = 0*IdO

B0 = np.dstack((r0,g0,b0))
B0 = uint8(B0)
io.imsave(A,B0) 


#---------------- Parametres du recepteur CCD------------------------------
#Taille CCD (pixel)
NbHR = 1920 #1600  #en horizontal
NbVR = 1080 #1200   #en vertical
#coordonnées matricielles des pts mR du CCD
xx = linspace(0,NbHR-1,NbHR)
yy = linspace(0,NbVR-1,NbVR)
vR,uR = meshgrid(xx,yy)

#---- Matrice de projection perspective recepteur MR ----
#Angles du dispositif
alpha_d = 55 #[°]
beta_d = 85 #[°]
alpha = alpha_d*pi/180 #[rad]
beta = beta_d*pi/180 #[rad]

np.savetxt('angles.txt', (alpha_d, beta_d), fmt='%1.16e')
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

#Facteurs d'echelle du CCD 
kuR = 454.545 #[mm-1]
kvR = 454.545 #[mm-1]

#Focale recepteur
fR = 3.67 #[mm]

#Parametres intrinsèques
alphauR = -kuR*fR #[]
alphavR = kvR*fR #[]

#Centre axe optique sur CCD
u0R = NbVR/2-0.5 #[pixel]
v0R = NbHR/2-0.5 #[pixel]

#Matrice ICR
ICR = array([[alphauR, 0, u0R, 0], [0, alphavR, v0R, 0], [0, 0, 1, 0]])

#Matrice AR
RRTR = concatenate((RR,TR),axis=1)
intermed = array([(0, 0, 0, 1)])
AR = concatenate((RRTR, intermed),axis=0)
#print(AR)

#Matrice MR
MR = ICR.dot(AR)
np.savetxt('MR.txt', MR, fmt='%-7.9f')

#----------------- Image de la mire projetee sur   ---------------
#Projection abscisses et ordonnees Objet mire sur recepteur CCD


sRuR1 = MR[0,0]*X + MR[0,1]*Y + MR[0,2]*Z + MR[0,3]
sRuR1 = array(sRuR1)
sRvR1 = MR[1,0]*X + MR[1,1]*Y + MR[1,2]*Z + MR[1,3]
sRvR1 = array(sRvR1)
sR = MR[2,0]*X + MR[2,1]*Y + MR[2,2]*Z + MR[2,3]
sR = array(sR)

uR1 = sRuR1/sR
vR1 = sRvR1/sR

#Determination de l'image projetee dans rep recepteur IdR
# on utilise "griddata" à la place de la fonction d'interpolation 
#"ndimage.map_coordinates" car vR1 et uR1
# pas directement issus d'un "meshgrid"
#Détermination de l'image projetée dans rep Objet

#Libération mémoire
sRuR1 = None
sRvR1 = None
sR = None
Z = None
AR = None
ICR = None
RR = None
TR = None
MR = None
xx = None
yy = None

# On utilise ici la méthode cubic en sous echantillonant car méthode très longue qui permet de récupérer les bords en NaN puis on les remplace dans le IdR issu de nearest 
#car avec cette dernière on a un damier prolongé en dehors de la zone d'interet

# Sous echantillonnage : On prend une valeur sur step = 4
step = 10
uR1e = uR1[0:NbVO:step, 0:NbHO:step]
vR1e = vR1[0:NbVO:step, 0:NbHO:step]

points_e =np.zeros((2,np.size(uR1e)))

points_e[0] = uR1e.flatten()
points_e[1] = vR1e.flatten()
points_e = points_e.T


IdOe = IdO[0:NbVO:step, 0:NbHO:step]
valeur_e = IdOe.flatten()

coord =np.zeros((2,np.size(uR)))
coord[0] = uR.flatten()
coord[1] = vR.flatten()
coord = coord.T


IdR1 = griddata(points_e,valeur_e,coord, 'cubic').reshape(NbVR,NbHR) #, method='linear'

points =np.zeros((2,np.size(uR1)))

points[0] = uR1.flatten()
points[1] = vR1.flatten()
points = points.T



valeur = IdO.flatten()
valeur = valeur.astype(np.float64)
IdR = griddata(points,valeur,coord, 'nearest').reshape(NbVR,NbHR) #, method='linear'

## Seuillage de l'image qui permet d'enregistrer le damier en rouge et noir
threshold = 0.5
idx = IdR[:,:] < threshold 
IdR[idx] = 0
idx2 = IdR[:,:] >= threshold  
IdR[idx2] = 1


## Seuillage de l'image qui permet d'enregistrer le damier en rouge et noir
idx1 = IdR1[:,:] < threshold 
IdR1[idx1] = 0
idx3 = IdR1[:,:] >= threshold  
IdR1[idx3] = 1

IdR = IdR.astype(np.float64)
import math
for i in range(NbVR):
    for j in range (NbHR):
        if math.isnan(IdR1[i,j]) == True:
            # print('i=',i,'j=',j)
            IdR[i,j] = np.nan


#enregistrement intensite recepteur IdR
#Libération mémoire
A = None
B = None

##Intensite mire damier objet

A = "IdR.bmp"
# A = "IdR100.bmp"
r = 255*IdR   
g = 0*IdR
b = 0*IdR

B = np.dstack((r,g,b))
B = uint8(B)
io.imsave(A,B)  

# #enregistrement intensite recepteur IdR
# #Libération mémoire
# A = None
# B = None

# ##Intensite mire damier objet
# A = "IdR1.bmp"
# #A = "IdR100.bmp"
# r = 255*IdR1   
# g = 0*IdR1
# b = 0*IdR1

# B = np.dstack((r,g,b))
# B = uint8(B)
# io.imsave(A,B)  



# #Affichage
# plt.figure()
# plt.pcolor(X,Y,IdO, cmap='gray')
# plt.title('Image IdO')
# # set the limits of the plot to the limits of the data
# plt.axis([X.min(), X.max(), Y.min(), Y.max()])

# plt.figure()
# plt.pcolor(vR,uR,IdR, cmap='gray') #
# plt.title('Image IdR')

print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion