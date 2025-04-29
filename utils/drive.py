import os
import sys
import json
import shutil
from tkinter import Tk, filedialog, messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Determina o diretório base
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Função para solicitar o arquivo de credenciais ao usuário
def request_credentials_file():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    messagebox.showinfo("Configuração Inicial", "Por favor, selecione o arquivo 'credentials.json'.")
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("Todos os Arquivos", "*.*")])
    if not file_path:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado. O programa será encerrado.")
        root.destroy()
        exit()
    try:
        shutil.copy(file_path, SERVICE_ACCOUNT_FILE)
        messagebox.showinfo("Sucesso", f"Arquivo '{SERVICE_ACCOUNT_FILE}' carregado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")
        root.destroy()
        exit()
    root.destroy()

# Função para validar o arquivo de credenciais
def validate_credentials_file():
    try:
        with open(SERVICE_ACCOUNT_FILE, "r") as f:
            data = json.load(f)
        required_fields = ["client_email", "token_uri", "private_key"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise Exception(f"Campo obrigatório '{field}' ausente ou vazio no arquivo de credenciais.")
    except json.JSONDecodeError:
        raise Exception(f"O arquivo '{SERVICE_ACCOUNT_FILE}' está vazio ou corrompido. Envie um arquivo válido.")
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{SERVICE_ACCOUNT_FILE}' não foi encontrado. Certifique-se de que ele está no diretório correto.")

# Função para carregar as credenciais do arquivo atualizado
def load_credentials():
    try:
        return service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        raise Exception(f"Erro ao carregar as credenciais: {e}")

# Verifica se o arquivo credentials.json existe, caso contrário solicita o arquivo ao usuário
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    request_credentials_file()
else:
    try:
        validate_credentials_file()
    except Exception as e:
        print(f"Erro na validação do arquivo de credenciais: {e}")
        print("Solicitando novas credenciais...")
        request_credentials_file()

def upload_image_and_get_link(file_path, folder_id):
    try:
        # Recarrega as credenciais antes de cada operação
        credentials = load_credentials()
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
        media = MediaFileUpload(file_path, mimetype="image/png")

        file = service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()

        file_id = file.get("id")
        service.permissions().create(
            fileId=file_id, body={"role": "reader", "type": "anyone"}
        ).execute()

        link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        return link

    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado. Verifique o caminho e tente novamente.")
    except Exception as e:
        raise Exception(f"Erro ao fazer upload para o Google Drive: {e}")