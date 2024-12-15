#@title MINIMAX IMAGE A VIDEOO
import requests
import uuid
import json
import os
import requests
from kreg import register_user
from logs import *
import requests
import time
import os
import requests
import time
import os

def load_counter():
    COUNTER_FILE = "/tmp/counter.txt"

    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_counter(count):
    COUNTER_FILE = "/tmp/counter.txt"

    with open(COUNTER_FILE, "w") as file:
        file.write(str(count))

def increment_counter():
    count = load_counter()
    if count < 20:
        count += 1
        save_counter(count)
    #print(f"The current counter value is: {count}")
    if count == 20:
        print("You have reached the daily limit.")

    return count


def delete_account():
    result, success = login_and_get_data()

    if success:

        bearer_token = os.environ.get("BEARER_TOKEN")
        refresh_token = os.environ.get("REFRESH_TOKEN")
        current_password = os.environ.get("NAME_PASS")

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
            "Origin": result[1],
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": result[2],
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        }

        # Datos que se envían en el cuerpo de la solicitud
        data = {
            "currentPassword": current_password
        }

        # Realizando la solicitud POST
        response = requests.post(result[0], headers=headers, json=data)


def get_media(bearer_token, refresh_token, media_id):
    # URL del endpoint con el ID de media
    url = f"https://kaiber.ai/api/v1/media/{media_id}"

    # Cabeceras (headers) de la solicitud
    headers = {
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",  # Token Bearer editable
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6IjQ0NzU5OTUwMTgwYjc3MTgiLCJ0ciI6IjY1NDhiZDU3ZTIyMmNhYzQxMDEwYjRhMTllZjUxZjU2IiwidGkiOjE3MzI3NzA4MzY0MzV9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=e5967f3de92606cfa5faed6b27e5711320af8389,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=79be22464b9f4e7ba5ea6defd88f9513,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "6dd3ff7522a14ce6a3bf32473e21d6ce-8745aedda8590f03-1",
        "traceparent": "00-6548bd57e222cac41010b4a19ef51f56-44759950180b7718-01",
        "X-Refresh-Token": refresh_token,  # Token de refresco editable
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-44759950180b7718----1732770836435",
        "X-Timezone-Offset": "180",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://kaiber.ai/superstudio/canvas/{media_id}",  # Referer con el ID de media
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    # Realizando la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificando el estado de la respuesta
    if response.status_code == 200:
        return response.json()  # Retornar la respuesta en formato JSON si la solicitud fue exitosa
    else:
        return None  # Si hay error, retornar None para que sigamos esperando

def download_video(url, save_path):
    # Realizar la solicitud para obtener el archivo del video
    response = requests.get(url, stream=True)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Guardar el archivo en el directorio especificado
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("\nVideo downloaded")
    else:
        print("\Error downloading video")

def monitor_media(bearer_token, refresh_token, media_id):
    attempt_count = 0  # Contador de intentos

    while True:
        # Llamar a la función get_media para obtener la información del video
        response_data = get_media(bearer_token, refresh_token, media_id)

        if response_data:
            media_status = response_data.get("media", {}).get("status")
            
            # Verificar si el estado es "failed"
            if media_status == "failed":
                os.environ["FAILDE_VIDEO"] = media_status
                print("\nVideo processing failed. Processing stopped.")
                break

            # Verificar si el estado es "pending"
            elif media_status == "pending":
                os.environ["FAILDE_VIDEO"] = media_status
                attempt_count += 1
                print(f"\tAttempt {attempt_count}: Pending status. Waiting 3 seconds before trying again...", end="")
                time.sleep(3)

            # Verificar si la respuesta contiene la clave "source" para descargar el video
            elif "source" in response_data.get("media", {}):
                video_url = response_data["media"]["source"]

                # Ruta donde se guardará el video
                save_path = f"/tmp/video/{media_id}.mp4"

                # Descargar el video
                download_video(video_url, save_path)

                os.environ["DIR_VIDEO"] = save_path
                increment_counter()
                print("\nVideo downloaded successfully.\nProcess completed.")
                break
        else:
            print("\failed to get video information. Trying again...")

        # Aumentar el contador de intentos y esperar
        attempt_count += 1
        time.sleep(3)

def gen_runway_image2_to_video(model_type="RunwayVideoGen3", elements_0="subject", elements_1="runwayStartKeyframe", elements_2="runwayEndKeyframe", elements_3="runwayVideoGen3Settings", aspect_ratio="16:9", width=1344, height=768, subject="talking youtuber", evolve=4, version=1, video_type="Video", motion_magnitude=4, length=5, stable_diffusion_checkpoint="dreamshaper", guidance=3, steps=38, denoise=0.4, creativity_scale=5, loop_video=False, audio_reactivity=6, scale_factor=2, topaz_model="Standard V2", topaz_face_enhancement_creativity=0, flux_pro_model="flux-pro-1.1-ultra", prompt_upsampling=True, form_index=1, starting_frame_weights="", runway_EndKeyframeWeights="0.8", name="Runway Video", userProvidedStartingFrame="", runway_EndKeyframe=""):
    result, success = login_and_get_data()

    if success:

        bearer_token = os.environ.get("BEARER_TOKEN")
        refresh_token = os.environ.get("REFRESH_TOKEN")
        uuids = str(uuid.uuid4())

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
            "Referer": f"{result[6]}{uuids}",
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        }

        # Realizar la solicitud GET
        response = requests.get(result[5], headers=headers)
        
        # Comprobar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Analizar la respuesta JSON

            credits = data.get("credits")  # Extraer el valor de 'credits'

                
            # Validar si los créditos son mayores a 25
            if credits >= 25:
                print(f"Generation in process...")
                process_media(bearer_token, refresh_token, model_type, elements_0, elements_1, elements_2, elements_3, aspect_ratio, width, height, subject, evolve, version, video_type, motion_magnitude, length, stable_diffusion_checkpoint, guidance, steps, denoise, creativity_scale, loop_video, audio_reactivity, scale_factor, topaz_model, topaz_face_enhancement_creativity, flux_pro_model, prompt_upsampling, form_index, starting_frame_weights, runway_EndKeyframeWeights, name, userProvidedStartingFrame, runway_EndKeyframe)
                
                media_id = os.environ.get("MEDIA_ID")
                
                if media_id:
                  # Llamar a la función que monitoriza la media
                  monitor_media(bearer_token, refresh_token, media_id)
                  
            else:
                print(f"Generation in process...")
                delete_account()
                time.sleep(1)
                count = load_counter()
                if count < 20:
                    register_user()
                user_email = os.environ.get("NAME_EMAIL")
                user_pass = os.environ.get("NAME_PASS")

                bearer_token = os.environ.get("BEARER_TOKEN")
                refresh_token = os.environ.get("REFRESH_TOKEN")


                time.sleep(2)
                process_media(bearer_token, refresh_token, model_type, elements_0, elements_1, elements_2, elements_3, aspect_ratio, width, height, subject, evolve, version, video_type, motion_magnitude, length, stable_diffusion_checkpoint, guidance, steps, denoise, creativity_scale, loop_video, audio_reactivity, scale_factor, topaz_model, topaz_face_enhancement_creativity, flux_pro_model, prompt_upsampling, form_index, starting_frame_weights, runway_EndKeyframeWeights, name, userProvidedStartingFrame, runway_EndKeyframe)
                
                media_id = os.environ.get("MEDIA_ID")
                
                if media_id:
                  # Llamar a la función que monitoriza la media
                  monitor_media(bearer_token, refresh_token, media_id)
                
        else:
            print(f"Generation in process...")
            delete_account()
            time.sleep(1)
            count = load_counter()
            if count < 20:
                register_user()
            user_email = os.environ.get("NAME_EMAIL")
            user_pass = os.environ.get("NAME_PASS")

            bearer_token = os.environ.get("BEARER_TOKEN")
            refresh_token = os.environ.get("REFRESH_TOKEN")

            time.sleep(2)
            process_media(bearer_token, refresh_token, model_type, elements_0, elements_1, elements_2, elements_3, aspect_ratio, width, height, subject, evolve, version, video_type, motion_magnitude, length, stable_diffusion_checkpoint, guidance, steps, denoise, creativity_scale, loop_video, audio_reactivity, scale_factor, topaz_model, topaz_face_enhancement_creativity, flux_pro_model, prompt_upsampling, form_index, starting_frame_weights, runway_EndKeyframeWeights, name, userProvidedStartingFrame, runway_EndKeyframe)
                
            media_id = os.environ.get("MEDIA_ID")
                
            if media_id:
                # Llamar a la función que monitoriza la media
                monitor_media(bearer_token, refresh_token, media_id)
            

