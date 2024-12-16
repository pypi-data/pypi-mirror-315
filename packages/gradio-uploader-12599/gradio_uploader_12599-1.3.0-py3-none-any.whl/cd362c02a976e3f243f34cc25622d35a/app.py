import os
from logs import *
import shutil
import gradio as gr
import random
import requests
import time
from IPython.display import Image, display
from flux import generar_imagen_flux
from linearv1 import generar_imagen_linearv1
from ponyv6 import generar_imagen_ponyv6
from realisticv2 import generar_imagen_realisticv2
from animev2 import generar_imagen_animev2
from pic_reg import configurar_usuario
from upscaler import upload_file_upscaler, upscale_image
from remove import remove_image, upload_file_remove
import subprocess
from PIL import Image
import cv2
import time
from flux_pro import gen_flux_pro_image

def load_flux_ration(selected_ration):
    # Mapeo de idiomas a directorios
    aspe_rations = {
        "1:1": "1024x1024",
        "16:9": "1344x768",
        "9:16": "768x1344",
        "4:3": "1280x960",
        "3:4": "960x1280"
    }
    resolution = aspe_rations.get(selected_ration)

    return resolution

def load_text_ranwey(selected_ration):
    # Mapeo de idiomas a directorios
    aspe_rations = {
        "16:9": "/tmp/16_9.png",
        "9:16": "/tmp/9_16.png"
    }
    resolution = aspe_rations.get(selected_ration)

    return resolution


# Función para crear el archivo .zip de la carpeta de imágenes
def create_zip_of_images_fluxpro():
        # Crear el archivo zip
        zip_filename = "/tmp/generated_fluxpro.zip"
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/img_flux_pro")  # Comprimir la carpeta

        # Devolver el archivo comprimido para ser descargado
        return zip_filename

    # Función para ejecutar cuando se presiona el botón "Save All"
def on_save_fluxpro_click():
        # Llamar a la función para crear el archivo zip
        zip_file = create_zip_of_images_fluxpro()

        # Devolver el archivo para que el componente gr.File pueda manejarlo
        return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga

# Función para ejecutar cuando se presiona el botón "Generate"
def on_generate_fluxpro_click(prompt, selected_ration, models_type):

        wid_hei = load_flux_ration(selected_ration)
        ancho, alto = map(int, wid_hei.split('x'))
        print(ancho)
        print(alto)
        width = ancho
        height = alto

        gen_flux_pro_image(prompt, width, height, selected_ration, models_type)
        video_output1 = os.environ.get("DIR_IMAGEE_FLUX_PRO")

        gen_flux_pro_image(prompt, width, height, selected_ration, models_type)
        video_output2 = os.environ.get("DIR_IMAGEE_FLUX_PRO")

        output_textbox3 = "Successful generation"

        # Devolver las actualizaciones
        return video_output1, video_output2, output_textbox3

def divide_seconds(minute):
    # Calcular segundos totales
    total_seconds = minute * 60
    # Calcular cuántos intervalos de 3 segundos caben
    intervals = total_seconds // 3  # Número de divisiones en intervalos de 3 segundos
    return intervals


def actualizar_length(tipo_model):
    if tipo_model == "Pro":
        return gr.update(visible=False, value="5")
    return gr.update(visible=True)


def process_upload_image2_runway(image):
    jpg_path2 = "/tmp/img_fragmento2.jpg"

    try:
        if image.format != "JPEG":
            image = image.convert("RGB")
        image.save(jpg_path2, "JPEG", quality=100)
        if os.path.exists(jpg_path2):
            print(f"Imagen guardada correctamente")

            # Obtener las dimensiones de la imagen
            width2, height2 = image.size

            # Guardar las coordenadas en un archivo de texto
            os.environ["WIDTH_IMG2"] = str(width2)
            os.environ["HEIGHT_IMG2"] = str(height2)
            os.environ["IMG2"] = jpg_path2

            print(f"Coordenadas guardadas correctamente")

    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")

