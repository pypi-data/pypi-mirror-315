import requests
import os
import re
import time
import hashlib
import json
import random
import string

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

def enviar_formulario():
    url = 'https://email-fake.com/'

    datos = {'campo_correo': 'ejemplo@dominio.com'}

    """Envía una solicitud POST a un formulario web."""
    response = requests.post(url, data=datos)
    return response.text

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio




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
    #print(response.text)

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


def registrar_usuario(account, password, validate_code):
    url = "https://piclumen.com/api/user/register"

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": "",  # Agrega tu token aquí si es necesario
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json;charset=UTF-8",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/account",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate"
    }

    # Generar el hash MD5 para la contraseña
    #hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Cuerpo de la solicitud
    payload = {
        "account": account,
        "password": password,
        "validateCode": validate_code
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)

    # Manejar la respuesta
    #print(response.headers)
    #print(response.json())

    if 'success' in response.text:
        #print("La palabra 'success' está presente en el mensaje.")

        token, user_id = iniciar_sesion(account, password)

        return token, user_id

    elif 'deleted' in response.text:
        #print("La palabra 'deleted' está presente en el mensaje.")
     
        return None,  None
    else:
        #print("Ni 'success' ni 'deleted' están presentes en el mensaje.")
        return None,  None
    
    #status  = print_email_message(response.text)
    return None,  None


COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}

def extract_verification_code(html_content):
    """
    Extrae el código de verificación de un contenido HTML dado.
    
    Args:
        html_content (str): El texto HTML que contiene el código de verificación.
    
    Returns:
        str: El código de verificación como una cadena, o None si no se encuentra.
    """
    pattern = r"Your verification code is ：(\d+)"
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)  # Retorna solo el número
    return None  # Retorna None si no encuentra el código

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
        print("Wait...")
        return True
    else:
        print("Error...")
        return False

def get_verification_code(username_email, dominios_dropdown):
    """Obtiene el código de verificación del correo y el identificador."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        **COMMON_HEADERS,
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Cookie': f'surl={dominios_dropdown}%2F{username_email}',
    }

    response = requests.get(url, headers=headers)

    verification_code = extract_verification_code(response.text)
    
    # Utiliza una expresión regular para encontrar el identificador largo
    identifier_match = re.search(r'delll:\s*"([a-zA-Z0-9]+)"', response.text)
    #return identifier_match, verification_code

    # Extrae y retorna los valores si fueron encontrados
    if identifier_match:
        identifier = identifier_match.group(1)
        return verification_code, identifier
    else:
        return None, None, None 

import time

def enviar_codigo_registro():
    correo = os.environ.get("USER_EMAIL_PIC")
    password = os.environ.get("PASS_WORD_PIC")
    #print(correo)
    #print(password)

    name, domain = correo.split('@')

    url = "https://piclumen.com/api/user/register-send-code"

    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "Authorization": "",  # Agrega tu token aquí si es necesario
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryPiHCBk7u93JxSMB2",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://piclumen.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://piclumen.com/app/account",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    }

    # Formato exacto del cuerpo de la solicitud con correo como variable
    payload = (
        f"------WebKitFormBoundaryPiHCBk7u93JxSMB2\r\n"
        f"Content-Disposition: form-data; name=\"account\"\r\n\r\n"
        f"{correo}\r\n"
        f"------WebKitFormBoundaryPiHCBk7u93JxSMB2--\r\n"
    )

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=payload)
    #print(response.text)
    if 'success' in response.text:
        print("Request sent successfully. Looking for verification code...")
        
        attempts = 0
        verification_code, identifier = None, None
        
        # Reintentar hasta 6 veces
        while attempts < 6:
            verification_code, identifier = get_verification_code(name, domain)
            if verification_code:  # Si se obtiene el código, salir del bucle
                break
            attempts += 1
            time.sleep(3)  # Esperar 3 segundos antes del siguiente intento

        if verification_code:
            #print("Código de verificación obtenido:", verification_code)
            #print("Identificador:", identifier)

            # Borrar el correo temporal asociado al identifier
            delete_temp_mail(name, domain, identifier)

            time.sleep(1)
            #print("CORREEO", correo)
            #print("PASS", password)
            #print("CODE", verification_code)
            # Registrar el usuario con el código de verificación
            token, user_id = registrar_usuario(correo, password, verification_code)

            return token, user_id

    print("process failed.")
    return None, None


def configurar_usuario():
    # Generar el nombre de usuario
    user_name = generar_nombre_completo()
    
    # Obtener el dominio de usuario
    domain_user = obtener_sitio_web_aleatorio(enviar_formulario())
    
    # Crear el correo electrónico del usuario
    user_emails = f"{user_name}@{domain_user}"
    
    # Contraseña (puede venir de otro lugar si es necesario)
    passwords = "c3b974a9b96984fabe65b5ee44a6a6cc" 
    
    # Configurar las variables de entorno
    os.environ["USER_EMAIL_PIC"] = user_emails
    os.environ["PASS_WORD_PIC"] = passwords
    
    # Enviar código de registro
    tokens, user_ids = enviar_codigo_registro()
    
    # Validar los resultados y configurar más variables de entorno
    if tokens and user_ids:
        os.environ["USER_ID_PIC"] = user_ids
        os.environ["TOKEN_PIC"] = tokens
    else:
        print("Connecting API...")
        configurar_usuario()