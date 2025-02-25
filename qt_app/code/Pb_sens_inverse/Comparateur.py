# rotation_Z.py
import numpy as np
from numpy import loadtxt, linspace, sin, cos, pi, array, concatenate, savetxt, meshgrid, isnan
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# --- Chargement des coordonnées de l'objet vu de face ---
# Ces fichiers sont générés par Objet.py.
# On suppose que X.txt, Y.txt et Z.txt contiennent chacun un tableau 1D (les points de l'objet)
X = loadtxt('X.txt').flatten()
Y = loadtxt('Y.txt').flatten()
Z_obj = loadtxt('Z.txt').flatten()  # Z de l'objet vu de face (taille 1280x800 au départ)
X_sim = loadtxt('X2.txt')  # X de l'objet vu de face (taille 1280x800 au départ)
Y_sim = loadtxt('Y2.txt')  # Y de l'objet vu de face (taille 1280x800 au départ
Z_sim = loadtxt('Z2.txt')  # Z de l'objet vu de face (taille 1280x800 au départ

# --- Chargement des paramètres d'orientation ---
# Le fichier angles.txt contient alpha_d et beta_d (en degrés)
alpha_d, beta_d = loadtxt('angles.txt')

# --- Paramètres du récepteur (définis dans le script Images vues par le recepteur) ---
NbHR = 1920    # Nombre de colonnes du CCD
NbVR = 1080    # Nombre de lignes du CCD
zoom = 1500    # On souhaite obtenir 1500 colonnes en sortie

MR = loadtxt('MR.txt')

# Création de la grille de coordonnées matricielles du récepteur
# (uR, vR) correspond à l'ensemble des points du CCD
xx = linspace(0, NbHR-1, NbHR)
yy = linspace(0, NbVR-1, NbVR)
vR, uR = meshgrid(xx, yy)

# --- Application de la projection aux points de l'objet ---
# On calcule les coordonnées projetées (uR1, vR1) pour chaque point de l'objet
sRuR1 = MR[0,0]*X + MR[0,1]*Y + MR[0,2]*Z_obj + MR[0,3]
sRvR1 = MR[1,0]*X + MR[1,1]*Y + MR[1,2]*Z_obj + MR[1,3]
sR    = MR[2,0]*X + MR[2,1]*Y + MR[2,2]*Z_obj + MR[2,3]

uR1 = sRuR1 / sR
vR1 = sRvR1 / sR

# --- Interpolation de la valeur Z sur la grille du récepteur ---
# Ici, on interpole les valeurs de Z_obj (les hauteurs frontales)
# depuis les points (uR1, vR1) sur la grille (uR, vR) définie pour le CCD.
Z_rot = griddata((uR1.flatten(), vR1.flatten()),
                 Z_obj.flatten(),
                 (uR, vR),
                 method='linear')

# Remplacement des NaN par 0 (ou une autre valeur de votre choix)
Z_rot[np.isnan(Z_rot)] = 0

# --- Recadrage pour obtenir une matrice 1500 x 1080 ---
# La grille (uR, vR) est de taille 1080 x 1920.
# On conserve les 1500 premières colonnes pour obtenir 1500 x 1080.
Z_real = Z_rot[:, :zoom]

# Sauvegarde du résultat
savetxt('Z_real.txt', Z_real, fmt='%-7.6f')

# --- Affichage du résultat ---
plt.figure(figsize=(8, 6))
plt.pcolor(Z_real, cmap='gray')
plt.colorbar(label='Z (mm)')
plt.title('Objet réel tourné (Z_real) en 1500x1080')
plt.xlabel('Pixels (horizontal)')
plt.ylabel('Pixels (vertical)')
plt.show()






# Calcul de l'erreur entre la simulation et la réalité
erreur =  Z_real - Z_sim

# Création de la carte de différences
plt.figure(figsize=(8, 6))
plt.pcolor(X_sim, Y_sim, erreur, cmap='OrRd', vmin=-np.nanmax(abs(erreur)), vmax=np.nanmax(abs(erreur)))
plt.colorbar(label="Erreur (mm)")
plt.title("Ecart entre objet simulé et objet mesuré")
plt.xlabel("Xmes (mm)")
plt.ylabel("Ymes (mm)")
plt.savefig("Erreur.png")
plt.show()
