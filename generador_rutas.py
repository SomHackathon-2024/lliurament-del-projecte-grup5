import pandas as pd
import random

random.seed(33)



sector = ['ocio', 'cultura', 'deporte', 'comercio_local', 'gastronomia', 'natura', 'educacion', 'bienestar']


atributos = ['id', 'longitud_ruta','sector']

df = pd.DataFrame(columns=atributos)


datos_rutas = {}
for atr in atributos:
    datos_rutas[atr] = None
for n in range(20):
    lista = []
    l = round(random.uniform(500, 10000),2)
    if l < 2000:
        l = 'corta'
    elif l > 7000:
        l = 'larga'
    else:
        l = 'media'
    s = random.choices(sector)[0] 

    lista.extend([n,l,s])

    for i in range(len(lista)):
        datos_rutas[atributos[i]] = lista[i]
    df = pd.concat([df, pd.DataFrame([datos_rutas])], ignore_index=True)

df.to_csv("df_rutas.csv", index=False)