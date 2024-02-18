from CHATbot import ChatBot
import CONST
import pandas as pd
import joblib
from sklearn.metrics.pairwise import euclidean_distances
from itertools import islice
from Prepro_Cas_Script import case_preprocessing, find_cluster

df_rutas = pd.read_csv('rutas_final.csv')
df_places = pd.read_csv('datos_lugares.csv')
df_usuarios = pd.read_csv('df_usuarios.csv')
df_casos = pd.read_csv('df_casos.csv')




class RecommendationSystem:
    def __init__(self, scaler_model, kmeans_model, pca_model,chatbot):
        self.scaler_model = scaler_model
        self.kmeans_model = kmeans_model
        self.pca_model = pca_model
        self.chatbot = chatbot

    def retrieve(self, case):
        prep_case = case_preprocessing(case)
        n_cluster = find_cluster(prep_case, self.scaler_model, self.kmeans_model, self.pca_model)

        path = './' 
        file_name = f'cluster_{n_cluster}.csv'
        path_name = path + file_name

        cluster = pd.read_csv(path_name)

        return cluster, prep_case

    def calculate_distance(self, cluster_resultante_final, prep_case):
        cluster_resultante_resultante = cluster_resultante_final[cluster_resultante_final['valoracion'] > 3]

        columns = prep_case.columns
        columns_list = ['ruta']

        for col in columns:
            columns_list.append(col)

        cluster_resultante_final = cluster_resultante_resultante[columns_list]

        distancias = euclidean_distances(prep_case, cluster_resultante_final.drop('ruta', axis=1))
        cluster_resultante_final['distancia_usuario'] = distancias.T

        df_rutas_ordenadas = cluster_resultante_final.sort_values(by='distancia_usuario')

        routes = df_rutas_ordenadas['ruta'].value_counts()

        weights = {}
        for i in range(20):
            weights[i] = 0

        points = len(df_rutas_ordenadas)

        for i in range(len(df_rutas_ordenadas)):
            weights[df_rutas_ordenadas['ruta'].iloc[i]] += points
            points -= 1

        for x in range(len(routes)):
            if weights[x] != 0:
                weights[x] = weights[x] * routes[x]

        weights_ordered = {clave: weights[clave] for clave in sorted(weights, key=weights.get, reverse=True)}
        
        return weights_ordered

    def print_results(self, dicc, df_rutas, df_places):
        print("\nEstas son las rutas que mejor se adaptan a tu perfil:")
        i = 1
        for clave, _ in islice(dicc.items(), 5):
            ruta_nombre = df_rutas.loc[df_rutas['id_ruta'] == clave, 'nombre'].values[0]
            lugares = self.get_places(df_rutas,df_places,clave)
            print(f"\n{i}. {ruta_nombre}. La ruta incluye los siguientes puntos de interés:")
            for l in lugares:
                print(f"-{l}")
            i += 1
        
        
    def get_places(self,df_rutas,df_places, clave):
        lugares = df_rutas['lugares_ruta'].iloc[clave].strip('][').split(', ')
        lista_lugares = []
        for x in lugares:
            x = int(x)
            lista_lugares.append(df_places.loc[df_places['Id_sitio'] == x,'nombre'].values[0])
        return lista_lugares
    
    def feedback_retain(self,dicc,df_usuarios,df_casos,df_rutas,respuestas):
        n_ruta = int(input('Seleccione una de las 5 rutas(1-5:'))
        claves_lista = list(dicc.keys())
        route = claves_lista[n_ruta-1]
        n_user = len(df_usuarios)
        feedback = int(input('¿Qué le ha parecido la ruta? Agradeceriamos si pudieras puntuarla entre 1 y 5 para el mejor desarroyo de la aplicación:'))
        resp = respuestas.copy()
        new_user = [n_user,resp['genero'],resp['edad'],resp['region'],resp['trabajo'],resp['musica'],resp['tarde_libre'],resp['vacaciones'],resp['mobilidad_reducida']]
        df_usuarios.loc[len(df_usuarios)] = new_user
        long = df_rutas.loc[df_rutas['id_ruta'] == route,'distancia'].values[0]
        sec = df_rutas.loc[df_rutas['id_ruta'] == route,'sectores'].values[0]
        new_case = [n_user,resp['genero'],resp['edad'],resp['region'],resp['trabajo'],resp['musica'],resp['tarde_libre'],resp['vacaciones'],resp['mobilidad_reducida'],route,long,sec,feedback]
        df_casos.loc[len(df_casos)] = new_case
        df_usuarios.to_csv('df_usuarios.csv', index=False)
        df_casos.to_csv('df_casos.csv', index=False) 

        
        return
        
            
    def recomendation(self):
        """
        Recomendació del CBR
        """
        #CHATBOT
        self.chatbot.hacer_preguntas()

        self.case = self.chatbot.devolver_respuestas()

        cluster, prep_case = self.retrieve(self.case)

        w = self.calculate_distance(cluster,prep_case)

        self.print_results(w,df_rutas,df_places)
        
        self.feedback_retain(w,df_usuarios,df_casos,df_rutas,self.case)
        
        

        
        print("\n¡Gracias por confiar en nosotros y gracias por el feedback! Hasta otra.")


