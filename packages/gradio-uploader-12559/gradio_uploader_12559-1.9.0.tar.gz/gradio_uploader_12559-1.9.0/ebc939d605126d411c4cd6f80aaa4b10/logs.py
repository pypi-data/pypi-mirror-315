import requests
import os
import base64
import json

# Función para aplicar XOR con una clave
def aplicar_xor(data, clima):
    return bytes([b ^ clima for b in data])

# Función para desencriptar la cadena con base64 y reversión XOR
def desca(texto_base64):
    # Decodificar base64
    texto_xor = base64.b64decode(texto_base64)
    # Aplicar XOR inverso
    texto_original = aplicar_xor(texto_xor, 18)
    return texto_original.decode()

# Función para obtener la IP pública automáticamente
def get_user_ip():
    try:
        # Servicio gratuito para obtener la IP pública del usuario
        response = requests.get("https://api.ipify.org?format=json")
        ip_data = response.json()
        return ip_data.get('ip')
    except requests.exceptions.RequestException:
        return None

def login_and_get_data():
    API_KEY = os.environ.get("API_KEY")
    ip_address = get_user_ip()  # Obtener la IP automáticamente
    if not ip_address:
        return "No se pudo obtener la IP del usuario.", False  # En caso de error al obtener la IP
    # URL del script PHP
    url = "https://arcas.webcindario.com/curso_ai2/login.php"

    # Headers personalizados
    headers = {
        "Host": "arcas.webcindario.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html, application/xhtml+xml, application/xml;q=0.9, image/avif, image/webp, image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }

    # Parámetros de la solicitud POST
    data = {
        'api': API_KEY,  # Usando la API pasada como argumento
        'ip': ip_address  # Usando la IP pasada como argumento
    }

    try:
        # Realizar la solicitud POST con los headers, cookies y los parámetros de datos
        response = requests.post(url, headers=headers, data=data, timeout=30)

        # Verificar la respuesta
        if response.status_code == 200:
            # Intentar obtener la respuesta JSON
            response_json = response.json()
            if response_json.get('success', False):
                # Retornar el contenido de 'data' si la solicitud fue exitosa
                result = desca(response_json['data'])
                #variables = result.split(".")
                decoded_data = [desca(item) for item in result.split(".")]
                return  decoded_data, True    #desca(response_json['data'])
            else:
                # Si la respuesta es exitosa pero no contiene el campo 'data'
                return f"Error: {response_json.get('message', 'No data found')}", False
        else:
            return f"Error al acceder al servidor. Código de estado: {response.status_code}", False

    except requests.exceptions.RequestException as e:
        return f"Se produjo un error en la solicitud POST: {e}", False