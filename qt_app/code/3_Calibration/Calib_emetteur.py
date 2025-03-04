import time
start_time = time.process_time()  # début mesure temps d'exécution
import numpy as np
from numpy import savetxt, loadtxt
import scipy.optimize


MRNmes = loadtxt('MRNmes.txt')

## Calcul de MENmes
#------------------------------
#------------------------------


Pt_calib_recep_pixel = np.array([
    [200, 540, 882, 242, 540, 838, 276, 540, 805, 302, 540, 778, 201, 540, 879, 244, 540, 836, 277, 540, 803, 304, 540, 777],
    [596, 596, 596, 960, 960, 960, 1242, 1242, 1242, 1466, 1466, 1466, 707, 707, 707, 1062, 1062, 1062, 1335, 1335, 1335, 1554, 1554, 1554],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
])

Pt_aqui_pixel= np.array([
    [100,400,700,100,400,700,100,400,700,100,400,700,100,400,700,100,400,700,100,400,700,100,400,700],
    [320,320,320,640,640,640,960,960,960,1280,1280,1280,320,320,320,640,640,640,960,960,960,1280,1280,1280]
])

n = 24

Pt_calib_XY = []

for j in range(n):
    Vj=[[],[]]
    Vj[0] = [MRNmes[2][0]*Pt_calib_recep_pixel[0][j]-MRNmes[0][0], MRNmes[2][1]*Pt_calib_recep_pixel[0][j]-MRNmes[0][1]]
    Vj[1] = [MRNmes[2][0]*Pt_calib_recep_pixel[1][j]-MRNmes[1][0], MRNmes[2][1]*Pt_calib_recep_pixel[1][j]-MRNmes[1][1]]
    Vj=np.array(Vj)
    ##print(Vj)
    Wj=[0,0]
    Wj[0] = (MRNmes[0][2] - MRNmes[2][2] * Pt_calib_recep_pixel[0][j]) * Pt_calib_recep_pixel[2][j] - MRNmes[2][3] * Pt_calib_recep_pixel[0][j] + MRNmes[0][3]
    Wj[1] = (MRNmes[1][2] - MRNmes[2][2] * Pt_calib_recep_pixel[1][j]) * Pt_calib_recep_pixel[2][j] - MRNmes[2][3] * Pt_calib_recep_pixel[1][j] + MRNmes[1][3]
    Wj=np.array(Wj)
    ##print(Wj)
    Pt_calib_XY.append(np.linalg.inv(Vj) @Wj)


print("Pt_calib_XY:", Pt_calib_XY)


Pt_calib = [[], [], []]

for j in range(n):
    Pt_calib[0].append(Pt_calib_XY[j][0])
    Pt_calib[1].append(Pt_calib_XY[j][1])
    if j < 12:
        Pt_calib[2].append(0)
    else:
        Pt_calib[2].append(100)

print(Pt_calib)

Pt_calib = np.array(Pt_calib)

A = np.zeros((2*n, 11))

