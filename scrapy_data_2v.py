import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

print('*** Sistema para descargar datos de tablas en HTML ***')
url = input('Ingrese la URL de la página que desea scrapear: ')

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

# Función para contar las tablas en el HTML
def countTables(data):
    soup = bs(data, 'html.parser')
    tables = soup.find_all('table')  # Encuentra todas las tablas en el HTML.
    return len(tables), soup  # Devuelve la cantidad de tablas y el objeto soup.

# Leer el sitio web
req = requests.get(url)

if req.status_code != 200:
    print(f'Error al acceder a la página: {req.status_code}')
    exit()

HTML = req.text  # Convierte el contenido HTML en texto.
num_tables, soup = countTables(HTML)

if num_tables == 0:
    print("No se encontraron tablas en la página.")
    exit()

print(f'Se encontraron {num_tables} tablas en el HTML.')

# Pedir al usuario que elija una tabla
numero_tabla = int(input(f'¿A qué tabla del HTML quiere extraer la información? (1-{num_tables}): '))

if numero_tabla < 1 or numero_tabla > num_tables:
    print("Número de tabla fuera de rango.")
    exit()

# Procesar la tabla seleccionada
def processDataHTML(data, numero_tabla):
    tbl = soup.find_all('table')[numero_tabla - 1]  # Recupera la tabla seleccionada.
    tblRows = processTableData(tbl)  # Procesa la tabla.
    return tblRows

table = processDataHTML(HTML, numero_tabla)
dominio = url.split("//")[1].split("/")[0].replace(".", "-")
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
