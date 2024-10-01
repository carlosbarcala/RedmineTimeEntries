from flask import Flask, request, jsonify
import requests
from flask import render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los valores de las variables de entorno
REDMINE_URL = os.getenv('REDMINE_URL', '')
API_KEY = os.getenv('API_KEY', '')
APP_PORT = os.getenv('APP_PORT', 3000)
REDMINE_USER_ID = os.getenv('REDMINE_USER_ID', '')

@app.route('/api/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(url):
    headers = {
        'X-Redmine-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }

    full_url = f'{REDMINE_URL}/{url}'

    # Obtener los parámetros de la solicitud original
    params = request.args.to_dict()
    params['user_id'] = REDMINE_USER_ID
    data = request.get_json(silent=True)

    # Enviar la solicitud a la API de Redmine con los parámetros recibidos por la URL y el cuerpo de la solicitud
    response = requests.request(
        method=request.method,
        url=full_url,
        headers=headers,
        params=params,
        json=data,
        verify=False,
    )

    return (response.content, response.status_code, response.headers.items())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=APP_PORT, debug=True)