# Función para unir videos numerados y limpiar la carpeta
def join_videos_and_clean(video_folder, output_file):
    try:
        # Verificar si la carpeta existe
        if not os.path.exists(video_folder):
            return "Error: La carpeta no existe.", None

        # Obtener y ordenar archivos MP4 numerados
        video_files = sorted([f for f in os.listdir(video_folder) if f.endswith(".mp4")])
        if not video_files:
            return "Error: No se encontraron archivos MP4 en la carpeta.", None

        # Crear archivo de lista para FFmpeg
        list_file_path = os.path.join(video_folder, "file_list.txt")
        with open(list_file_path, "w") as list_file:
            for video in video_files:
                list_file.write(f"file '{os.path.join(video_folder, video)}'\n")

        # Ejecutar FFmpeg para unir los videos
        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            output_file
        ]
        subprocess.run(command, check=True)

        # Eliminar archivo de lista temporal
        os.remove(list_file_path)

        # Eliminar los archivos MP4 de la carpeta después de la unión
        for video in video_files:
            os.remove(os.path.join(video_folder, video))

        return "Videos unidos y archivos eliminados exitosamente.", output_file
    except subprocess.CalledProcessError as e:
        return f"Error al unir los videos con FFmpeg: {str(e)}", None
    except Exception as e:
        return f"Error inesperado: {str(e)}", None

# Función para mostrar o ocultar el segundo cuadro de imagen
def activar_end_frame(activar):
    return gr.update(visible=activar)


def run_remove_img():

    remove_image()
    #time.sleep(1)
    directory_image_remove = os.environ.get("IMAGE_REMOVE")
    # Devuelve la ruta del video y un mensaje
    return directory_image_remove, "Successful climbing image"

def run_upscaler_img(scale):

    upscale_image(scale)
    #time.sleep(1)
    directory_image_upscaler = os.environ.get("IMAGE_UPSCALER")
    # Devuelve la ruta del video y un mensaje
    return directory_image_upscaler, "Successful climbing image"

def load_text_ration(selected_ration):
    # Mapeo de idiomas a directorios
    aspe_rations = {
        "1:1": "c",
        "16:9": "1344x768",
        "9:16": "768x1344",
        "4:3": "1152x896",
        "3:4": "896x1152",
        "3:2": "1216x832",
        "2:3": "832x1216",
        "8:5": "1216x768",
        "5:8": "768x1216",
        "19:9": "1472x704",
        "9:19": "704x1472",
        "21:9": "1536x640",
        "9:21": "640x1536"
    }
    resolution = aspe_rations.get(selected_ration)

    return resolution

# Función para actualizar los valores de sliders y el campo de texto según el modelo seleccionado
def update_model_settings(selected_model):
    settings = {
        "PicLumen Realistic V2": (4.5, 25, "NSFW, watermark"),
        "PicLumen Anime V2": (7.0, 25, "(nsfw:0.7), (worst quality:1.5), (low quality:1.5), (normal quality:1.5), lowres,watermark, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, username, blurry, artist name"),
        "PicLumen Lineart VI": (5.0, 22, "nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]"),
        "Pony Diffusion V6": (5.0, 22, ""),
        "FLUX.1": (5.0, 4, "")
    }

    scale, steps, negative_prompt = settings[selected_model]
    # Devuelve las actualizaciones para los sliders y el cuadro de texto
    return (
        gr.update(value=scale),
        gr.update(value=steps),
        gr.update(value=negative_prompt, visible=selected_model != "FLUX.1")
    )

# Función para mostrar o ocultar el segundo cuadro de imagen
def activar_seed(activar):
    return gr.update(visible=activar)

def toggle_negative_prompt_visibility(selected_model):
    """
    Muestra u oculta el campo negative_prompts según el modelo seleccionado.
    Si el modelo seleccionado es 'FLUX.1', el campo se oculta.
    """
    return gr.update(visible=selected_model != "FLUX.1")

