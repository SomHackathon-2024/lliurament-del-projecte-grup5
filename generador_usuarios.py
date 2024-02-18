import pandas as pd
import random

random.seed(33)

genero = ['hombre', 'mujer', 'prefiero no decirlo']
edad = ['niño','joven', 'adulto']
continent = ['europe', 'asia', 'oceania', 'africa', 'north america', 'south america']
musica = ['pop', 'techno', 'reggeaton','clasica','rap','heavy metal']
tarde_libre = ['bar', 'playa', 'montaña', 'sofa']
trabajo = ['nada', 'estudiante', 'trabajador', 'jubilado']
vacaciones = ['ocio', 'cultura', 'aventura']
mobilidad_reducida = ['no', 'si']

atributos = ['usuario', 'genero','edad', 'region', 'trabajo', 'musica', 'tarde_libre', 'vacaciones', 'mobilidad_reducida']

def genero_usuario(genero):
    pesos =  [0.45,0.45,0.1]
    g = random.choices(genero, weights=pesos, k=1)[0]  
    return g

def cont(continent):
    pesos =  [0.55,0.15,0.05,0.05,0.1,0.1]
    ct = random.choices(continent, weights=pesos, k=1)[0] 
    return ct

def ed(edad):
    pesos =  [0.1,0.25,0.65]
    e = random.choices(edad, weights=pesos, k=1)[0]
    return e 
    

def mob_reducida(mobilidad_reducida,e):
    if e == 'joven':
        pesos =  [0.95,0.05]
        m = random.choices(mobilidad_reducida, weights=pesos, k=1)[0] 
    elif e == 'niño':
        pesos =  [0.98,0.02]
        m = random.choices(mobilidad_reducida, weights=pesos, k=1)[0] 
    else:
        pesos =  [0.8,0.2]
        m = random.choices(mobilidad_reducida, weights=pesos, k=1)[0]
    return m

def tard_libr(tarde_libre, e):
    if e == 'niño':
        pesos = [0,0.4,0.2,0.2]
        t_l = random.choices(tarde_libre, weights=pesos, k=1)[0]
    else:
        t_l = random.choices(tarde_libre)[0]
        
    return t_l
    

def trabajo_usuario(trabajo, e):
    if e == 'joven':
        pesos =  [0.1,0.7,0.2,0]
        tr = random.choices(trabajo, weights=pesos, k=1)[0] 
    elif e == 'niño':
        pesos =  [0,1,0,0]
        tr = random.choices(trabajo, weights=pesos, k=1)[0]
    else:
        pesos =  [0.1,0.05,0.65,0.2]
        tr = random.choices(trabajo, weights=pesos, k=1)[0] 
    return tr



def musica_usuario(musica, g,e):
    if g == 'hombre':
        if e == 'joven':
            pesos =  [0.1,0.2,0.3,0.05,0.25,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        elif e == 'niño':
            pesos =  [0.3,0.2,0.2,0.05,0.2,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        else:
            pesos =  [0.2,0.1,0.1,0.25,0.1,0.25]
            m = random.choices(musica, weights=pesos, k=1)[0] 
    elif g == 'mujer':
        if e == 'joven':
            pesos =  [0.4,0.15,0.3,0.05,0.05,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        elif e == 'niño':
            pesos =  [0.3,0.2,0.2,0.05,0.2,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0]
        else:
            pesos =  [0.35,0.15,0.05,0.35,0.05,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0] 
    else:
        if e == 'joven':
            pesos =  [0.2,0.25,0.25,0.05,0.15,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 
        elif e == 'niño':
            pesos =  [0.3,0.2,0.2,0.05,0.2,0.05]
            m = random.choices(musica, weights=pesos, k=1)[0]
        else:
            pesos = [0.2,0.25,0.25,0.05,0.15,0.1]
            m = random.choices(musica, weights=pesos, k=1)[0] 

    return m


df = pd.DataFrame(columns=atributos)

datos_usuario = {}
for atr in atributos:
    datos_usuario[atr] = None
for n in range(500):
    lista = []
    g = genero_usuario(genero)
    e = ed(edad)
    r = cont(continent)
    tr = trabajo_usuario(trabajo,e)
    m = musica_usuario(musica,g,e)
    t_l = tard_libr(tarde_libre,e) 
    v = random.choices(vacaciones)[0] 
    m_r = mob_reducida(mobilidad_reducida,e)
    lista.extend([n,g,e,r,tr,m,t_l,v,m_r])

    for i in range(len(lista)):
        datos_usuario[atributos[i]] = lista[i]
    df = pd.concat([df, pd.DataFrame([datos_usuario])], ignore_index=True)

df.to_csv("df_usuarios.csv", index=False)
