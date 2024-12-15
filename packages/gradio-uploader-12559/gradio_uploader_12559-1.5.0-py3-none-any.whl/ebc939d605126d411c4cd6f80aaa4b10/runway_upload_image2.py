#@title subir imagen Minimax
import requests
import uuid
import json
import ast
import os
import time
from kreg import register_user

def subir_media_runway2(path_image):
    bearer_token = os.environ.get("BEARER_TOKEN")
    refresh_token = os.environ.get("REFRESH_TOKEN")
    uuids = str(uuid.uuid4())
    # URL del endpoint
    url = "https://kaiber.ai/api/v1/media/save_media"

    # Cabeceras completas (sin Content-Type explícito)
    headers = {
        "Host": "kaiber.ai",
        "Connection": "keep-alive",
        "X-Platform": "web",
        "Authorization": f"Bearer {bearer_token}",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ0ODAzOTkiLCJhcCI6IjExMjAzMjM1NzIiLCJpZCI6ImRhNzUyMmRlYjA3YWY1MWQiLCJ0ciI6IjcwMzJjNTFjNTc2ZjAwYmUxMjhiZWIxYTJlZjliZWIwIiwidGkiOjE3MzI4MjgzNTY1NDN9fQ==",
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=14ffe6fa8d526ee741281bffeeeaa90c5da55b2c,sentry-public_key=9348ec458b83e7582c3a35f036e91604,sentry-trace_id=3d91e402e13d43aea3b2c0341a8cb686,sentry-sample_rate=1,sentry-sampled=true",
        "sentry-trace": "3d91e402e13d43aea3b2c0341a8cb686-9dbe92b24c87786d-1",
        "traceparent": "00-db9c7f20e16dcac28406b2cff8b6c737-eade0963ffb1e941-01",
        "X-Refresh-Token": refresh_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "tracestate": "4480399@nr=0-1-4480399-1120323572-eade0963ffb1e941----1732949641749",
        "X-Timezone-Offset": "180",
        "Origin": "https://kaiber.ai",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://kaiber.ai/superstudio/canvas/{uuids}",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

    # Datos del formulario
    files = {
        "media": ("Sin título.png", open(f"{path_image}", "rb"), "image/png"),
    }
    data = {
        "tags": '[{"ns":"Media","name":"Image"},{"ns":"Uploaded","name":"Yes"}]',
        "mediaId": f"{uuids}",
    }



    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        # Intentar convertir la respuesta a JSON
        try:
            data_dict = ast.literal_eval(response.text)

            # Extraer valores
            asset_key_id = data_dict['media']['assetKey']
            media_ids = data_dict['media']['mediaId']

            os.environ["ASSET_KEY_ID2"] = asset_key_id
            os.environ["MEDIA_ID_IMG2"] = media_ids
            #return media_ids, asset_key_id   # Retorna el mediaId extraído
        except ValueError:
            print("Error...")
            #return None, None
    else:
        print("In process...")
        register_user()
        time.sleep(2)
        subir_media_runway2(path_image)