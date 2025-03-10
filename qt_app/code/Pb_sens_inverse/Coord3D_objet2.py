import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt, savetxt
from scipy.interpolate import griddata

def genere_coord3D(progress_callback):
    progress_callback.emit(0)
    # Chargement des fichiers
    PosiGlobal = loadtxt('Posiglobal.txt')
    ME = loadtxt('ME.txt')
    MR = loadtxt('MR.txt')
    NBHE = loadtxt('NbHE.txt')
    N = loadtxt('N.txt')

    X, Y, Z, Xb, Yb, Zb = [], [], [], [], [], []

    # Boucle unique sur PosiGlobal
    for i in range(PosiGlobal.shape[0]):
        z_def = 0
        for e in range(PosiGlobal.shape[1]):
            if PosiGlobal[i, e] != 0:
                ur, vr = i, e
                
                if PosiGlobal[i, e] % 2 == 0:  # PosiGauche (2n)
                    ve = (NBHE / (2**N)) * PosiGlobal[i, e]
                else:  # PosiDroite (2n+1)
                    ve = (NBHE / (2**N)) * (PosiGlobal[i, e]) + 1

                # Construction des matrices G et H
                G = [[MR[2,0]*ur - MR[0,0], MR[2,1]*ur - MR[0,1], MR[2,2]*ur - MR[0,2]],
                    [MR[2,0]*vr - MR[1,0], MR[2,1]*vr - MR[1,1], MR[2,2]*vr - MR[1,2]],
                    [ME[2,0]*ve - ME[1,0], ME[2,1]*ve - ME[1,1], ME[2,2]*ve - ME[1,2]]]
                
                H = [[MR[0,3] - MR[2,3]*ur],
                    [MR[1,3] - MR[2,3]*vr],
                    [ME[1,3] - ME[2,3]*ve]]

                # Résolution du système linéaire
                inv_G = np.linalg.inv(G)
                (x, y, z) = np.matmul(inv_G, H)

                # Stockage des coordonnées
                X.append(x)
                Y.append(y)
                Z.append(z)
                z_def = z.item()
            Xb.append(e)
            Yb.append(i)
            Zb.append(z_def)

    # Affichage des points 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, s=0.5)
    plt.title("Points reconstruits en 3D")
    plt.show()

    savetxt('X_scan.txt', X, fmt='%-7.6f')
    savetxt('Y_scan.txt', Y, fmt='%-7.6f')
    savetxt('Z_scan.txt', Z)

    del PosiGlobal, ME, MR, NBHE, N, X, Y, Z

    print("Je suis là")  

    # Interpolation et enregistrement

    unique_X, unique_Y = np.unique(Xb), np.unique(Yb)
    print("Je suis là 2")
    X2, Y2 = np.meshgrid(unique_X, unique_Y)
    print("Je suis là 3")
    Z2 = griddata((Xb, Yb), Zb, (X2, Y2), method='linear')
    print("Je suis là 4")


    del Xb, Yb, Zb
    del unique_X, unique_Y


    # Affichage de l'image interpolée
    plt.figure()
    plt.pcolor(X2, Y2, Z2, cmap='gray', vmin=Z2.min(), vmax=np.nanmax(Z2))
    plt.title('Z (mm) - Objet bouclier simulé')
    plt.axis([X2.min(), X2.max(), Y2.min(), Y2.max()])
    plt.colorbar()
    plt.savefig("Nuances.png")
    progress_callback.emit(100)


class callback():
   def emit(self, value):
      print(value)
      if value == 100:
         plt.show()

if __name__ == '__main__':
   genere_coord3D( callback())
