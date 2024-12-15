#@title flux ultra
import requests
import uuid
import json
from kreg import register_user
import time
import os

def delete_account():
    bearer_token = os.environ.get("BEARER_TOKEN")
    refresh_token = os.environ.get("REFRESH_TOKEN")
    current_password = os.environ.get("NAME_PASS")
    # URL del endpoint para eliminar la cuenta
    url = "https://kaiber.ai/api/auth/myaccount/delete"

    # Cabeceras (headers) de la solicitud
    headers = {
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",  # Token Bearer editable
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImZmYTEzMjQ5OGUxNzZhMzciLCJ0ciI6IjQ0NWNkYWI4OGU1YzFjYjhhODlmZWJiMDkyOTdmNTliIiwidGkiOjE3MzI3NzY5NjQ0NDV9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=e5967f3de92606cfa5faed6b27e5711320af8389,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=71ee1caca0d843a991b316008899b374,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "71ee1caca0d843a991b316008899b374-a4d6f7a682131ea9-1",
        "traceparent": "00-445cdab88e5c1cb8a89febb09297f59b-ffa132498e176a37-01",
        "X-Refresh-Token": refresh_token,  # Token de refresco editable
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-ffa132498e176a37----1732776964445",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://kaiber.ai/account",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Datos que se envían en el cuerpo de la solicitud
    data = {
        "currentPassword": current_password
    }

    # Realizando la solicitud POST
    response = requests.post(url, headers=headers, json=data)




def gen_flux_pro_image(prompt, width, height, aspectRatio, model):
    bearer_token = os.environ.get("BEARER_TOKEN")
    refresh_token = os.environ.get("REFRESH_TOKEN")
    uuids = str(uuid.uuid4())
    # Definir la URL y los encabezados de la solicitud
    url = "https://kaiber.ai/api/get_credits"
    headers = {
        "Host": "kaiber.ai",
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6IjczY2I2MzFkZWQ3N2RiYmQiLCJ0ciI6ImJlNDZjZGM5ZGY5YTRmM2M3ODBkYjRlMDczZjA4OTNiIiwidGkiOjE3MzMwMDk5MTUwNjV9fQ==",
        "baggage": "sentry-environment=production,sentry-release=3efe4968f941933ebe2c9920e9a021f8740a50bf,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=13801de87c0547ab91fcf9d38f49316d,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "13801de87c0547ab91fcf9d38f49316d-9b93cf813adb3f97-1",
        "traceparent": "00-be46cdc9df9a4f3c780db4e073f0893b-73cb631ded77dbbd-01",
        "X-Refresh-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2NzRiOTg4MGIwN2YxZTliNWU3NDlhMDYiLCJzaWQiOiI2NzRiOThiYzNkZDNiMzUwMTQ1ZWNmNmEiLCJpYXQiOjE3MzMwMDc1NTEsImV4cCI6MTc0MDc4MzU1MX0.jCJUko3-Hm_FREinCcoC5TcftZP3qnYjOUaDhukn25E",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-73cb631ded77dbbd----1733009915065",
        "X-Timezone-Offset": "180",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://kaiber.ai/superstudio/canvas/{uuids}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)
    
    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()  # Analizar la respuesta JSON

        credits = data.get("credits")  # Extraer el valor de 'credits'

            
        # Validar si los créditos son mayores a 5
        if credits >= 5:
            print(f"In process..")
            #process_media(bearer_token, refresh_token, model_type, elements_0, elements_1, aspect_ratio, width, height, subject, evolve, version, video_type, motion_magnitude, length, stable_diffusion_checkpoint, guidance, steps, denoise, creativity_scale, loop_video, audio_reactivity, scale_factor, topaz_model, topaz_face_enhancement_creativity, flux_pro_model, prompt_upsampling, form_index, starting_frame_weights, name, userProvidedStartingFrame)
            save_path_flux = send_request_with_boundary(prompt, width, height, aspectRatio, model)
            os.environ["DIR_IMAGEE_FLUX_PRO"] = save_path_flux
            print(save_path_flux)
          
              
        else:
            print(f"In process..")
            delete_account()
            time.sleep(1)
            register_user()
            user_email = os.environ.get("NAME_EMAIL")
            user_pass = os.environ.get("NAME_PASS")

            bearer_token = os.environ.get("BEARER_TOKEN")
            refresh_token = os.environ.get("REFRESH_TOKEN")

            time.sleep(2)
            save_path_flux = send_request_with_boundary(prompt, width, height, aspectRatio, model)
            os.environ["DIR_IMAGEE_FLUX_PRO"] = save_path_flux
            
    else:
        print(f"In process..")
        delete_account()
        time.sleep(1)
        register_user()
        user_email = os.environ.get("NAME_EMAIL")
        user_pass = os.environ.get("NAME_PASS")

        bearer_token = os.environ.get("BEARER_TOKEN")
        refresh_token = os.environ.get("REFRESH_TOKEN")

        time.sleep(2)
        save_path_flux = send_request_with_boundary(prompt, width, height, aspectRatio, model)
        os.environ["DIR_IMAGEE_FLUX_PRO"] = save_path_flu
          
def obtener_media_id(json_data):
    # Convertir el string JSON en un diccionario de Python
    data = json.loads(json_data)

    # Extraer y devolver el mediaId
    return data['medias'][0]['mediaId']


def send_request_with_boundary(prompt, width, height, aspectRatio, model):
    bearer_token = os.environ.get("BEARER_TOKEN")
    refresh_token = os.environ.get("REFRESH_TOKEN")
    uuids = str(uuid.uuid4())
    url = "https://kaiber.ai/api/v1/media/process_media"
    headers = {
        "Host": "kaiber.ai",
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImUzOGE1MmM3NjI4MjBhMTQiLCJ0ciI6ImI4NjVhNzM0YTU0M2FkN2U4NDBlMDE4ZjgyZTdhOTFhIiwidGkiOjE3MzQxNDg3Mzk5MDd9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=fbb2febb8a343bc0cab9f2ea0793358a4d93fc58,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=bec753bb5c3a4081ac13bd16e9e17026,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "bec753bb5c3a4081ac13bd16e9e17026-bd944097d447ac5f-1",
        "traceparent": "00-b865a734a543ad7e840e018f82e7a91a-e38a52c762820a14-01",
        "X-Refresh-Token": refresh_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary8Ut7Azp3unSEiHyl",
        "tracestate": "<VALOR>",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://kaiber.ai/superstudio/canvas/{uuids}",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    data = (
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"mediaIds[]\"\r\n\r\n"
        f"{uuids}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[modelType]\"\r\n\r\n"
        "FluxImage\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[elements][0]\"\r\n\r\n"
        "prompt\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[elements][1]\"\r\n\r\n"
        "fluxImageSettings\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][subject]\"\r\n\r\n"
        f"{prompt}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][seed]\"\r\n\r\n"
        "-1\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][safety_tolerance]\"\r\n\r\n"
        "2\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][type]\"\r\n\r\n"
        "Image\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][width]\"\r\n\r\n"
        f"{width}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][height]\"\r\n\r\n"
        f"{height}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][promptUpsampling]\"\r\n\r\n"
        "true\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][fluxProModel]\"\r\n\r\n"
        f"{model}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"flow[formValues][aspectRatio]\"\r\n\r\n"
        f"{aspectRatio}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl\r\n"
        "Content-Disposition: form-data; name=\"fluxImageArgs[prompt]\"\r\n\r\n"
        f"{prompt}\r\n"
        "------WebKitFormBoundary8Ut7Azp3unSEiHyl--"
    )

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        json_response = response.json()
        # Extraer la URL del campo 'source'
        if 'medias' in json_response and len(json_response['medias']) > 0:
            source_url = json_response['medias'][0].get('source', None)
            if source_url:
                # Crear carpeta si no existe
                img_dir = "/tmp/img_flux_pro"
                os.makedirs(img_dir, exist_ok=True)

                # Descargar la imagen
                img_path = os.path.join(img_dir, f"{uuids}.jpg")
                try:
                    img_response = requests.get(source_url, stream=True)
                    if img_response.status_code == 200:
                        with open(img_path, "wb") as img_file:
                            for chunk in img_response.iter_content(1024):
                                img_file.write(chunk)
                        print(f"Image downloaded successfully")
                except Exception as e:
                    print(f"Error downloading image: {e}")
            else:
                print("No 'source' field found in the response.")
        else:
            print("No media data found in the response.")
    else:
        print(f"Request failed with status")
    return img_path
