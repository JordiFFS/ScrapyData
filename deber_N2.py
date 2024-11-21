import spacy
import matplotlib.pyplot as plt
import re

nlp = spacy.load("es_core_news_sm")

# Expresión regular para encontrar emojis
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticonos
    "\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
    "\U0001F680-\U0001F6FF"  # Transporte y mapas
    "\U0001F700-\U0001F77F"  # Alquimia
    "\U0001F780-\U0001F7FF"  # Geometría
    "\U0001F800-\U0001F8FF"  # Personas
    "\U0001F900-\U0001F9FF"  # Símbolos varios
    "\U0001FA00-\U0001FA6F"  # Objetos
    "\U0001FA70-\U0001FAFF"  # Lugares y edificios
    "\U00002702-\U000027B0"  # Varios símbolos
    "\U000024C2-\U0001F251"  # Caracteres adicionales
    "]", flags=re.UNICODE
)

print("*** Sistema para analizar texto de páginas web ***")
print('Ingrese el texto que desea analizar puede usar saltos de línea:')
textos = []
while True:
    linea = input()
    if linea:
        textos.append(linea)
    else:
        break  # Cuando se precione enter sin ingresar texto finaliza la entrada

texto_completo = "".join(textos)

print("Texto que se va analizar:\n")
print(texto_completo)  # En consola trae el texto ingresado por el usuario

print("Seleccione el tipo de palabra que desea analizar:")
print("1. NUM (Números)")
print("2. VERB (Verbos)")
print("3. AUX (Auxiliares)")
print("4. NOUN (Sustamtivo)")
print("5. ADP (Adposiciones)")
print("6. # (Hashtags)")
print("7. EMOJIS (Emojis)")
opcion = input("Ingrese el número correspondiente a su elección: ")

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
    case "6":
        etiqueta = "#"
    case "7":
        etiqueta = "emoji"
    case _:
        print("Opción no válida. Terminando el programa.")
        exit()

conteo = {}
for texto in textos:
    doc = nlp(texto)
    if etiqueta == "#":  # Si la opción es para hashtags
        hashtags = re.findall(r'#\w+', texto)  # Buscar hashtags usando expresiones regulares
        for hashtag in hashtags:
            conteo[hashtag] = conteo.get(hashtag, 0) + 1
    elif etiqueta == "emoji":  # Si la opción es para emojis
        emojis = re.findall(emoji_pattern, texto)  # Buscar emojis usando la expresión regular
        for emoji in emojis:
            conteo[emoji] = conteo.get(emoji, 0) + 1
    else:  # Si la opción es para verbos
        for token in doc:
            if token.pos_ == etiqueta:
                palabra = token.lemma_
                conteo[palabra] = conteo.get(palabra, 0) + 1

print(f"\nPalabras de tipo '{etiqueta}' encontradas y su frecuencia:")
for palabra, cantidad in conteo.items():
    print(f"{palabra} = {cantidad}")

conteo_total = sum(conteo.values())
print(f"\nCantidad total de palabras tipo '{etiqueta}' encontradas en el texto: {conteo_total}")

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
