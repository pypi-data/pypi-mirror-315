import requests
import hashlib
import os


def iniciar_sesion(account, password):
    url = "https://piclumen.com/api/user/login"

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": "",  # Agrega tu token aquí si es necesario
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryG0HDGc4eqwD1nY07",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/account",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }

    # Generar el hash MD5 de la contraseña
    #hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Cuerpo de la solicitud con la estructura exacta requerida
    payload = (
        "------WebKitFormBoundaryG0HDGc4eqwD1nY07\r\n"
        f"Content-Disposition: form-data; name=\"account\"\r\n\r\n"
        f"{account}\r\n"
        "------WebKitFormBoundaryG0HDGc4eqwD1nY07\r\n"
        f"Content-Disposition: form-data; name=\"password\"\r\n\r\n"
        f"{password}\r\n"
        "------WebKitFormBoundaryG0HDGc4eqwD1nY07--\r\n"
    )

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=payload)

    # Manejar la respuesta
    if response.ok:
        respuesta_json = response.json()
        if "data" in respuesta_json:
            # Extraer token y userId
            tokens = respuesta_json["data"].get("token", None)
            os.environ["TOKEN_PIC"] = tokens
            user_ids = respuesta_json["data"].get("userId", None)
            os.environ["USER_ID_PIC"] = user_ids
            return tokens, user_ids
        else:
            return None, None
    else:
        return None, None

