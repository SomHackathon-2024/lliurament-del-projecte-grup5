import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=InconsistentVersionWarning)

from CHATbot import ChatBot
import joblib
import CONST
from CBR_rutas import RecommendationSystem



#Fitxer a executar per a realitzar les recomanacions

if __name__ == "__main__":

    #Preguntes que s'utilitzaran en el chatbot per extreure informació
    

    lista_preguntas = [
        ("edad", "\n¿Qué edad tienes?", [], "Numerica"),
        ("region", "\n¿Desde qué región nos visitas?", CONST.region, "Categorica Simple"),
        ("genero", "\n¿Cuál es tu genero?",CONST.genero, "Categorica Simple"),
        ("vacaciones", "\n¿Qué actividades sueles hacer en tus vacaciones?",CONST.vacaciones, "Categorica Simple"),
        ("mobilidad_reducida", "\n¿Tienes mobilidad reducida o alguna discapacidad?", CONST.mobilidad_reducida, "Categorica Simple"),
        ("tarde_libre", "\n¿Qué te gusta hacer en tus tardes libres?", CONST.tarde_libre, "Categorica Simple"),
        ("trabajo", "\n¿Cuál es tu situación laboral?", CONST.trabajo, "Categorica Simple"),
        ("musica", "\n¿Qué tipo de música sueles escuchar?", CONST.musica, "Categorica Simple"),
        ("longitud_ruta", "\n¿cómo quieres que sea la longitud de tu ruta?", CONST.longitud_ruta, "Categorica Simple"),
        ("sector", "\n¿Qué sector prefieres visitar?", CONST.categorias_rutas, "Categorica Simple"),
        ]

    chat = ChatBot(lista_preguntas)
    
    respuestas = chat.devolver_respuestas()

    #Inicialitzem la classe CBR
    recommendation_system = RecommendationSystem(kmeans_model=joblib.load('./kmeans_model.joblib'), scaler_model=joblib.load('./scaler_model.joblib'), pca_model=joblib.load('./pca_model.joblib'),chatbot=chat)



    response = input("Bienvenido a Explora Mataró, donde tendrás la mejor experiencia interactiva posible. Pulsa Y para continuar:\n\n")

    while response == "Y":
        recommendation_system.recomendation()
        response = input("¿Quieres realizar otra consulta? (Y para continuar, cualquier otra tecla para salir): ")
    
print("¡Gracias por usar Explora Mataró!")
