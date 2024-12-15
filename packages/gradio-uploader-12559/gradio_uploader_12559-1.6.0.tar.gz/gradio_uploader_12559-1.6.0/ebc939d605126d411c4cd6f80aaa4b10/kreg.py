
#@title registro
# Primero asegúrate de tener instalada la librería requests (si no está instalada)

# Importa la librería
import os
import requests
import re
from bs4 import BeautifulSoup
import time
import random
import string
import random


def enviar_formulario():
    url = 'https://email-fake.com/'  # URL del formulario

    datos = {'campo_correo': 'ejemplo@dominio.com'}  # Datos del formulario

    # Envía la solicitud POST
    response = requests.post(url, data=datos)

    # Extrae los dominios de la respuesta
    dominios = extraer_dominios(response.text)

    if dominios:
      sitio_aleatorio = obtener_sitio_web_aleatorio(dominios)

    return sitio_aleatorio

def extraer_dominios(response_text):
    """Extrae dominios desde el texto HTML de la respuesta."""
    return re.findall(r'id="([^"]+\.[^"]+)"', response_text)

def obtener_sitio_web_aleatorio(dominios):
    """Obtiene un sitio web aleatorio de la lista de dominios."""
    return random.choice(dominios)

def generar_nombre_completo():
    """Genera un nombre completo triplicando el nombre y apellido, junto con un número aleatorio de 3 dígitos."""
    nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
               "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
               "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
               "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa",
               # Nombres comunes de EE.UU.
               "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
               "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
               "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
               "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
               "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry",
               "Tyler", "Aaron", "Henry", "Douglas", "Jose", "Peter", "Adam", "Zachary", "Nathan", "Walter", 
               "Kyle", "Harold", "Carl", "Arthur", "Gerald", "Roger", "Keith", "Jeremy", "Terry", "Lawrence",
               "Sean", "Christian", "Ethan", "Austin", "Joe", "Jordan", "Albert", "Jesse", "Willie", "Billy"]

    apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
                 "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
                 "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
                 "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez",
                 # Apellidos comunes de EE.UU.
                 "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                 "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                 "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                 "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                 "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood"]


    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    numero = random.randint(100000, 999999)

    nombre_completo = f"{nombre}_{apellido}_{numero}"
    return nombre_completo

