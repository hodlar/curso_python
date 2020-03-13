import matplotlib.pyplot as plt
import random
def darPaso(iteracion=0):
    paso = (random.randint(-1,1), random.randint(-1,1))
    if paso == (0,0):
        return darPaso()
    return paso
def llenarMapa(cantidad):
    pasos = [(0,0)]
    pasoX = [0]
    pasoY = [0]

    for i in range(cantidad):
        x, y = darPaso()
        nX = pasoX[i]+x
        nY = pasoY[i]+y
        pasoX.append(nX)
        pasoY.append(nY)
        pasos.append((nX,nY))
    plt.plot(pasoX, pasoY)
    plt.show()
for _ in range(1):
    llenarMapa(100)