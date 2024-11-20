import requests
from bs4 import BeautifulSoup as bs
import spacy
import matplotlib.pyplot as plt

# Cargar el modelo en español de SpaCy
nlp = spacy.load("es_core_news_sm")

print("*** Sistema para analizar texto de páginas web ***")
url = input('Ingrese la URL de la página que contiene el texto para analizarlo: ')

print('<------------------------------------------------------->')

# Leer el sitio web
req = requests.get(url)

if req.status_code != 200:
    print(f'Error al acceder a la página: {req.status_code}')
    exit()

# Convierte el contenido HTML en texto
HTML = req.text #Convierte el contenido HTML en texto
soup = bs(HTML, 'html.parser')  # Estructura el HTML
texto = soup.get_text(separator=' ', strip=True)  #Extrae todo el texto separado por espacios

# Imprimir el texto extraído
print("Texto extraído de la página:\n")
print(texto) #En consola trae en texto el html

print("\nAnalizando el texto...\n") #Analizando los datos

# Solicitar el tipo de dato que se desea analizar
print("Seleccione el tipo de palabra que desea analizar:")
print("1. NUM (Números)")
print("2. VERB (Verbos)")
print("3. AUX (Auxiliares)")
print("4. NOUN (Sustamtivo)")
print("5. ADP (Adposiciones)")
opcion = input("Ingrese el número correspondiente a su elección: ")

# Mapear la elección a la etiqueta de SpaCy
etiqueta = None
match opcion:
    case "1":
        etiqueta = "NUM"
    case "2":
        etiqueta = "VERB"
    case "3":
        etiqueta = "AUX"
    case "4":
        etiqueta = "DET"
    case "5":
        etiqueta = "ADP"
    case _:
        print("Opción no válida. Terminando el programa.")
        exit()

# Contar las palabras del tipo seleccionado
conteo = {}

doc = nlp(texto)
for token in doc:
    if token.pos_ == etiqueta:
        palabra = token.lemma_
        conteo[palabra] = conteo.get(palabra, 0) + 1

# Mostrar los resultados
print(f"\nPalabras de tipo '{etiqueta}' encontradas y su frecuencia:")
for palabra, cantidad in conteo.items():
    print(f"{palabra} = {cantidad}")

conteo_total = sum(conteo.values())
print(f"\nCantidad total de palabras tipo '{etiqueta}' encontradas en el texto: {conteo_total}")

# Crear un gráfico de barras con las palabras más frecuentes
if conteo:
    palabras_ordenadas = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    # Seleccionar las palabras más frecuentes
    top_palabras = palabras_ordenadas[:10]
    palabras = [item[0] for item in top_palabras]
    frecuencias = [item[1] for item in top_palabras]

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.barh(palabras, frecuencias, color='skyblue')
    plt.xlabel('Frecuencia')
    plt.ylabel('Palabras')
    plt.title(f'Top 10 palabras tipo {etiqueta} más frecuentes')
    plt.gca().invert_yaxis()  # Invertir el eje para mostrar la más frecuente arriba
    plt.tight_layout()
    plt.show()
else:
    print(f"No se encontraron palabras del tipo '{etiqueta}' en el texto.")