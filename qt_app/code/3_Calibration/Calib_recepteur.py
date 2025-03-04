import time
import numpy as np
import scipy.optimize


## Calcul de MRNmes
#------------------------------
#------------------------------
start_time = time.process_time()  # début mesure temps d'exécution

X = [-497.5, -497.5, -497.5, 0, 0, 0, 497.5, 497.5, 497.5, -497.5, -497.5, -497.5, 0, 0, 0, 497.5, 497.5, 497.5]
Y = [234, 0, -234, 311, 0, -311, 234, 0, -234, 234, 0, -234, 311, 0, -311, 234, 0, -234]
Z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100]


Pt_calib = np.array([
    X,
    Y,
    Z
])


Pt_aqui_pixel = np.array([
    [165, 539, 913, 120, 539, 967, 257, 539, 822, 127, 539, 951, 85, 539, 1005, 236, 539, 843],
    [209, 209, 209, 959, 959, 959, 1517, 1517, 1517, 195, 195, 195, 1010, 1010, 1010, 1603, 1603, 1603]
])


Pt_aqui_mm = Pt_aqui_pixel


n = 18
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
print(M)


M_temp=[M[0][0],M[1][0],M[2][0],M[3][0],M[4][0],M[5][0],M[6][0],M[7][0],M[8][0],M[9][0],M[10][0]]


MRNmes=np.array([
    [M_temp[0],M_temp[1],M_temp[2],M_temp[3]],
    [M_temp[4],M_temp[5],M_temp[6],M_temp[7]],
    [M_temp[8],M_temp[9],M_temp[10],1]
])


print("MRNmes",MRNmes)
np.savetxt('MRNmes.txt',MRNmes, fmt='%.20f')

end_time = time.process_time()  # fin mesure temps d'exécution
print(f"Temps d'exécution: {end_time - start_time} secondes")


## Calcul des autres paramètres
#------------------------------
#------------------------------

start_time = time.process_time()  # début mesure temps d'exécution

MRmes=1210.656*MRNmes
np.savetxt('MRmes.txt',MRmes, fmt='%.20f')

M1=np.array([MRmes[0][0],MRmes[0][1],MRmes[0][2]])
M2=np.array([MRmes[1][0],MRmes[1][1],MRmes[1][2]])
M3=np.array([MRmes[2][0],MRmes[2][1],MRmes[2][2]])
m14=MRmes[0][3]
m24=MRmes[1][3]
m34=MRmes[2][3]

u0Rmes=np.dot(M1,M3)
v0Rmes=np.dot(M2,M3)

alphaURmes=-np.linalg.norm(np.cross(M1,M3))
alphaVRmes=np.linalg.norm(np.cross(M2,M3))

r1=(M1-u0Rmes*M3)/alphaURmes
r2=(M2-v0Rmes*M3)/alphaVRmes
r3=M3

r1=np.reshape(r1,(1,3))
r2=np.reshape(r2,(1,3))
r3=np.reshape(r3,(1,3))

rrmes=np.concatenate((r1,r2,r3),axis=0)

t1Rmes=(m14-u0Rmes*m34)/alphaURmes
t2Rmes=(m24-v0Rmes*m34)/alphaVRmes
t3Rmes=m34


np.savetxt('u0Rmes.txt', np.array([u0Rmes]), fmt='%.20f')
np.savetxt('v0Rmes.txt', np.array([v0Rmes]), fmt='%.20f')
np.savetxt('alphaURmes.txt', np.array([alphaURmes]), fmt='%.20f')
np.savetxt('alphaVRmes.txt', np.array([alphaVRmes]), fmt='%.20f')
np.savetxt('rrmes.txt', np.array(rrmes), fmt='%.20f')
np.savetxt('t1Rmes.txt', np.array([t1Rmes]), fmt='%.20f')
np.savetxt('t2Rmes.txt', np.array([t2Rmes]), fmt='%.20f')
np.savetxt('t3Rmes.txt', np.array([t3Rmes]), fmt='%.20f')


end_time = time.process_time()  # fin mesure temps d'exéc
print(f"Temps d'exécution: {end_time - start_time} secondes")


## Calcul des angles phimes, thetames, psimes
#------------------------------
#------------------------------

start_time = time.process_time()  # début mesure temps d'exécution

def RRphithetapsi(phimes, thetames, psimes):
    return np.array([
    [np.cos(phimes)*np.cos(thetames), np.cos(phimes)*np.sin(thetames)*np.sin(psimes)-np.sin(phimes)*np.cos(psimes), np.cos(phimes)*np.sin(thetames)*np.cos(psimes)+np.sin(phimes)*np.sin(psimes)],
    [np.sin(phimes)*np.cos(thetames), np.sin(phimes)*np.sin(thetames)*np.sin(psimes)+np.cos(phimes)*np.cos(psimes), np.sin(phimes)*np.sin(thetames)*np.cos(psimes)-np.cos(phimes)*np.sin(psimes)],
    [-np.sin(thetames), np.cos(thetames)*np.sin(psimes), np.cos(thetames)*np.cos(psimes)]
])

def f(x):
    return np.linalg.norm(RRphithetapsi(x[0],x[1],x[2])-rrmes)

angles=(scipy.optimize.fmin(f, [-np.pi/2, -np.pi, 0]))
print(angles*180/np.pi)

end_time = time.process_time()  # fin mesure temps d'exéc
print(f"Temps d'exécution: {end_time - start_time} secondes")


