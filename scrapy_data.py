import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

print('*** Sistema para descargar datos de tablas en html ***')
url = input('Ingrese la url de la pagina que desea scrapiar: ')
cantidad = int(input('Ingrese la cantidad de datos que desea descargar: '))
numero_tabla = int(input('A que tabla del HTML quiere extraer la informacion: '))
print('<------------------------------------------------------->')

# Funcion para convertir una lista en elementos del dataframe de pandas
def rowsToDataFrame(rows):
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


# Funcion para extraer los datos de una tabla HTML
def processTableData(tbl):
    rows = []
    for tr in tbl.find('tbody').find_all('tr'):  # itera los items internos de la tabla [<tr>]
        row = []
        for cell in tr.find_all(['td', 'th']): # consultando en cada celda si es [<td> o <th>]
            item = cell.get_text(strip=True) # Trae el texto ignorando las demas etiquetas Ej: [<b>] los espacios
            row.append(item) #añade a la lista row
        if row:
            rows.append(row) # si row tiene información añade a la lista de rows
    return rows


# funcion para extraer los datos URL y procesar el contenido HTML
def processDataHTML(data):


    soup = bs(data, 'html.parser')  #Le da estructura al HTML que esta como string
    tbl = soup.find_all('table')[numero_tabla-1]  # recupera la tabla del HTML
    tblRows = processTableData(tbl)  # Ejecucion de la funcion para procesar el contenido de la tabla
    return tblRows


# Leer la webside
# Declaramos r para hacer lña consulta requests.get('URL')
req = requests.get(url)
if req.status_code != 200:
    print(f'Error al acceder a la pagina: {req.status_code}')


print(f'Estado de la solicitud: {req.status_code}')


HTML = req.text #si se trabaja con content te devuelve en un byte, por eso se coloca el .text para que
                #se haga un string, y si se quiere un json se pone .json()
table = processDataHTML(HTML) #No use json ya que es el texto HTML de lo que se esta obteniendo.
df = rowsToDataFrame(table)
print("DataFrame:\n", df.head(cantidad)) #df.head(n) me muestra n registros que estan al inicio
df.info()
df.to_csv('statsWorldCup.csv', index=False)   #aqui se genera un csv y el index tiene la funcion de
                                                        #ocultar o mostrar la cabecera True oculta y False muestra
