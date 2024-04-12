# Importación de bibliotecas necesarias
import nltk  # Biblioteca de procesamiento de lenguaje natural
from nltk.stem import WordNetLemmatizer  # Para lematizar palabras
from nltk.corpus import stopwords  # Lista de palabras vacías (stopwords)
from translate import Translator  # Para traducción de texto
from collections import defaultdict  # Para manejar diccionarios
import pandas as pd  # Biblioteca para manipulación de datos
import re  # Módulo para expresiones regulares

# Descargar recursos adicionales de NLTK (solo necesario la primera vez)
nltk.download('punkt')  # Tokenizador de NLTK
nltk.download('wordnet')  # Diccionario de lematización de NLTK
nltk.download('stopwords')  # Lista de stopwords de NLTK en español

# Configuración de la traducción
translator = Translator(to_lang="es")  # Traductor a español
stop_words_es = set(stopwords.words('spanish'))  # Lista de stopwords en español
lemmatizer = WordNetLemmatizer()  # Lematizador de palabras en inglés

# Lectura de datos desde el archivo CSV
df = pd.read_csv('MBTI 500.csv')

# Lista de preguntas para el usuario
questions = [
    # Organización vs. Flexibilidad
    "¿Prefieres seguir un plan establecido y organizado o mantener la flexibilidad para adaptarte a lo inesperado?",
    "¿Te sientes más cómodo con tareas que tienen un inicio, un desarrollo y un final claros, o te gusta la libertad de explorar y trabajar en diferentes proyectos de forma simultánea?",
    "¿Te cuesta trabajo improvisar o prefieres la espontaneidad y la fluidez en tu día a día?",
]

# Función para preprocesar texto (tokenización, lematización y eliminación de stopwords)
def preprocess_text(text, stop_words):
    tokens = nltk.word_tokenize(text.lower())  # Tokenización del texto
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]  # Eliminación de stopwords y símbolos
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]  # Lematización de palabras
    return ' '.join(lemmatized_tokens)  # Unir tokens lematizados en un texto procesado

# Función para traducir respuestas del usuario
def translate_responses(responses):
    translated_responses = []
    for response in responses:
        try:
            translated_response = translator.translate(response)  # Traducción de la respuesta
            if isinstance(translated_response, str):
                translated_responses.append(translated_response)  # Agregar traducción a la lista de respuestas traducidas
            else:
                translated_responses.append(translated_response.text)
        except Exception as e:
            print(f"Error translating response: {e}")  # Manejo de errores en la traducción
    return translated_responses  # Devolver lista de respuestas traducidas

# Función para verificar coincidencias en mensajes preprocesados
def check_all_messages(messages):
    matches = defaultdict(int)  # Diccionario para contar coincidencias por tipo de personalidad
    total_matches = 0  # Contador total de coincidencias
    preprocessed_messages = [preprocess_text(message, stop_words_es) for message in messages]  # Preprocesamiento de mensajes del usuario
    for index, row in df.iterrows():  # Iteración sobre filas del DataFrame
        count = 0  # Contador de coincidencias por mensaje
        preprocessed_posts = preprocess_text(row['posts'], stop_words_es)  # Preprocesamiento de mensajes del DataFrame
        for preprocessed_message in preprocessed_messages:  # Iteración sobre mensajes del usuario preprocesados
            if re.search(preprocessed_message, preprocessed_posts):  # Búsqueda de coincidencias utilizando expresiones regulares
                count += 1  # Incrementar contador de coincidencias
        if count > 0:  # Si se encontraron coincidencias
            total_matches += count  # Sumar al contador total de coincidencias
            matches[row['type']] += count  # Incrementar contador de coincidencias por tipo de personalidad

    if total_matches > 0:  # Si se encontraron coincidencias totales
        scores = {personality: count / total_matches for personality, count in matches.items()}  # Calcular puntajes de personalidad
        max_score_type = max(scores, key=scores.get)  # Obtener tipo de personalidad con puntaje máximo
        return f'Bot: La personalidad más probable es {max_score_type} con un puntaje de {scores[max_score_type]:.2f}'  # Devolver resultado de personalidad más probable
    else:  # Si no se encontraron coincidencias
        return 'Bot: No se ha encontrado un tipo de personalidad.'  # Devolver mensaje de no encontrado

# Función para obtener respuestas del usuario a las preguntas
def get_responses():
    user_responses = []  # Lista para almacenar respuestas del usuario
    for question in questions:  # Iterar sobre preguntas
        print('Bot:', question)  # Imprimir pregunta del bot
        user_input = input('You: ')  # Obtener respuesta del usuario
        user_responses.append(user_input)  # Agregar respuesta a la lista
    return user_responses  # Devolver lista de respuestas del usuario

# Función para determinar el tipo de personalidad del usuario
def get_response_type(user_responses):
    translated_responses = translate_responses(user_responses)  # Traducir respuestas del usuario
    return check_all_messages(translated_responses)  # Verificar coincidencias y determinar tipo de personalidad

# Obtener respuestas del usuario
user_responses = get_responses()
# Determinar tipo de personalidad del usuario y mostrar resultado
result = get_response_type(user_responses)
print(result)  # Imprimir resultado
