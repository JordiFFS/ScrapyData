import spacy

# Cargar el modelo en español de Spacy
nlp = spacy.load("es_core_news_sm") #Idioma español, analisis gramatical, reconocimiento de palabras por tipo (part-of-speech tagging, POS)

textos = [
    "estoy corriendo hacia la selva",
    "vamos en camino por la ciudad cantando y riendo todo el tiempo",
    "si cantar y correr seria un ejercicio sería el primero en ganar batallas",
    "la ganancia es el primer principio de correr hacia la meta",
    "ganar es ganar, la ganancia",
    "estamos ganando el semestre, de la ganancia del conocimiento"
]

verbos = {}  #Almacena la información verbos

# Procesar cada texto
for texto in textos:
    # Analizar el texto utilizando Spacy
    doc = nlp(texto)

    # Contar los verbos en el texto
    for token in doc: #Filtra las palabras que se identifican como verbo (POS tag "VERB")
        if token.pos_ == 'VERB':
            verbo = token.lemma_ #Obtiene la forma base del verbo
            verbos[verbo] = verbos.get(verbo, 0) + 1 #Conteo de verbos, si el verbo no existe inicia con 0

# Imprimir los resultados
for verbo, cantidad in verbos.items():
    print(f"{verbo} = {cantidad}")
