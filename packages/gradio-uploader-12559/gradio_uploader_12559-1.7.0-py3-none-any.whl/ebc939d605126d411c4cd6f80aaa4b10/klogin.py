#@title login
import requests
import os
import time

def obtener_tokens(bearer_token):
    # URL del endpoint
    url = "https://kaiber.ai/api/auth/me"

    # Encabezados necesarios para la solicitud
    headers = {
        "Authorization": f"Bearer {bearer_token}",  # Inserta el token de autorización
        "X-Platform": "web",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua": 'Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        
    }

    # Realizamos la solicitud GET
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Si la respuesta es exitosa, extraemos los tokens del JSON
        data = response.json()  # Convertir la respuesta a JSON
        token = data.get("token")
        refresh_token = data.get("refreshToken")

        return token, refresh_token
    else:
        print("Error en la solicitud:", response.status_code)
        return None, None


import os
import requests
import time

def login_to_kaiber(email, password):
    # Validar valores de entrada
    if not email or not password:
        raise ValueError("El correo electrónico y la contraseña son obligatorios.")
    
    os.environ["NAME_EMAIL"] = email
    os.environ["NAME_PASS"] = password
    url = "https://kaiber.ai/api/auth/login"

    headers = {
        "Host": "kaiber.ai",
        "Connection": "keep-alive",
        "X-Platform": "web",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://kaiber.ai",
        "Referer": "https://kaiber.ai/login",
        "Accept-Language": "es-ES,es;q=0.9"
    }

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get('token', None)

        if not token:
            print("Error: No se encontró el token en la respuesta.")
            return

        time.sleep(3)
        bearer_token, refresh_token = obtener_tokens(token)

        if bearer_token and refresh_token:
            os.environ["BEARER_TOKEN"] = bearer_token
            os.environ["REFRESH_TOKEN"] = refresh_token
        else:
            print("No se pudieron obtener los tokens.")
            os.environ["BEARER_TOKEN"] = None
            os.environ["REFRESH_TOKEN"] = None

    elif response.status_code == 401:
        print("Credenciales incorrectas: Verifica tu correo electrónico y contraseña.")
        os.environ["BEARER_TOKEN"] = None
        os.environ["REFRESH_TOKEN"] = None

    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")
        os.environ["BEARER_TOKEN"] = None
        os.environ["REFRESH_TOKEN"] = None