# Función para procesar y guardar la imagen automáticamente en formato JPG
def process_and_save_image1(image):
    jpg_path = "/tmp/img_fragmento.jpg"

    try:
        if image.format != "JPEG":
            image = image.convert("RGB")
        image.save(jpg_path, "JPEG", quality=100)
        if os.path.exists(jpg_path):
            print(f"Imagen guardada correctamente")

            # Obtener las dimensiones de la imagen
            width, height = image.size

            os.environ["WIDTH_IMG_UPSCALER"] = str(width)
            os.environ["HEIGHT_IMG_UPSCALER"] = str(height)
            os.environ["ORIGINAL_IMG_UPSCALER"] = jpg_path
            print(jpg_path)

            # Ejecutar la función
            upload_file_upscaler(jpg_path)

            print(f"Coordenadas guardadas correctamente")

        return None
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return None

# Función para procesar y guardar la imagen automáticamente en formato JPG
def process_and_save_image2(image):
    jpg_path = "/tmp/img_fragmento.jpg"

    try:
        if image.format != "JPEG":
            image = image.convert("RGB")
        image.save(jpg_path, "JPEG", quality=100)
        if os.path.exists(jpg_path):
            print(f"Imagen guardada correctamente")

            # Obtener las dimensiones de la imagen
            width, height = image.size

            os.environ["WIDTH_IMG_REMOVE"] = str(width)
            os.environ["HEIGHT_IMG_REMOVE"] = str(height)
            os.environ["ORIGINAL_IMG_REMOVE"] = jpg_path
            print(jpg_path)

            # Ejecutar la función
            upload_file_remove(jpg_path)

            print(f"Coordenadas guardadas correctamente")

        return None
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return None


def up_save_button_click():
              # Llamar a la función para crear el archivo zip
              zip_file = up_zip_of_images()

              # Devolver el archivo para que el componente gr.File pueda manejarlo
              return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga

            # Función para crear el archivo .zip de la carpeta de imágenes
def up_zip_of_images():
                # Crear el archivo zip
                zip_filename = "/tmp/upscalers_images.zip"
                shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/img_upscaler")  # Comprimir la carpeta

                # Devolver el archivo comprimido para ser descargado
                return zip_filename

def rev_save_button_click():
              # Llamar a la función para crear el archivo zip
              zip_file = rev_zip_of_images()

              # Devolver el archivo para que el componente gr.File pueda manejarlo
              return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga

            # Función para crear el archivo .zip de la carpeta de imágenes
def rev_zip_of_images():
                # Crear el archivo zip
                zip_filename = "/tmp/remove_images.zip"
                shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/img_remove")  # Comprimir la carpeta

                # Devolver el archivo comprimido para ser descargado
                return zip_filename


# Función para crear el archivo .zip de la carpeta de imágenes
def create_zip_of_images():
        # Crear el archivo zip
        zip_filename = "/tmp/generated_images.zip"
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/images")  # Comprimir la carpeta

        # Devolver el archivo comprimido para ser descargado
        return zip_filename

    # Función para ejecutar cuando se presiona el botón "Save All"
def on_save_button_click():
        # Llamar a la función para crear el archivo zip
        zip_file = create_zip_of_images()

        # Devolver el archivo para que el componente gr.File pueda manejarlo
        return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga


    # Función para ejecutar cuando se presiona el botón "Generate"
