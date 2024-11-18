import requests #La librería request es una librería de Python que permite hacer peticiones HTTP
import pandas as pd #Pandas está diseñada específicamente para la manipulación y el análisis de datos en el lenguaje
from bs4 import BeautifulSoup as bs #sirve para extraer datos de archivos html

print('*** Sistema para descargar datos de tablas en HTML ***')
url = input('Ingrese la URL de la página que desea scrapear: ')
numero_tabla = int(input('¿A qué tabla del HTML quiere extraer la información? (Número entero): '))

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
            item = cell.get_text(strip=True)  # Extrae el texto ignorando etiquetas adicionales.
            row.append(item)  # Añade el contenido extraído a la lista row.
        if row:
            rows.append(row)  # Si row tiene información, la añade a la lista de rows.
    return rows


# Función para extraer los datos de una URL y procesar el contenido HTML
def processDataHTML(data):
    soup = bs(data, 'html.parser')  # Estructura el HTML.
    tbl = soup.find_all('table')[numero_tabla - 1]  # Recupera la tabla del HTML.
    tblRows = processTableData(tbl)  # Procesa la tabla.
    return tblRows


# Leer el sitio web
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
    print(f'Error al acceder a la página: {req.status_code}')
    exit()

HTML = req.text  # Convierte el contenido HTML en texto.
table = processDataHTML(HTML)  # Procesa los datos de la tabla.
df = rowsToDataFrame(table)

# Solicitar al usuario si desea descargar todos los datos o una cantidad específica
opcion = input('¿Desea descargar todos los datos o una cantidad específica? (todos/cantidad): ').strip().lower()

if opcion == 'cantidad':
    cantidad = int(input(f'Ingrese la cantidad de datos que desea descargar (máximo {len(df)}): '))
    cantidad = min(cantidad, len(df))  # Asegurarse de no exceder el límite de datos disponibles.
    df = df.head(cantidad)  # Filtrar el DataFrame con los primeros 'cantidad' registros.
elif opcion != 'todos':
    print("Opción no válida. Se descargarán todos los datos.")
else:
    print(f"Descargando los {len(df)} datos disponibles...")

# Mostrar los datos descargados en consola
print("DataFrame:\n", df)

# Guardar los datos en un archivo CSV con codificación UTF-8
df.to_csv(f'{dominio}.csv', index=False, encoding='utf-8-sig')
print(f'Datos guardados en el archivo: {dominio}.csv')
