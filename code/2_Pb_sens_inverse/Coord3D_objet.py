import time
start_time = time.process_time() # début mesure temps d'éxecusion

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, size, sin, cos, pi, array, concatenate,dot
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
#On importe ndimage pour pouvoir utiliser la fonction d'interpolation map_coordinates

PosiDroite = loadtxt('PosiDroite.txt')
PosiGauche = loadtxt('PosiGauche.txt')

ME = loadtxt('ME.txt')
MR = loadtxt('MR.txt')
NBHE = loadtxt('NbHE.txt')
N = loadtxt('N.txt')



X=[]
Y=[]
Z=[]

for i in range(len(PosiDroite)):
    for e in range(len(PosiDroite[0])):
        if PosiDroite[i,e] !=0:
            ur = i
            vr = e 
            ve = (NBHE/(2**N))*PosiDroite[i,e]
            G=[[MR[2,0]*ur -MR[0,0] , MR[2,1]*ur - MR[0,1],MR[2,2]*ur - MR[0,2]],
               [MR[2,0]*vr -MR[1,0] , MR[2,1]*vr - MR[1,1],MR[2,2]*vr - MR[1,2]],
               [ME[2,0]*ve -ME[1,0] , ME[2,1]*ve - ME[1,1],ME[2,2]*ve - ME[1,2]]]
            H=[[MR[0,3]-MR[2,3]*ur],
               [MR[1,3]-MR[2,3]*vr],
               [ME[1,3]-ME[2,3]*ve]]
            inv_G = np.linalg.inv(G)
            (x,y,z) = np.matmul(inv_G,H)
            X.append(x)
            Y.append(y)
            Z.append(z)

for i in range(len(PosiGauche)):
    for e in range(len(PosiGauche[0])):
        if PosiGauche[i,e] !=0:
            ur = i
            vr = e 
            ve = (NBHE/(2**N))*PosiGauche[i,e]+1
            G=[[MR[2,0]*ur -MR[0,0] , MR[2,1]*ur - MR[0,1],MR[2,2]*ur - MR[0,2]],
               [MR[2,0]*vr -MR[1,0] , MR[2,1]*vr - MR[1,1],MR[2,2]*vr - MR[1,2]],
               [ME[2,0]*ve -ME[1,0] , ME[2,1]*ve - ME[1,1],ME[2,2]*ve - ME[1,2]]]
            H=[[MR[0,3]-MR[2,3]*ur],
               [MR[1,3]-MR[2,3]*vr],
               [ME[1,3]-ME[2,3]*ve]]
            inv_G = np.linalg.inv(G)
            (x,y,z) = np.matmul(inv_G,H)
            X.append(x)
            Y.append(y)
            Z.append(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, s=0.5)
plt.show()

