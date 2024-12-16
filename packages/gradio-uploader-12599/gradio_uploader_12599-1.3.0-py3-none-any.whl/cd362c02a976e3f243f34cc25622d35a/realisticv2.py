import requests
import os
import time
from IPython.display import Image, display

def eliminar_imagen(correo, prompt_id, img_name):
    token = os.environ.get("TOKEN_PIC")
    url = "https://piclumen.com/api/img/delete"

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": token,  # Incluir el token aquí
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryNYpFkpGlmkQKklUK",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/image-generator/create",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }

    # El cuerpo de la solicitud es un multipart/form-data
    data = (
        f'------WebKitFormBoundaryNYpFkpGlmkQKklUK\r\n'
        f'Content-Disposition: form-data; name="promptId"\r\n\r\n{prompt_id}\r\n'
        f'------WebKitFormBoundaryNYpFkpGlmkQKklUK\r\n'
        f'Content-Disposition: form-data; name="imgName"\r\n\r\n{img_name}\r\n'
        f'------WebKitFormBoundaryNYpFkpGlmkQKklUK\r\n'
        f'Content-Disposition: form-data; name="loginName"\r\n\r\n{correo}\r\n'
        f'------WebKitFormBoundaryNYpFkpGlmkQKklUK--\r\n'
    )

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=data)

    # Manejar la respuesta
    if response.ok:
        return response.json()  # Devuelve la respuesta como JSON
    else:
        return {"error": f"Request failed: {response.status_code}", "details": response.text}

def procesar_tarea(mark_id):
    attempt_count = 0  # Variable para contar los intentos
    token = os.environ.get("TOKEN_PIC")
    correo = os.environ.get("USER_EMAIL_PIC")
    url = "https://piclumen.com/api/task/processTask"

    img_paths = []  # Lista para almacenar los paths de las imágenes

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": token,  # Incluir el token aquí
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryY6Cs6Ri21EvS8cpC",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/image-generator/create",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }

    payload = (
        "------WebKitFormBoundaryY6Cs6Ri21EvS8cpC\r\n"
        f"Content-Disposition: form-data; name=\"markId\"\r\n\r\n"
        f"{mark_id}\r\n"
        "------WebKitFormBoundaryY6Cs6Ri21EvS8cpC--\r\n"
    )

    while True:
        response = requests.post(url, headers=headers, data=payload)

        if response.ok:
            data = response.json()

            if "data" in data and "promptId" in data["data"]:
                prompt_id = data["data"]["promptId"]
                img_urls = data["data"]["img_urls"]

                if img_urls:
                    img_folder = "./images"
                    if not os.path.exists(img_folder):
                        os.makedirs(img_folder)

                    for img_data in img_urls:
                        img_name = img_data["imgName"]
                        img_url = img_data["imgUrl"]

                        # Descargar y guardar la imagen
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(img_folder, os.path.basename(img_name))
                            with open(img_path, "wb") as img_file:
                                img_file.write(img_response.content)

                            # Agregar img_path a la lista
                            img_paths.append(img_path)

                            # Eliminar la imagen del servidor
                            eliminar_imagen(correo, prompt_id, img_name)
                        else:
                            print(f"Error downloading image")

                    # Retornar solo los paths de las imágenes
                    return img_paths
                else:
                    attempt_count += 1
                    print(f"\tAttempt {attempt_count}: Waiting 5 seconds before trying again...", end="")
                    time.sleep(5)
            else:
                print("Task is not complete yet, retrying in 5 seconds...")
                time.sleep(5)
        else:
            #print(f"Request failed: {response.status_code}")
            return []



def generar_imagen_realisticv2(
    prompt,
    negative_prompt="",
    width=1472,
    height=704,
    batch_size=1,
    seed=70212802643,
    steps=4,
    cfg=5,
    denoise=1,
    hires_fix_denoise=0.5,
    hires_scale=2,
    img_url="",
    style=""
):

    token = os.environ.get("TOKEN_PIC")
    url = "https://piclumen.com/api/gen/create"

    headers = {
        "Host": "piclumen.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json;charset=UTF-8",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/image-generator/create",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Cuerpo de la solicitud JSON con parámetros editables
    payload = {
        "model_id": "34ec1b5a-8962-4a93-b047-68cec9691dc2",  # Modelo fijo
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "resolution": {
            "width": width,
            "height": height,
            "batch_size": batch_size  # Puedes ajustar si necesario
        },
        "model_ability": {
            "anime_style_control": None  # Valor fijo
        },
        "seed": seed,
        "steps": steps,
        "cfg": cfg,
        "sampler_name": "dpmpp_2m_sde_gpu",  # Valor fijo
        "scheduler": "karras",             # Valor fijo
        "ponyTags": {},                    # Valor fijo
        "denoise": denoise,
        "hires_fix_denoise": hires_fix_denoise,
        "hires_scale": hires_scale,
        "gen_mode": "quality",             # Valor fijo
        "img2img_info": {
            "img_url": img_url,
            "style": style,
            "weight": 0  # Valor fijo
        }
    }


    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)


    #print(response.text)

    # Manejar la respuesta
    if response.ok:
        # Extraer el markId de la respuesta
        response_data = response.json()

        mark_id = response_data.get('data', {}).get('markId', None)  # Extraer markId

        if mark_id:
           #resultado = procesar_tarea(mark_id)
           img_paths = procesar_tarea(mark_id)

        return mark_id, img_paths  # Devuelve el markId extraído
    else:
        return {"error": "Request failed", "details": "..."}, None