def on_generate_button_click(prompt, batch_size, selected_ration, steps, hires_scale, seed_text, seed_fixed, models_type, negative_prompts):

        token = os.environ.get("TOKEN_PIC")
        if not token:
          configurar_usuario()
          token = os.environ.get("TOKEN_PIC")
          user_id = os.environ.get("USER_ID_PIC")
          #print("token:", token)
          #print("user_id", user_id)
        if models_type=="FLUX.1":
          negative_prompt = ""
        else:
          negative_prompt = negative_prompts

        if seed_fixed:
           seed = seed_text
        else:
           seed = random.randint(0, 73709551615)

        wid_hei = load_text_ration(selected_ration)

        ancho, alto = map(int, wid_hei.split('x'))

        print(ancho)
        print(alto)

        print(seed)

        width = ancho
        height = alto
        cfg = 7
        denoise = 1
        hires_fix_denoise = 0.6
        img_url = ""
        style = ""


        if models_type=="FLUX.1":
           mark_id, img_paths = generar_imagen_flux(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Realistic V2":
           mark_id, img_paths = generar_imagen_realisticv2(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Anime V2":
           mark_id, img_paths = generar_imagen_animev2(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Lineart VI":
           mark_id, img_paths = generar_imagen_linearv1(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="Pony Diffusion V6":
           mark_id, img_paths = generar_imagen_ponyv6(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        # Rellenar con None hasta llegar a 4 imágenes si es necesario
        while len(img_paths) < 4:
            img_paths.append(None)

        # Crear una lista de actualizaciones para cada imagen basada en el valor del slider
        image_updates = []

        # Hacer visibles las imágenes según el número seleccionado en el slider
        if batch_size >= 1:
            image_updates.append(gr.update(value=img_paths[0], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 2:
            image_updates.append(gr.update(value=img_paths[1], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 3:
            image_updates.append(gr.update(value=img_paths[2], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 4:
            image_updates.append(gr.update(value=img_paths[3], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        # Actualizar el output_textbox con el número de imágenes generadas
        image_updates.append(f"""
        Model: {models_type}\n
        Seed: {seed}\n
        Aspect Ratio: {selected_ration}\n
        Width: {ancho}\n
        Height: {alto}\n
        Steps: {steps}\n
        Guidance Scale: {hires_scale}\n
        Generated {batch_size} images for prompt: {prompt}\n
        Negative Prompt: {negative_prompts}
                             """)

        # Devolver las actualizaciones
        return image_updates
# Función para crear el archivo .zip de la carpeta de imágenes
def create_zip_of_images():
        # Crear el archivo zip
        zip_filename = "/tmp/generated_images.zip"
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/images")  # Comprimir la carpeta

        # Devolver el archivo comprimido para ser descargado
        return zip_filename

# Función para ejecutar cuando se presiona el botón "Save All"
def on_save_button_click():
        # Llamar a la función para crear el archivo zip
        zip_file = create_zip_of_images()

        # Devolver el archivo para que el componente gr.File pueda manejarlo
        return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga


# Función para ejecutar cuando se presiona el botón "Generate"
def on_generate_button_click(prompt, batch_size, selected_ration, steps, hires_scale, seed_text, seed_fixed, models_type, negative_prompts):

        token = os.environ.get("TOKEN_PIC")
        if not token:
          configurar_usuario()
          token = os.environ.get("TOKEN_PIC")
          user_id = os.environ.get("USER_ID_PIC")
          #print("token:", token)
          #print("user_id", user_id)
        if models_type=="FLUX.1":
          negative_prompt = ""
        else:
          negative_prompt = negative_prompts

        if seed_fixed:
           seed = seed_text
        else:
           seed = random.randint(0, 73709551615)

        wid_hei = load_text_ration(selected_ration)

        ancho, alto = map(int, wid_hei.split('x'))

        print(ancho)
        print(alto)

        print(seed)

        width = ancho
        height = alto
        cfg = 7
        denoise = 1
        hires_fix_denoise = 0.6
        img_url = ""
        style = ""


        if models_type=="FLUX.1":
           mark_id, img_paths = generar_imagen_flux(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Realistic V2":
           mark_id, img_paths = generar_imagen_realisticv2(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Anime V2":
           mark_id, img_paths = generar_imagen_animev2(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="PicLumen Lineart VI":
           mark_id, img_paths = generar_imagen_linearv1(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        if models_type=="Pony Diffusion V6":
           mark_id, img_paths = generar_imagen_ponyv6(prompt, negative_prompt, width, height, batch_size, seed, steps, cfg, denoise, hires_fix_denoise, hires_scale, img_url, style)

        # Rellenar con None hasta llegar a 4 imágenes si es necesario
        while len(img_paths) < 4:
            img_paths.append(None)

        # Crear una lista de actualizaciones para cada imagen basada en el valor del slider
        image_updates = []

        # Hacer visibles las imágenes según el número seleccionado en el slider
        if batch_size >= 1:
            image_updates.append(gr.update(value=img_paths[0], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 2:
            image_updates.append(gr.update(value=img_paths[1], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 3:
            image_updates.append(gr.update(value=img_paths[2], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        if batch_size >= 4:
            image_updates.append(gr.update(value=img_paths[3], visible=True))
        else:
            image_updates.append(gr.update(visible=False))

        # Actualizar el output_textbox con el número de imágenes generadas
        image_updates.append(f"""
        Model: {models_type}\n
        Seed: {seed}\n
        Aspect Ratio: {selected_ration}\n
        Width: {ancho}\n
        Height: {alto}\n
        Steps: {steps}\n
        Guidance Scale: {hires_scale}\n
        Generated {batch_size} images for prompt: {prompt}\n
        Negative Prompt: {negative_prompts}
                             """)

        # Devolver las actualizaciones
        return image_updates

# Función para habilitar/deshabilitar el botón "Create"
def toggle_create_button(img):
    if img is not None:
        return gr.update(interactive=True)  # Habilita el botón
    else:
        return gr.update(interactive=False)  # Deshabilita el botón

# Función para verificar el login y mostrar la interfaz de Gradio
def verify_and_show_data(api_key):
    # Verifica el login
    os.environ["API_KEY"] = api_key

    result, success = login_and_get_data()

    if success:
        # Si el login es exitoso, muestra el contenido de 'data'
        return gr.update(visible=False), gr.update(visible=True), f"Login exitoso. Contenido de 'data': {result}"  # Gradio UI visible
    else:
        # Si el login falla, muestra el mensaje de error
        return gr.update(visible=True), gr.update(visible=False), result  # Solo muestra el login

# Crear la interfaz de Gradio
def gradio_interface():
    with gr.Blocks() as demo:
        with gr.Row(visible=True) as login_row:  # Login visible al principio
            with gr.Column():
                gr.Markdown("<h2 style='text-align: center;'>Login</h2>")
                api_key_input = gr.Textbox(label="API Key", placeholder="Enter your API Key", type="text")
                login_button = gr.Button("Login")
                login_message = gr.Textbox(label="Resultado", interactive=False)

        with gr.Row(visible=False) as gradio_row:  # Esta fila será visible después del login exitoso
            with gr.Column():
              gr.Markdown("<h2 style='text-align: center;'>Curso AI</h2>")
              with gr.Tab("AI Image"):
                  with gr.TabItem("Text to Image"):
                      with gr.Row():
                          with gr.Column(scale=1):

                              models_type = gr.Dropdown(
                                  choices=["PicLumen Realistic V2", "PicLumen Anime V2", "PicLumen Lineart VI", "Pony Diffusion V6", "FLUX.1"],
                                  label="Models",
                                  value="FLUX.1",
                                  elem_id="models_type"
                              )

                              description_input3 = gr.Textbox(label="Prompt", placeholder="Enter text to begin creating a video", elem_id="description_input3")
                              batch_size_slider = gr.Slider(label="Number of Images", minimum=1, maximum=4, step=1, value=4, elem_id="batch_size_slider")

                              step_slider = gr.Slider(label="Steps", minimum=1, maximum=30, step=1, value=4, elem_id="batch_size_slider")

                              scale_slider = gr.Slider(minimum=1.0, maximum=30.0, step=0.1, value=5.0, label="Guidance Scale")

                              aspect_ratio_dropdown = gr.Dropdown(
                                  choices=["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "8:5", "5:8", "19:9", "9:19", "21:9", "9:21"],
                                  label="Aspect Ratio",
                                  value="16:9",
                                  elem_id="aspect_ratio_dropdown"
                              )

                              seed_fixed = gr.Checkbox(label="Seed Manual", value=False, visible=True)

                              seed_text = gr.Textbox(label="Seed", placeholder="Add your seed", value="0", visible=False)

                              negative_prompts = gr.Textbox(label="Negative Prompt", placeholder="Type your negative prompt", elem_id="negative_prompts", visible=False)

                              create_button3 = gr.Button("Generate", elem_id="create_button3")
                              save_button3 = gr.Button("Save All", elem_id="save_button3")  # Botón de guardado

                              # Log para mostrar el enlace de descarga
                              download_log = gr.File(label="Download Zip", elem_id="download_log", interactive=False)  # Usamos gr.File para descargar el archivo comprimido


                          # Videos y botones en el lado derecho
                          with gr.Column(scale=4):  # Ajusta el ancho de la columna de video
                              with gr.Row():  # Primera fila de imágenes
                                  with gr.Column():  # Contenedor para Video 1 y sus botones
                                      video_output1 = gr.Image(label="Image 1", height=250, visible=True)  # Inicialmente invisible
                                  with gr.Column():  # Contenedor para Video 2 y sus botones
                                      video_output2 = gr.Image(label="Image 2", height=250, visible=True)  # Inicialmente invisible

                              with gr.Row():  # Segunda fila de imágenes
                                  with gr.Column():  # Contenedor para Video 3 y sus botones
                                      video_output3 = gr.Image(label="Image 3", height=250, visible=True)  # Inicialmente invisible
                                  with gr.Column():  # Contenedor para Video 4 y sus botones
                                      video_output4 = gr.Image(label="Image 4", height=250, visible=True)  # Inicialmente invisible

                              output_textbox3 = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox3")  # Cambia el nombre del textbox


                      # Conectar la interfaz de usuario con la función de generación de imágenes
                      create_button3.click(
                      on_generate_button_click,
                      inputs=[description_input3, batch_size_slider, aspect_ratio_dropdown, step_slider, scale_slider, seed_text, seed_fixed, models_type, negative_prompts],  # Añadimos el slider como entrada
                      outputs=[video_output1, video_output2, video_output3, video_output4, output_textbox3]
                      )

                      seed_fixed.change(activar_seed, seed_fixed, seed_text)

                      # Conexión entre modelo y configuración dinámica
                      models_type.change(
                              update_model_settings,
                              inputs=[models_type],
                              outputs=[scale_slider, step_slider, negative_prompts]
                          )

                      # Conectar la interfaz de usuario con la función de guardado
                      save_button3.click(on_save_button_click, outputs=download_log)  # Devolver el archivo comprimido a gr.File






                  with gr.TabItem("Flux 1.1 Ultra Pro"):
                        with gr.Row():
                            with gr.Column(scale=1):

                                models_type = gr.Dropdown(
                                    choices=["flux-pro-1.1", "flux-pro-1.1-ultra"],
                                    label="Models",
                                    value="flux-pro-1.1",
                                    elem_id="models_type"
                                )


                                aspect_ratio_dropdown = gr.Dropdown(
                                    choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
                                    label="Aspect Ratio",
                                    value="16:9",
                                    elem_id="aspect_ratio_dropdown"
                                )

                                description_input3 = gr.Textbox(label="Prompt", placeholder="Enter text to begin creating a video", elem_id="description_input3")

                                create_button3 = gr.Button("Generate", elem_id="create_button3")
                                save_button3 = gr.Button("Save All", elem_id="save_button3")  # Botón de guardado

                                # Log para mostrar el enlace de descarga
                                download_log = gr.File(label="Download Zip", elem_id="download_log", interactive=False)  # Usamos gr.File para descargar el archivo comprimido


                            # Videos y botones en el lado derecho
                            with gr.Column(scale=4):  # Ajusta el ancho de la columna de video
                                with gr.Row():  # Primera fila de imágenes
                                    with gr.Column():  # Contenedor para Video 1 y sus botones
                                         video_output1 = gr.Image(label="Image 1", height=250, visible=True)  # Inicialmente invisible
                                    with gr.Column():  # Contenedor para Video 2 y sus botones
                                          video_output2 = gr.Image(label="Image 2", height=250, visible=True)  # Inicialmente invisible
                                output_textbox3 = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox3")  # Cambia el nombre del textbox


                        # Conectar la interfaz de usuario con la función de generación de imágenes
                        create_button3.click(
                        on_generate_fluxpro_click,
                        inputs=[description_input3, aspect_ratio_dropdown, models_type],  # Añadimos el slider como entrada
                        outputs=[video_output1, video_output2, output_textbox3]
                        )

                        # Conectar la interfaz de usuario con la función de guardado
                        save_button3.click(on_save_fluxpro_click, outputs=download_log)  # Devolver el archivo comprimido a gr.File


            
                  

                  with gr.TabItem("Image Upscaler"):
                      with gr.Row():
                          with gr.Column(scale=1):  # Nueva fila y columna con escala
                              # Fila para mostrar ambas imágenes cuando se activa subject, length, loop_video, prompt_upsampling
                              with gr.Row():
                                  # Imagen de inicio (carga de archivo)
                                  img1 = gr.Image(type="pil", label="Drag image here or select image", interactive=True,
                                                  elem_id="img1", width=200, height=200)  # Ajustar tamaño de la imagen


                              upscaler_slider = gr.Slider(label="Upscaler Images", minimum=2, maximum=4, step=2, value=2, elem_id="upscaler_slider")


                              upscaler_button = gr.Button("Upscaler", elem_id="upscaler_button")
                              save_up_button = gr.Button("Save", elem_id="save_button") # Botón de guardado

                              # Log para mostrar el enlace de descarga
                              download_up_log = gr.File(label="Download Zip", elem_id="download_log", interactive=False)  # Usamos gr.File para descargar el archivo comprimidov


                          with gr.Column(scale=3):  # Nueva fila y columna con escala
                              image_upscale_output = gr.Image(label="Image Upscale", elem_id="}image_upscaler")
                              output_textbox = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox") # Cambia el nombre del textbox

                      # Vincular botón al método
                      upscaler_button.click(
                          fn=run_upscaler_img,
                          inputs=[upscaler_slider],
                          outputs=[image_upscale_output, output_textbox]
                      )

                      img1.change(
                          fn=process_and_save_image1,
                          inputs=img1,
                          outputs=[]
                      )

                      save_up_button.click(up_save_button_click, outputs=download_up_log)




                  with gr.TabItem("Remove Background"):
                      with gr.Row():
                          with gr.Column(scale=1):  # Nueva fila y columna con escala
                              # Fila para mostrar ambas imágenes cuando se activa subject, length, loop_video, prompt_upsampling
                              with gr.Row():
                                  # Imagen de inicio (carga de archivo)
                                  img2 = gr.Image(type="pil", label="Drag image here or select image", interactive=True,
                                                  elem_id="img2", width=200, height=200)  # Ajustar tamaño de la imagen

                              remove_button = gr.Button("Remove", elem_id="remove_button")
                              save_rev_button = gr.Button("Save", elem_id="save_button") # Botón de guardado

                              # Log para mostrar el enlace de descarga
                              download_rev_log = gr.File(label="Download Zip", elem_id="download_log", interactive=False)  # Usamos gr.File para descargar el archivo comprimidov


                          with gr.Column(scale=3):  # Nueva fila y columna con escala
                              image_rev_output = gr.Image(label="Image remove", elem_id="image_remove", height=450)
                              output_textbox = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox") # Cambia el nombre del textbox

                      # Vincular botón al método
                      remove_button.click(
                          fn=run_remove_img,
                          inputs=[],
                          outputs=[image_rev_output, output_textbox]
                      )

                      img2.change(
                          fn=process_and_save_image2,
                          inputs=img2,
                          outputs=[]
                      )

                      save_rev_button.click(rev_save_button_click, outputs=download_rev_log)



        # Acción del login
        login_button.click(verify_and_show_data, inputs=[api_key_input], outputs=[login_row, gradio_row, login_message])


    demo.launch(inline=False, debug=True, share=True)

# Llamar a la función para lanzar la interfaz de Gradio
gradio_interface()