import pandas as pd
import random

# Cargar los DataFrames
df = pd.read_csv('df_usuarios.csv')
rutas = pd.read_csv('rutas_final.csv')

# Inicializar las columnas
df['ruta'] = [random.randint(0, 16) for _ in df.index]
df['longitud_ruta'] = pd.NA
df['sector'] = pd.NA
df['valoracion'] = [random.randint(1, 5) for _ in df.index]

# Asignar valores a 'longitud_ruta'
for a in df.index:
    ruta_id = df.at[a, 'ruta']
    sector_value = rutas.loc[rutas['id_ruta'] == ruta_id, 'distancia'].values[0]
    df.at[a, 'longitud_ruta'] = str(sector_value)

# Asignar valores a 'sector'
for a in df.index:
    ruta_id = df.at[a, 'ruta']
    sector_value = rutas.loc[rutas['id_ruta'] == ruta_id, 'sectores'].values[0]
    df.at[a, 'sector'] = str(sector_value)

# Guardar el DataFrame modificado
df.to_csv("df_casos.csv", index=False)



