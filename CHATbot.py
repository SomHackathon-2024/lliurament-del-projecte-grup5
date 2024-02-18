import pandas as pd
import CONST

class ChatBot:
    def __init__(self, preguntas):
        self.preguntas = preguntas
        self.respuestas_df = pd.DataFrame()

    def hacer_preguntas(self):
        for var, pregunta, opciones, tipo in self.preguntas:
            respuesta = self.preguntar(pregunta, opciones, tipo)
            self.respuestas_df.at[0, var] = respuesta

    def preguntar(self, pregunta, opciones, tipo):
        if tipo == "Categorica Simple":
            return self.preguntar_opcion(pregunta, opciones)

        elif tipo == "Categorica Multiple":
            return self.preguntar_opciones_multiples(pregunta, opciones)

        elif tipo == "Numerica":
            return self.preguntar_numerica(pregunta)
        
        elif tipo == "Numerica Especifica":
            return self.preguntar_numerica_opciones(pregunta, opciones)

    def preguntar_opcion(self, pregunta, opciones):
        respuesta = input(pregunta + ". Opciones: " + str(", ".join(opciones)) + ". ")

        while respuesta not in opciones:
            print("Respuesta no válida. Por favor, elige una opción válida.")
            respuesta = input(pregunta + " ")

        return respuesta

    def preguntar_opciones_multiples(self, pregunta, opciones):
        respuesta = input(pregunta + ". Opciones: " + str(", ".join(opciones)) + ". ")

        while any(opcion not in opciones for opcion in respuesta.split(',')):
            print("Respuestas no válidas. Por favor, elige opciones válidas separadas por comas.")
            respuesta = input(pregunta + " ")

        return respuesta

    def preguntar_numerica(self, pregunta):
        while True:
            try:
                respuesta = float(input(pregunta + " "))
                break
            except ValueError:
                print("Respuesta no válida. Por favor, introduce un valor numérico.")

        return respuesta
    
    def preguntar_numerica_opciones(self, pregunta, opciones):
        while True:
            try:
                respuesta = int(input(pregunta + ". Opciones: " + str(", ".join((opciones))) + ". "))
                if str(respuesta) not in opciones:
                    raise ValueError
                break
            except ValueError:
                print("Respuesta no válida. Por favor, introduce un valor numérico de las opciones.")

        return respuesta

    def exportar_respuestas(self, nombre_archivo='respuestas.csv'):
        self.respuestas_df.to_csv(nombre_archivo, index=False)
        

    def devolver_respuestas(self):
        return self.respuestas_df

# Ejemplo de uso:
#chatbot = ChatBot(lista_preguntas)
# chatbot.hacer_preguntas()
# chatbot.exportar_respuestas()
