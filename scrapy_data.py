import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

print('*** Sistema para descargar datos de tablas en HTML ***')
url = input('Ingrese la URL de la página que desea scrapear. ')
numero_tabla = int(input('¿A qué tabla del HTML quiere extraer la información? '))
#cantidad = int(input('Ingrese la cantidad de datos que desea descargar. '))

print('<------------------------------------------------------->')


# Función para convertir una lista en elementos de un DataFrame de pandas
def rowsToDataFrame(rows):
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


# Función para extraer los datos de una tabla HTML
def processTableData(tbl):
    rows = []
    for tr in tbl.find('tbody').find_all('tr'):  # Itera los elementos internos de la tabla (<tr>).
        row = []
        for cell in tr.find_all(['td', 'th']):  # Consulta en cada celda si es <td> o <th>.
            item = cell.get_text(
                strip=True)  # Extrae el texto ignorando las demás etiquetas (por ejemplo, <b>), y también los espacios.
            row.append(item)  # Añade el contenido extraído a la lista row.
        if row:
            rows.append(row)  # Si row tiene información, la añade a la lista de rows.
    return rows


# Función para extraer los datos de una URL y procesar el contenido HTML
def processDataHTML(data):
    soup = bs(data, 'html.parser')  # Estructura el HTML que está en formato de cadena (string).
    tbl = soup.find_all('table')[numero_tabla - 1]  # Recupera la tabla del HTML.
    tblRows = processTableData(tbl)  # Ejecución del procesamiento de la función para el contenido de la tabla
    return tblRows


# Leer el sitio web.
# Declarar req para hacer la consulta: requests.get('URL').
req = requests.get(url)
dominio = url.split("//")[1].split("/")[0].replace(".", "-")

"""
url.split("//") divide la url en dos partes si url = "https://ejemplo.com/path" el resultado sera
["https:", "ejemplo.com/path"] 
[1] Toma el segundo elemento de la lista generada en este caso "ejemplo.com/path"
.split("/") divide el string anterior por el carácter "/" con el ejemplo ["ejemplo.com", "path"]
[0] selecciona el primer elemento de la lista "ejmplo.com"
.replace reemplza todos los "." que ecuentre y los cambio por "-" en el ejemplo quedaria asi "ejemplo-com"

url.split("//") → ["https:", "www.ejemplo.com/path"]
[1] → "www.ejemplo.com/path"
.split("/") → ["www.ejemplo.com", "path"]
[0] → "www.ejemplo.com"
.replace(".", "-") → "www-ejemplo-com"
"""


if req.status_code != 200:
    print(f'Error al acceder a la pagina: {req.status_code}')
    exit()

HTML = req.text  # Si se trabaja con content, devuelve un byte. Por eso, se utiliza .text para convertirlo a una cadena (string).
# Si se requiere un JSON, se utiliza .json().
table = processDataHTML(HTML)  # No se usa .json() aquí, ya que el contenido es texto HTML.
df = rowsToDataFrame(table)

opcion = input("¿Desea descargar todos los datos o una cantidad específica? (todos/cantidad): ").strip().lower()

if opcion == "cantidad":
    cantidad = int(input(f'Ingrese la cantidad de datos que desea descargar (máximo {len(df)}): '))
    cantidad = min(cantidad, len(df))  # asegura no exeder el numero de datos de la tabla
    df = df.head(cantidad) # Filtrar el DataFrame con los primeros 'cantidad' registros.
elif opcion != 'todos':
    print("Opción no válida. Se descargarán todos los datos.")
else:
    print(f"Descargando los {len(df)} datos disponibles...")

print("DataFrame:\n", df)  # df.head(n) muestra los primeros n registros del DataFrame.
# df.info()
df.to_csv(f'{dominio}.csv', index=False)  # Se genera un archivo CSV donde el índice puede ocultarse o mostrarse:
# True: Oculta el índice.
# False: Muestra el índice.
print(f'Datos guardados en el archivo: {dominio}.csv')
