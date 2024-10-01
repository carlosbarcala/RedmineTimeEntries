import requests
import pandas as pd
from datetime import datetime, timedelta

# Configura tus credenciales y URL de Redmine
REDMINE_URL = 'https://gestion.sixtema.int'  # Cambia esto por la URL de tu Redmine
API_KEY = 'e94c9122d8c018b0344cdbfbf66e0e3442810bf7'  # Cambia esto por tu clave API
USER_ID = '89'  # Cambia esto por el ID del usuario que deseas filtrar

# Establecer los encabezados para la solicitud
headers = {
    'X-Redmine-API-Key': API_KEY,
    'Content-Type': 'application/json',
}

def obtener_tiempo_dedicado(user_id, desde, hasta):
    url = f'{REDMINE_URL}/time_entries.json?user_id={user_id}&from={desde}&to={hasta}'
    
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code != 200:
        print(f'Error al obtener datos: {response.status_code}')
        return []
    
    data = response.json()
    return data.get('time_entries', [])

def mostrar_tiempo_dedicado(tiempo_entries):
    # Crear un DataFrame de pandas para mostrar en forma de tabla
    df = pd.DataFrame(tiempo_entries)
    
    if not df.empty:
        # Seleccionar las columnas relevantes
        df = df[['hours', 'spent_on']]
        df.columns = ['Horas', 'Fecha']
        
        # Agrupar por fecha y sumar las horas
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df = df.groupby('Fecha').sum().reset_index()

        # Ordenar por fecha
        df.sort_values('Fecha', inplace=True)

        # Imprimir la tabla
        print(df)
    else:
        print('No se encontraron entradas de tiempo.')

def main():
    # Calcular las fechas para los dos últimos meses
    hoy = datetime.today()
    desde = (hoy - timedelta(days=hoy.day + 30)).replace(day=1).strftime('%Y-%m-%d')
    hasta = hoy.strftime('%Y-%m-%d')

    tiempo_entries = obtener_tiempo_dedicado(USER_ID, desde, hasta)
    mostrar_tiempo_dedicado(tiempo_entries)

if __name__ == '__main__':
    main()