def generar_contrasena():
    """Genera una contraseña aleatoria."""
    caracteres = string.ascii_letters + "0123456789" + "#$%&/()@_-*+[]"
    longitud = 10
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def login_user(email, password, bearer_token, refresh_token):

    url = "https://kaiber.ai/api/auth/login"
    headers = {
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",  # Token de autorización
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImUxNzY0ZDk0NDBmMGE0ODUiLCJ0ciI6IjFiMGQ2MWQyMTU1NDU5OGJkZTBkZDE3MWViOGQ5Y2MxIiwidGkiOjE3MzI3NjI1NDM4ODN9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=e5967f3de92606cfa5faed6b27e5711320af8389,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=d41e8f5c9e3d4a788a35426f24e728fd,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "d41e8f5c9e3d4a788a35426f24e728fd-bfe65deb79b5eff4-1",
        "traceparent": "00-1b0d61d21554598bde0dd171eb8d9cc1-e1764d9440f0a485-01",
        "X-Refresh-Token": refresh_token,  # Refresh Token
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-e1764d9440f0a485----1732762543883",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://kaiber.ai/login",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    data = {
        "email": email,  # Email ingresado por el usuario
        "password": password  # Contraseña ingresada por el usuario
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Lanza un error para respuestas HTTP no exitosas
        response_data = response.json()  # Obtiene la respuesta JSON del servidor

        # Extraer token y refreshToken de la respuesta
        extracted_token = response_data.get('token', None)
        extracted_refresh_token = response_data.get('refreshToken', None)

        # Mostrar los tokens extraídos
        #print(f"Token: {extracted_token}")
        #print(f"RefreshToken: {extracted_refresh_token}")

        # Retornar los valores si es necesario
        return extracted_token, extracted_refresh_token

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def verify_email(token):

    url = "https://kaiber.ai/api/auth/email/verify"
    headers = {
        "Host": "kaiber.ai",
        "Connection": "keep-alive",
        "X-Platform": "web",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6IjJlOTFhY2Q4ZmZhMDgwNWUiLCJ0ciI6IjU3MTcyMDQyZTZiYTc4NGYyZGZkMWMzNmQ0NjZjYjA3IiwidGkiOjE3MzI3NjM2MzA3OTl9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=e5967f3de92606cfa5faed6b27e5711320af8389,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=b5de5eb42cd24e77b8aa811ceb3ea56a,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "b5de5eb42cd24e77b8aa811ceb3ea56a-9fc56f30f91b2abd-1",
        "traceparent": "00-57172042e6ba784f2dfd1c36d466cb07-2e91acd8ffa0805e-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-2e91acd8ffa0805e----1732763630799",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://kaiber.ai/email/verify/{token}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }
    data = {
        "token": token
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Lanza un error para respuestas HTTP no exitosas
        response_data = response.json()  # Devuelve la respuesta JSON del servidor

        # Extraemos el token y refreshToken de la respuesta
        extracted_token = response_data.get('token', None)
        extracted_refresh_token = response_data.get('refreshToken', None)

        # Imprimir los tokens extraídos
        #print(f"Token: {extracted_token}")
        #print(f"RefreshToken: {extracted_refresh_token}")

        # Retornar los valores de los tokens si es necesario para más uso
        return extracted_token, extracted_refresh_token

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def extract_kaiber_verification_token(url):
    """
    Extracts the verification token from a Kaiber email verification URL.

    Args:
        url: The Kaiber verification URL as a string.

    Returns:
        The extracted token as a string, or None if the URL is not in the expected format.
    """
    token_pattern = r"https://click\.pstmrk\.it/3s/kaiber\.ai%2Femail%2Fverify%2F([^\/]+)"
    match = re.search(token_pattern, url)

    if match:
        return match.group(1)
    else:
        return None

def extract_kaiber_verification_url(html_content):
    """
    Extracts the Kaiber email verification URL from HTML content.

    Args:
        html_content: The HTML content as a string.

    Returns:
        The extracted URL as a string, or None if the URL is not found.
    """
    url_pattern = r"(https://click\.pstmrk\.it/3s/kaiber\.ai%2Femail%2Fverify%2F[^\"]+)"
    match = re.search(url_pattern, html_content)

    if match:
        return match.group(1)
    else:
        return None

COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}


def delete_temp_mail(username_email, dominios_dropdown, extracted_string):
    """Borra el correo temporal especificado."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/del_mail.php"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://email-fake.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'embx=%5B%22{username_email}%40{dominios_dropdown}%22%2C',
    }

    data = f'delll={extracted_string}'

    response = requests.post(url, headers=headers, data=data)

    if "Message deleted successfully" in response.text:
        print("Temporary mail deleted...")
        return True
    else:
        print("Error deleting temporary email...")
        return False

def get_verification_code(username_email, dominios_dropdown, max_retries=6, wait_seconds=3):
    """Obtiene el código de verificación del correo y el identificador."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Cookie': f'surl={dominios_dropdown}%2F{username_email}',
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            html_content = response.text
            verification_url = extract_kaiber_verification_url(html_content)
            identifier_match = re.search(r'delll:\s*"([a-zA-Z0-9]+)"', html_content)

            if verification_url and identifier_match:
                identifier = identifier_match.group(1)
                delete_temp_mail(username_email, dominios_dropdown, identifier)

                return extract_kaiber_verification_token(verification_url), identifier
            else:
                print(f"Attempt {attempt + 1}/{max_retries}: Verification URL or identifier not found. Retrying...")
                time.sleep(wait_seconds)

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Error fetching URL: {e}")
            time.sleep(wait_seconds)
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Unexpected error occurred: {e}")
            time.sleep(wait_seconds)

    print("Maximum retry attempts reached. Exiting...")
    return None, None

# Define la función para realizar la solicitud POST
def register_user():
    # Si no se pasan email o password, pedirlos al usuario
    nombres = generar_nombre_completo()
    if nombres:
      dominios = enviar_formulario()
      email  = f"{nombres}@{dominios}"
      password = generar_contrasena()
      #print("Email", email)
      #print("Password", password)
      os.environ["NAME_EMAIL"] = email
      os.environ["NAME_PASS"] = password


    # URL del endpoint
    url = "https://kaiber.ai/api/auth/register"

    # Encabezados de la solicitud
    headers = {
        "Connection": "keep-alive",
        "X-Platform": "web",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImU5ZDIyMzU1NDllMzVkYzIiLCJ0ciI6IjlhOGViOGY3ZjM5NGNkMjZhZTc4Mzg3ZWIzM2FjY2I5IiwidGkiOjE3MzI3NjI1MTY4NTB9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=e5967f3de92606cfa5faed6b27e5711320af8389,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=e95dae821ce34c4891e3cf496fbfc069,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "e95dae821ce34c4891e3cf496fbfc069-b63e22b49a30a7ff-1",
        "traceparent": "00-9a8eb8f7f394cd26ae78387eb33accb9-e9d2235549e35dc2-01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-e9d2235549e35dc2----1732762516850",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://kaiber.ai/register",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    # Datos del cuerpo de la solicitud (payload)
    data = {
        "email": email,
        "password": password,
        "passwordConfirmation": password,
        "newsletter": True,
        "referrerId": None,
        "affiliateLinkToken": None,
        "impactPartnerId": None,
        "impactPartnerToken": None
    }

    # Realiza la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    time.sleep(3)

    # Imprime el estado y respuesta del servidor
    #print("Status Code:", response.status_code)
    #print(response.text)

    if "Created" == response.text:

      # Parámetros de entrada
      username_email = email.split('@')[0]
      dominios_dropdown = email.split('@')[1]

      # Ejecución de la función
      url_token, identifier = get_verification_code(username_email, dominios_dropdown)

      #print(f"Verification URL: {url_token}")
      #print(f"Identifier: {identifier}")

      if url_token and identifier:
        #print(f"Token: {url_token}")
        #print(f"User ID: {identifier}")

        time.sleep(1)

        bearer_token, refresh_token = verify_email(url_token)

        if bearer_token and refresh_token:
          #print("bearer_token", bearer_token)
          #print("refresh_token", refresh_token)
          
          time.sleep(1)
          # Llamar a la función con los parámetros
          bearer_token, refresh_token = login_user(email, password, bearer_token, refresh_token)

          if bearer_token and refresh_token:

             os.environ["BEARER_TOKEN"] = bearer_token
             os.environ["REFRESH_TOKEN"] = refresh_token


      else:
        print("Error al obtener el url_token o el identifier.")