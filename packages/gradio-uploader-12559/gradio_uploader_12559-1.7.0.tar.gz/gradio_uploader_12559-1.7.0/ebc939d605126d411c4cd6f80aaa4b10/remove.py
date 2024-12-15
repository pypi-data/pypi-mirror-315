import requests
import os
import uuid

def upload_file_remove(file_path):

    url = "https://api5g.iloveimg.com/v1/upload"
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJhdWQiOiIiLCJpYXQiOjE1MjMzNjQ4MjQsIm5iZiI6MTUyMzM2NDgyNCwianRpIjoicHJvamVjdF9wdWJsaWNfYzkwNWRkMWMwMWU5ZmQ3NzY5ODNjYTQwZDBhOWQyZjNfT1Vzd2EwODA0MGI4ZDJjN2NhM2NjZGE2MGQ2MTBhMmRkY2U3NyJ9.qvHSXgCJgqpC4gd6-paUlDLFmg0o2DsOvb1EUYPYx_E",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    # Archivos y datos para enviar en la solicitud
    files = {
        "file": (file_path.split('/')[-1], open(file_path, "rb"), "image/png")
    }
    data = {
        "name": file_path.split('/')[-1],
        "chunk": "0",
        "chunks": "1",
        "task": "gyhlpbxfbv92Asq51kA9412wtnzfsbpj8fd0rsrspk86jxfs1bjph66qqgl0nlpgAk6mxlxc16kn9xr1p6ccw36m7gzkjmbAllnptwdm2rgc8qtxd2slc9716AkdsA1cfv8txz2rn87y1dtpz0bxtA6rl0qc5lkssts00jzf5jp79y47dszq",
        "preview": "1",
        "pdfinfo": "0",
        "pdfforms": "0",
        "pdfresetforms": "0",
        "v": "web.0"
    }

    # Hacer la solicitud POST
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()  # Elevar una excepción si hay un error HTTP
        json_response = response.json()  # Parsear la respuesta como JSON
        server_filenames = json_response.get("server_filename", "No se encontró server_filename")

        if server_filenames:
           os.environ["REMOVE_FILE"] = server_filenames
           
        return "No se encontró server_filename"
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def remove_image():
    # Ruta de la carpeta
    carpeta = '/tmp/img_remove'
    # Verifica si la carpeta no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    output_path = str(uuid.uuid4())
    server_filename = os.environ.get("REMOVE_FILE")
    api_url = "https://api5g.iloveimg.com/v1/removebackground"

    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIiLCJhdWQiOiIiLCJpYXQiOjE1MjMzNjQ4MjQsIm5iZiI6MTUyMzM2NDgyNCwianRpIjoicHJvamVjdF9wdWJsaWNfYzkwNWRkMWMwMWU5ZmQ3NzY5ODNjYTQwZDBhOWQyZjNfT1Vzd2EwODA0MGI4ZDJjN2NhM2NjZGE2MGQ2MTBhMmRkY2U3NyJ9.qvHSXgCJgqpC4gd6-paUlDLFmg0o2DsOvb1EUYPYx_E",
        "Accept": "*/*"
    }
    
    # Datos del formulario
    data = {
        "task": "gyhlpbxfbv92Asq51kA9412wtnzfsbpj8fd0rsrspk86jxfs1bjph66qqgl0nlpgAk6mxlxc16kn9xr1p6ccw36m7gzkjmbAllnptwdm2rgc8qtxd2slc9716AkdsA1cfv8txz2rn87y1dtpz0bxtA6rl0qc5lkssts00jzf5jp79y47dszq",
        "server_filename": server_filename
    }

    try:
        # Realizar la solicitud POST
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()  # Verifica errores HTTP

        # Guardar la respuesta como archivo de imagen
        with open(f"/tmp/img_remove/{output_path}.png", "wb") as file:
            file.write(response.content)
        
        os.environ["IMAGE_REMOVE"] = f"/tmp/img_remove/{output_path}.png"
        print(f"Scaled image saved in: {output_path}.png")
    except requests.exceptions.RequestException as e:
        print(f"Error executing request")