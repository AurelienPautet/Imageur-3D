# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 08:28:41 2017
MAJ octobre 2023
@author: Elisabeth Lys
"""
# %%
import time

# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
from skimage import io
from skimage import filters
from skimage.morphology import disk
# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import loadtxt, empty, zeros, ones, savetxt

def localisation_cotes_franges(progress_callback):
    progress_callback.emit(0)
    start_time = time.process_time() # début mesure temps d'éxecusion

    #Chargement nombre d'image
    N = loadtxt('N.txt', np.int32)
    #Chargement abscisses et ordonnées récepteur zoom
    uRzoomvect = loadtxt('uRzoomvect.txt')
    vRzoomvect = loadtxt('vRzoomvect.txt')

    #Chargement abscisses et ordonnées récepteur zoom
    uRzoom = loadtxt('uRzoom.txt')
    vRzoom = loadtxt('vRzoom.txt')

    #Taille récepteur zoom
    NbVRzoom = len(uRzoomvect)
    NbHRzoom = len(vRzoomvect)

    #On créé la matrice IRzoom
    IRzoom = zeros((NbHRzoom,NbVRzoom,N))
    Posiglobal = zeros((NbHRzoom,NbVRzoom))
    PosiGauche = zeros((NbHRzoom,NbVRzoom))
    PosiDroite = zeros((NbHRzoom,NbVRzoom))

    # Seuillage de l'image
    threshold = 230
    # chargement de l'image puis binarisation 
    for k in range (N):

        #------ Chargement des images d'intensité IRZoom de l'objet dans le repere recepteur ---  
        #Nom = f'IRZoom{str(k + 1)}.bmp'
        Nom = f'capture{str(k + 1)}.bmp'
        # Resize the image to 1080x1500
        img = io.imread(Nom)
        img = img[:1080, :1500]

        img[:, :, 0] = filters.median(img[:, :, 0], disk(5))
        io.imsave(f'processed_IRZoom{str(k + 1)}.bmp', img)
        idx = img[:,:,0] > threshold
        img[idx,0] = 255
        img[idx,1] = 0
        img[idx,2] = 0
        idx = img[:,:,0] <= threshold
        img[idx,0] = 0
        img[idx,1] = 0
        img[idx,2] = 0
        io.imsave(f'processed_IRZoom_bis{str(k + 1)}.bmp', img)
        img[:, :, 0] = filters.median(img[:, :, 0], disk(5))
        io.imsave(f'processed_IRZoom_bis_bis{str(k + 1)}.bmp', img)
        idx = img[:,:,0] > threshold
        img[idx,0] = 255

        idx = img[:,:,0] <= threshold
        img[idx,0] = 0
        img[idx,1] = 0
        img[idx,2] = 0

        IRz = (img/255)
        # On enregistre les IRzoom_1 2 3 ... dans IR_zoom
        #IRz[:,:,0] = filters.median(IRz[:,:,0], disk(5))
        IRzoom[:,:,k] = IRz[:,:,0]
        progress_callback.emit((k+1)/N*2*100)

    #Libération mémoire
    Nom = None
    R = None     

    # ----------------------Localisation de la frange C 
        
    #On initialise les variales LClogic et LC 
    LC_num = empty((NbHRzoom,NbVRzoom))
    LClogic = ones((NbHRzoom,NbVRzoom), dtype=bool) 

    LC = zeros((NbHRzoom,NbVRzoom))
    for C in range (1,2**N+1,2):

        #Numéro base binaire de la frange à localiser
        Cbin = np.binary_repr(C, N)
        
        # On transforme le nombre binaire en une liste dont on peut chercher les éléments un à un
        tabCbin = list(map(int, Cbin)) 
        
        # Localisation de la frange C impaire
        LClogic = IRzoom[:,:,0]==tabCbin[0]
        for l in range (1,N):
            LClogic = LClogic & (IRzoom[:,:,l]==tabCbin[l])
    
        # Matrice de localisation numérique 
        LC = LClogic*1
        
        # Libération de la mémoire
        del LClogic
        # IRzoom[:,:,l] = None
        # Filtrage médian sur les images des franges permet de nettoyer les petites imperfections
        LC = filters.median(np.uint8(LC),disk(5))

        for i in range (NbHRzoom): #NbHRzoom
            
            p0 = np.nonzero(LC[i,:] == 1)[0]
            if len(p0) > 0: 
                aG = p0[0] # first element -> début de frange
                aD = p0[-1] # last element -> fin de frange
                # on concatène les position 
                # Position G et D
                Posiglobal[i,aG] = C 
                Posiglobal[i,aD] = C + 1 
                #on concatène les position gauche avec les positions G existantes
                PosiGauche[i,aG] = C
                #on concatène les position droite avec les positions D existantes
                PosiDroite[i,aD] = C + 1
        progress_callback.emit((C+1)/2**N*100)

    #Enregistrement 
    savetxt('PosiGauche.txt', PosiGauche, fmt='%-7.0f')
    savetxt('PosiDroite.txt', PosiDroite, fmt='%-7.0f')
    savetxt('Posiglobal.txt', Posiglobal, fmt='%-7.0f')
    savetxt('LC_num.txt', LC_num, fmt='%-7.0f')

    #Inversion de contraste pour l'affichage
    InvPosiglobal=1.-Posiglobal

    #Enregistrement image des cotes de franges
    couleur_cotes = np.asarray([255,255,255])  #Blanc intensitee maximale
    B = zeros((NbHRzoom,NbVRzoom,3))

    A = 'Cotes_franges.bmp'
    B[:,:,0] = couleur_cotes[0]*InvPosiglobal
    B[:,:,1] = couleur_cotes[1]*InvPosiglobal
    B[:,:,2] = couleur_cotes[2]*InvPosiglobal
    B=B.astype(np.uint8)
    io.imsave(A,B)

    # Affichage
    """
    plt.figure()
    plt.imshow(PosiGauche, cmap = plt.get_cmap('gray'))
    plt.title('Position Gauche')
    plt.show()

    plt.figure()
    plt.imshow(PosiDroite, cmap = plt.get_cmap('gray'))
    plt.title('Position Droite')
    plt.show()

    plt.figure()
    plt.imshow(Posiglobal, cmap = plt.get_cmap('gray'))
    plt.title('Position Globale')
    plt.show()

    #Affichage de l'image enregistrée des positions globales des franges
    plt.figure()
    plt.imshow(B[:,:,1], cmap = plt.get_cmap('gray'))
    plt.title('Image des cotés des franges')
    plt.xlabel('vRzoom pixels')
    plt.ylabel('uRzomm pixels')
    plt.show()
    """
    print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion
    # %%
class callback():
   def emit(self, value):
      print(value)


if __name__ == '__main__':
    localisation_cotes_franges(callback())