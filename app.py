from flask import Flask, request, jsonify
import requests
from flask import render_template

app = Flask(__name__)

# Configura tu URL de Redmine y la clave API
REDMINE_URL = 'https://gestion.sixtema.int'  # Cambia esto según tu instancia
API_KEY = 'e94c9122d8c018b0344cdbfbf66e0e3442810bf7'  # Cambia esto por tu API key

@app.route('/api/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(url):
    headers = {
        'X-Redmine-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }

    full_url = f'{REDMINE_URL}/{url}'

    # Obtener los parámetros de la solicitud original
    params = request.args.to_dict()
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
    app.run(port=3000, debug=True)