def obtener_media_id(json_data):
    # Convertir el string JSON en un diccionario de Python
    data = json.loads(json_data)

    # Extraer y devolver el mediaId
    return data['medias'][0]['mediaId']

def process_media(bearer_token, refresh_token, model_type="RunwayVideoGen3", elements_0="subject", elements_1="runwayStartKeyframe", elements_2="runwayEndKeyframe", elements_3="runwayVideoGen3Settings", aspect_ratio="16:9", width=1344, height=768, subject="talking youtuber", evolve=4, version=1, video_type="Video", motion_magnitude=4, length=5, stable_diffusion_checkpoint="dreamshaper", guidance=3, steps=38, denoise=0.4, creativity_scale=5, loop_video=False, audio_reactivity=6, scale_factor=2, topaz_model="Standard V2", topaz_face_enhancement_creativity=0, flux_pro_model="flux-pro-1.1-ultra", prompt_upsampling=True, form_index=1, starting_frame_weights="", runway_EndKeyframeWeights="0.8", name="Runway Video", userProvidedStartingFrame="", runway_EndKeyframe=""):
    result, success = login_and_get_data()

    if success:
        
        uuids = str(uuid.uuid4())

        # Headers (cabeceras de la solicitud)
        headers = {
            "Connection": "keep-alive",
            "X-Platform": "web",
            "Authorization": f"Bearer {bearer_token}",  # Bearer token
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImUwNmVlYmMxZmE2ODk5ZTciLCJ0ciI6IjRlMWQyMTdmNDA4ZTQyNTc3YmY5YjZmOWY3YzBiN2JhIiwidGkiOjE3MzI3NzA4MzAzODJ9fQ==",
            "sec-ch-ua-mobile": "?0",
            "baggage": "sentry-environment=production,sentry-release=14ffe6fa8d526ee741281bffeeeaa90c5da55b2c,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=3d91e402e13d43aea3b2c0341a8cb686,sentry-sample_rate=1,sentry-sampled=true",
            "sentry-trace": "3d91e402e13d43aea3b2c0341a8cb686-9dbe92b24c87786d-1",
            "traceparent": "00-a9a154c53d69b0507c749da774680fe8-a70a942b8b8286d7-01",
            "X-Refresh-Token": refresh_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarySGpGyngeeNNpUANH",
            "tracestate": "4480399@nr=0-1-4480399-1120323572-a70a942b8b8286d7----1732949651840",
            "X-Timezone-Offset": "180",
            "Origin": result[8],
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"{result[9]}{uuids}",
            "Accept-Language": "es-ES,es;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        }

        # Cuerpo de la solicitud (en formato multipart/form-data)
        data = (
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"mediaIds[]\"\r\n\r\n{uuids}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[modelType]\"\r\n\r\n{model_type}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[elements][0]\"\r\n\r\n{elements_0}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[elements][1]\"\r\n\r\n{elements_1}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][aspectRatio]\"\r\n\r\n{aspect_ratio}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][lockAspectRatio]\"\r\n\r\ntrue\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][width]\"\r\n\r\n{width}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][height]\"\r\n\r\n{height}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][subject]\"\r\n\r\n{subject}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][style]\"\r\n\r\n\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][evolve]\"\r\n\r\n{evolve}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][version]\"\r\n\r\n{version}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][type]\"\r\n\r\n{video_type}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][motionMagnitude]\"\r\n\r\n{motion_magnitude}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][length]\"\r\n\r\n{length}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][stableDiffusionCheckpoint]\"\r\n\r\n{stable_diffusion_checkpoint}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][guidance]\"\r\n\r\n{guidance}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][steps]\"\r\n\r\n{steps}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][denoise]\"\r\n\r\n{denoise}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][creativityScale]\"\r\n\r\n{creativity_scale}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][loopVideo]\"\r\n\r\n{str(loop_video).lower()}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][audioReactivity]\"\r\n\r\n{audio_reactivity}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][scaleFactor]\"\r\n\r\n{scale_factor}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][topazModel]\"\r\n\r\n{topaz_model}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][topazFaceEnhancementCreativity]\"\r\n\r\n{topaz_face_enhancement_creativity}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][fluxProModel]\"\r\n\r\n{flux_pro_model}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][promptUpsampling]\"\r\n\r\n{str(prompt_upsampling).lower()}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][userProvidedStartingFrame][0]\"\r\n\r\n{userProvidedStartingFrame}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][runwayEndKeyframe][0]\"\r\n\r\n{runway_EndKeyframe}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][formIndex]\"\r\n\r\n{form_index}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][runwayEndKeyframeWeights][0]\"\r\n\r\n{runway_EndKeyframeWeights}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[formValues][userProvidedStartingFrameWeights][0]\"\r\n\r\n{starting_frame_weights}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH\r\n"
            f"Content-Disposition: form-data; name=\"flow[name]\"\r\n\r\n{name}\r\n"
            f"------WebKitFormBoundarySGpGyngeeNNpUANH--\r\n"
        )

        # Realizando la solicitud POST
        response = requests.post(result[7], headers=headers, data=data)

        #print(response.text)

        # Si la respuesta es exitosa (código 200)
        if response.status_code == 200:
            # Intentar convertir la respuesta a JSON
            try:
                data = json.loads(response.text)

                # Extraer y devolver el mediaId
                media_id = data['medias'][0]['mediaId']
                os.environ["MEDIA_ID"] = media_id
                #print(media_id)
                #return media_id  # Retorna el mediaId extraído
            except ValueError:
                #print("Error al convertir la respuesta a JSON")
                os.environ["MEDIA_ID"] = None
                #return None
        else:
            #print(f"Error en la solicitud: {response.status_code}")
            os.environ["MEDIA_ID"] = None
            #return None