for i in range(2*n):
    for j in range(3):
        if i % 2 == 0:
            A[i][j] = Pt_calib[j][i // 2]
            A[i][3] = 1
        else:
            A[i][j + 4] = Pt_calib[j][(i - 1) // 2]
            A[i][7] = 1

for i in range(2*n):
    for j in range(3):
        if i % 2 == 0:
            A[i][j + 8] = -Pt_aqui_pixel[0][i // 2] * Pt_calib[j][i // 2]
        else:
            A[i][j + 8] = -Pt_aqui_pixel[1][(i - 1) // 2] * Pt_calib[j][(i - 1) // 2]

B = np.zeros((2*n, 1))
for i in range(2*n):
    if i % 2 == 0:
        B[i] = Pt_aqui_pixel[0][i // 2]
    else:
        B[i] = Pt_aqui_pixel[1][(i - 1) // 2]

M, residuals, rank, s = np.linalg.lstsq(A, B, rcond=None)

M_temp=[M[0][0],M[1][0],M[2][0],M[3][0],M[4][0],M[5][0],M[6][0],M[7][0],M[8][0],M[9][0],M[10][0]]

MENmes = np.array([
    [M_temp[0], M_temp[1], M_temp[2], M_temp[3]],
    [M_temp[4], M_temp[5], M_temp[6], M_temp[7]],
    [M_temp[8], M_temp[9], M_temp[10], 1]
])

print(MENmes)

end_time = time.process_time()  # fin mesure temps d'exécution
print(f"Temps d'exécution: {end_time - start_time} secondes")

## Calcul des autres paramètres
#------------------------------
#------------------------------

start_time = time.process_time()  # début mesure temps d'exécution

MEmes=1472.3*MENmes
np.savetxt('MEmes.txt',MEmes, fmt='%.20f')

M1=np.array([MEmes[0][0],MEmes[0][1],MEmes[0][2]])
M2=np.array([MEmes[1][0],MEmes[1][1],MEmes[1][2]])
M3=np.array([MEmes[2][0],MEmes[2][1],MEmes[2][2]])
m14=MEmes[0][3]
m24=MEmes[1][3]
m34=MEmes[2][3]


u0Emes=np.dot(M1,M3)
v0Emes=np.dot(M2,M3)


alphaUEmes=-np.linalg.norm(np.cross(M1,M3))
alphaVEmes=np.linalg.norm(np.cross(M2,M3))


r1=(M1-u0Emes*M3)/alphaUEmes
r2=(M2-v0Emes*M3)/alphaVEmes
r3=M3


r1=np.reshape(r1,(1,3))
r2=np.reshape(r2,(1,3))
r3=np.reshape(r3,(1,3))


rEmes=np.concatenate((r1,r2,r3),axis=0)


t1Emes=(m14-u0Emes*m34)/alphaUEmes
t2Emes=(m24-v0Emes*m34)/alphaVEmes
t3Emes=m34


np.savetxt('u0Emes.txt', np.array([u0Emes]), fmt='%.15f')
np.savetxt('v0Emes.txt', np.array([v0Emes]), fmt='%.15f')
np.savetxt('alphaUEmes.txt', np.array([alphaUEmes]), fmt='%.15f')
np.savetxt('alphaVEmes.txt', np.array([alphaVEmes]), fmt='%.15f')
np.savetxt('rEmes.txt', np.array(rEmes), fmt='%.15f')
np.savetxt('t1Emes.txt', np.array([t1Emes]), fmt='%.15f')
np.savetxt('t2Emes.txt', np.array([t2Emes]), fmt='%.15f')
np.savetxt('t3Emes.txt', np.array([t3Emes]), fmt='%.15f')


end_time = time.process_time()  # fin mesure temps d'exéc
print(f"Temps d'exécution: {end_time - start_time} secondes")



## Calcul des angles phimes, thetames, psimes
#------------------------------
#------------------------------

start_time = time.process_time()  # début mesure temps d'exécution

def REphithetapsi(phimes, thetames, psimes):
    return np.array([
    [np.cos(phimes)*np.cos(thetames), np.cos(phimes)*np.sin(thetames)*np.sin(psimes)-np.sin(phimes)*np.cos(psimes), np.cos(phimes)*np.sin(thetames)*np.cos(psimes)+np.sin(phimes)*np.sin(psimes)],
    [np.sin(phimes)*np.cos(thetames), np.sin(phimes)*np.sin(thetames)*np.sin(psimes)+np.cos(phimes)*np.cos(psimes), np.sin(phimes)*np.sin(thetames)*np.cos(psimes)-np.cos(phimes)*np.sin(psimes)],
    [-np.sin(thetames), np.cos(thetames)*np.sin(psimes), np.cos(thetames)*np.cos(psimes)]
])

def f(x):
    return np.linalg.norm(REphithetapsi(x[0],x[1],x[2])-rEmes)

angles=(scipy.optimize.fmin(f, [-np.pi/2, np.pi, 0]))
print(angles*180/np.pi)

end_time = time.process_time()  # fin mesure temps d'exéc
print(f"Temps d'exécution: {end_time - start_time} secondes")