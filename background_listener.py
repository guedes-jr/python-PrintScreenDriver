import os
import time
from datetime import datetime
from pynput import keyboard
from PIL import ImageGrab, Image
import threading
import pyperclip
import pymsgbox
from utils.drive import upload_image_and_get_link
from utils.config import load_config
from utils.history import add_to_history
from io import BytesIO
import win32clipboard
import queue
import hashlib

TEMP_IMAGE = "last_capture.png"
listener_running = False
listener_thread = None
keyboard_listener = None
event_queue = queue.Queue()  # Fila para comunicação entre threads
denied_images = set()  # Conjunto para armazenar hashes de imagens negadas

def get_clipboard_image():
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            image = Image.open(BytesIO(data))
            win32clipboard.CloseClipboard()
            return image
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(f"Erro ao acessar a área de transferência: {e}")
    return None

def save_clipboard_image():
    image = get_clipboard_image()
    if image:
        try:
            image.save(TEMP_IMAGE)
            return TEMP_IMAGE
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
    return None

def calculate_image_hash(image_path):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
            return hashlib.sha256(image_data).hexdigest()
    except Exception as e:
        print(f"Erro ao calcular o hash da imagem: {e}")
    return None

last_image_hash = None  # Novo: para guardar o hash da última imagem processada (aceita ou negada)

def on_press(key):
    global listener_running, last_image_hash
    if not listener_running:
        print("Listener está desativado. Ignorando eventos de teclado.")
        return

    if key == keyboard.Key.print_screen:
        print("PrintScreen pressionado.")
        for _ in range(20):  # Tenta por até 10 segundos
            path = save_clipboard_image()
            if path:
                print("Imagem capturada e salva.")
                image_hash = calculate_image_hash(path)
                if image_hash:
                    if image_hash == last_image_hash:
                        print("Imagem já processada anteriormente. Aguardando nova imagem...")
                    elif image_hash in denied_images:
                        print("Imagem já foi negada anteriormente.")
                    else:
                        last_image_hash = image_hash
                        event_queue.put((path, image_hash))
                        break
            time.sleep(0.5)
        else:
            print("Nenhuma nova imagem encontrada na área de transferência.")


def handle_upload_in_main_thread():
    while True:
        try:
            path, image_hash = event_queue.get(block=True)  # Aguarda por eventos na fila
            user_choice = pymsgbox.confirm("Deseja enviar a captura para o Google Drive?", "Upload", ["Sim", "Não"])
            if user_choice == "Sim":
                config = load_config()
                folder_id = config.get("folder_id")
                if not folder_id:
                    pymsgbox.alert("Erro: ID da pasta do Google Drive não está configurado.")
                    continue

                link = upload_image_and_get_link(path, folder_id)
                pyperclip.copy(link)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                add_to_history(timestamp, link)
                pymsgbox.alert("Upload concluído! Link copiado para a área de transferência.")
            elif user_choice == "Não":
                denied_images.add(image_hash)  # Armazena o hash da imagem negada
                print(f"Imagem negada: {image_hash}")
        except Exception as e:
            print(f"Erro ao processar o upload: {e}")
        finally:
            # Garante que o listener continue processando eventos após uma imagem ser negada
            listener_running = True

def start_listener():
    global listener_running, keyboard_listener
    listener_running = True
    print("Listener iniciado.")
    try:
        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()
        keyboard_listener.join()
    except Exception as e:
        print(f"Erro ao iniciar o listener: {e}")
    finally:
        listener_running = False

def stop_listener():
    global listener_running, listener_thread, keyboard_listener
    listener_running = False
    print("Listener pausado.")
    if keyboard_listener is not None:
        keyboard_listener.stop()
        keyboard_listener = None
    if listener_thread is not None and listener_thread.is_alive():
        listener_thread.join(timeout=1)
        print("Thread do listener encerrada.")
        listener_thread = None

def run_listener_in_thread():
    global listener_thread
    if listener_thread is None or not listener_thread.is_alive():
        listener_thread = threading.Thread(target=start_listener, daemon=True)
        listener_thread.start()
        print("Listener executando em thread separada.")
    else:
        print("Listener já está ativo.")

# Inicia a thread principal para processar eventos da fila
main_thread = threading.Thread(target=handle_upload_in_main_thread, daemon=True)
main_thread.start()