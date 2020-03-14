#import para 3d
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt

#numero de datos que queremos graficar
#se usa linspace para que incluya el 3
z = np.linspace(-3, 3, 600)

#ecuacion de 2d a graficar (en este caso una recta)
rho = z/z

#vamos a dar pasos de 0 a 2*pi(360degrees)
#se hace el reshape solo para que np.dot funcione bien...
#dado que rho es tu radio a toda altura z, calculamos x,y alrededor del radio y antes necesitamos sabe a que posicionse encuentran del radio para conseguir x,y
revolve_steps = np.linspace(0, np.pi*2, 600).reshape(1,600)


#x=r*cos(theta)
#y=r*sin(theta)
#dado que r es tu rho y theta es revolve_steps
#al usar np.dot hacemos una multiplicacionn de matrices para conseguir un arreglo 2d donde las columnas de los x y y corresponderan a los de z
theta = revolve_steps
#convierte rho en un vector de columna
rho_column = rho.reshape(600,1)
x = rho_column.dot(np.cos(theta))
y = rho_column.dot(np.sin(theta))
#convertimos z en un arreglo 2d que concuerda con las dimensiones de x,y

zs, rs = np.meshgrid(z, rho)


#graficando
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
fig.tight_layout(pad = 0.0)

#transponemos zs, de lo contrario no sale el solido de revolucion
#rstride = int o csrride = int en kwargs conrolan la densidad de la grafica
ax.plot_surface(x, y, zs.T, color = 'white', shade = False)
#orientacion
#view orientation
ax.elev = 30 #30 grados para una vista isometrica
ax.azim = 30
#apaga los ejes
ax.set_axis_off()
plt.show()


ax.set_aspect('equal')
