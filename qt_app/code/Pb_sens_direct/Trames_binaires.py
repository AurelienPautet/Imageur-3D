# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:59:46 2018
MAJ octobre 2023
@author: Elisabeth Lys
"""
import time
# On importe le module numpy qui permet de faire du calcul numérique
import numpy as np
from numpy import linspace, zeros, savetxt, sin, pi, uint8
# On importe le module matplotlib qui permet de générer des graphiques 2D et 3D
import matplotlib.pyplot as plt
from skimage import io    

def faire_franges(progress_callback):
    start_time = time.process_time()  # début mesure temps d'éxecusion
    progress_callback.emit(0)
    # Définition du nombre de trames
    N = 5
    f = open('N.txt', 'w')
    f.write('%d' % N)
    f.close()

    #----- Paramètre LCD ---------------
    #Taille en pixel
    NbHE = 1280  # sur horizontal
    NbVE = 800  # sur vertical
    f = open('NbHE.txt', 'w')
    f.write('%d' % NbHE)
    f.close()

    x = linspace(0, NbHE-1, NbHE)
    y = linspace(0, NbVE-1, NbVE)

    # Coordonnées matricielles des pts mE du LCD
    vE, uE = np.meshgrid(x, y)

    savetxt('uE.txt', uE, fmt='%-7.0f')
    savetxt('vE.txt', vE, fmt='%-7.0f')

    B = zeros((NbVE, NbHE), dtype=np.uint8)

    # Création des N trames
    for k in range(N):
        # trame d'ordre k
        IE = 1 * ((sin(vE * 2**(k + 1) * pi / NbHE)) < 0)  # Expression mathématique
        r = 255 * IE
        g = 0 * IE
        b = 0 * IE

        B = np.dstack((r, g, b))
        B = uint8(B)
        # enregistrement
        A = 'Trame' + str(k+1) + '.bmp'
        io.imsave(A, B)

        # Emit the callback with the current frame
        progress_callback.emit((k+1) * 100 / N)
    

    progress_callback.emit(100)

    print(time.process_time() - start_time, "seconds")  # fin mesure temps d'éxecusion
