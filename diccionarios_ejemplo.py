# get(): Devuelve el valor que corresponde con la key introducida.
print(diccionario.get('Piloto 1'))


# pop(): Devuelve el valor que corresponde con la key introducida, y luego borra la key y el valor.
print(diccionario.pop('Piloto 1'))
print(diccionario)

# update(): Actualiza el valor de una determinada key o lo crea si no existe.
diccionario.update({'Piloto 4':'Lewis Hamilton'})
diccionario.update({'Piloto 2':'Sebastian Vettel'})
print(diccionario)

# "key" in diccionario: devuelve verdadero (True) o falso (False) si la key existe en el diccionario.
print ("Piloto 1" in diccionario)
print ("piloto 1" in diccionario)
print ("Sebastian Vettel" in diccionario)


# "definición" in diccionario.values(): devuelve verdadero (True) o falso (False) si la definición existe en el diccionario.
print ("Sebastian Vettel" in diccionario.values())


# del diccionario['key']: Elimina el valor (y el key) asociado a la key indicada.
#del diccionario['Piloto 2']
print(diccionario)
