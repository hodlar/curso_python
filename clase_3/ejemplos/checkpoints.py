import matplotlib.pyplot as plt
import random


def darPaso():
    """Selecciona al azar una direccion para moverse"""
    direcciones = [(0,1), (0,-1), (1,0), (-1,0)]
    return random.choice(direcciones)


def llenarMapa(cantidad=1000):
    """Comenzando en la posicion (0,0), da la cantidad de pasos indicada"""
    pasoX = [0]
    pasoY = [0]
    
    for i in range(cantidad):
        # Por cada paso, ejecutamos la funcion darPaso para obtener la direccion a la que nos moveremos
        x, y = darPaso()
        # Asignamos el valor del ultimo paso mas el nuevo a una variable
        nX = pasoX[i]+x
        nY = pasoY[i]+y
        # Anexamos el nuevo valor a la lista de pasos dados
        pasoX.append(nX)
        pasoY.append(nY)
    plt.plot(pasoX, pasoY)
    plt.show()
if __name__ == "__main__":
    llenarMapa()