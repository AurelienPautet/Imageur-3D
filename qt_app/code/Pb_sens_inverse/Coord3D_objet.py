import time

# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, size, sin, cos, pi, array, concatenate,dot, savetxt
from scipy.interpolate import griddata

# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
#On importe ndimage pour pouvoir utiliser la fonction d'interpolation map_coordinates
def genere_coord3D(progress_callback):
   progress_callback.emit(0)
   start_time = time.process_time() # début mesure temps d'éxecusion
   PosiDroite = loadtxt('PosiDroite.txt')
   PosiGauche = loadtxt('PosiGauche.txt')
   PosiGlobal = loadtxt('Posiglobal.txt')

   ME = loadtxt('ME.txt')
   MR = loadtxt('MR.txt')
   NBHE = loadtxt('NbHE.txt')
   N = loadtxt('N.txt')

   NbHO = 1280
   NbVO = 800

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

               # Convert X, Y, Z lists to numpy arrays
   X = np.array(X)
   Y = np.array(Y)
   Z = np.array(Z)

               # Determine the dimensions of the 2D matrix
   max_x = int(np.max(X)) + 1
   max_y = int(np.max(Y)) + 1

   progress_callback.emit(50)
               # Save the 2D matrix to a file

   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')
   ax.scatter(X, Y, Z, s=0.5)
   savetxt('X_scan.txt', X, fmt='%-7.6f')
   savetxt('Y_scan.txt', Y, fmt='%-7.6f')
   savetxt('Z_scan.txt', Z)
   print(Z)
   #plt.show()

   X = []
   Y = []
   Z = []

   for i in range(len(PosiGlobal)):
      z_def = -10  # on fixe la valeur de z
      for e in range(len(PosiGlobal[0])):
         if PosiGlobal[i,e] !=0:
            ur = i
            vr = e
            ve = (NBHE/(2**N))*PosiGlobal[i,e]+1
            G=[[MR[2,0]*ur -MR[0,0] , MR[2,1]*ur - MR[0,1],MR[2,2]*ur - MR[0,2]],
               [MR[2,0]*vr -MR[1,0] , MR[2,1]*vr - MR[1,1],MR[2,2]*vr - MR[1,2]],
               [ME[2,0]*ve -ME[1,0] , ME[2,1]*ve - ME[1,1],ME[2,2]*ve - ME[1,2]]]
            H=[[MR[0,3]-MR[2,3]*ur],
               [MR[1,3]-MR[2,3]*vr],
               [ME[1,3]-ME[2,3]*ve]]
            inv_G = np.linalg.inv(G)
            (x,y,z) = np.matmul(inv_G,H) 
            z_def = z.item()
         X.append(e)
         Y.append(i)
         Z.append(z_def)
# Création de la grille X2, Y2
   unique_X = np.unique(X)
   unique_Y = np.unique(Y)
   X2, Y2 = np.meshgrid(unique_X, unique_Y)

   # Interpolation des valeurs de Z sur la grille X2, Y2
   # Remove NaN values from X, Y, Z
   mask = ~np.isnan(Z)
   X = np.array(X)[mask]
   Y = np.array(Y)[mask]
   Z = np.array(Z)[mask]

   Z2 = griddata((X, Y), Z, (X2, Y2), method='linear')
   print("on en est la ")

   #Enregistrement des coordonnées matricelles objet
   savetxt('X2.txt', X2, fmt='%-7.6f')   
   savetxt('Y2.txt', Y2, fmt='%-7.6f')
   savetxt('Z2.txt', Z2, fmt='%-7.6f')  

   # Affichage du résultat avec colorbar
   plt.figure()
   plt.pcolor(X2, Y2, Z2, cmap='gray', vmin=-10, vmax=np.nanmax(Z2))
   plt.title('Z (mm) - Objet bouclier simulé')
   plt.axis([X2.min(), X2.max(), Y2.min(), Y2.max()])
   plt.colorbar()
   plt.savefig("Nuances.png")
   progress_callback.emit(100)

class callback():
   def emit(self, value):
      print(value)

if __name__ == '__main__':
   genere_coord3D( callback())