import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from background_listener import run_listener_in_thread, stop_listener
from utils.history import load_history, clear_history
from utils.config import load_config, save_config
import shutil
import os
import json
import markdown2
from tkhtmlview import HTMLLabel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoUploader - Google Drive")
        self.root.geometry("600x300")
        self.sidebar = ttk.Frame(root, width=200, bootstyle="secondary")
        self.sidebar.pack(side="left", fill="y")
        ttk.Button(self.sidebar, text="Página Inicial", command=self.show_home, width=20, bootstyle="outline-primary").pack(pady=10)
        ttk.Button(self.sidebar, text="Histórico", command=self.show_history, width=20, bootstyle="outline-primary").pack(pady=10)
        ttk.Button(self.sidebar, text="Configurações", command=self.show_config, width=20, bootstyle="outline-primary").pack(pady=10)
        ttk.Button(self.sidebar, text="Documentações", command=self.show_docs, width=20, bootstyle="outline-primary").pack(pady=10)
        ttk.Button(self.sidebar, text="Sair", command=root.quit, width=20, bootstyle="outline-danger").pack(pady=10)
        self.main_frame = ttk.Frame(root, bootstyle="light")
        self.main_frame.pack(side="right", expand=True, fill="both")
        self.listener_status = ttk.StringVar(value="Serviço parado")
        self.show_home()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Bem-vindo ao AutoUploader!", font=("Helvetica", 20), bootstyle="inverse-primary").pack(pady=20)
        ttk.Label(self.main_frame, text="Status do Serviço:", font=("Helvetica", 14), bootstyle="secondary").pack(pady=10)
        ttk.Label(self.main_frame, textvariable=self.listener_status, font=("Helvetica", 14), bootstyle="info").pack(pady=5)
        ttk.Button(self.main_frame, text="Iniciar Serviço", command=self.start_listener, width=20, bootstyle="success").pack(pady=10)
        ttk.Button(self.main_frame, text="Parar Serviço", command=self.stop_listener, width=20, bootstyle="danger").pack(pady=10)

    def show_docs(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Documentações", font=("Helvetica", 16), bootstyle="inverse-primary").pack(pady=10)
        docs_path = "docs"
        if not os.path.exists(docs_path):
            ttk.Label(self.main_frame, text="A pasta 'docs' não foi encontrada.", bootstyle="secondary").pack(pady=20)
            return
        docs_files = [f for f in os.listdir(docs_path) if f.endswith(".md")]
        if not docs_files:
            ttk.Label(self.main_frame, text="Nenhum arquivo Markdown encontrado na pasta 'docs'.", bootstyle="secondary").pack(pady=20)
            return
        for doc in docs_files:
            ttk.Button(self.main_frame, text=doc, command=lambda d=doc: self.open_doc(d), bootstyle="outline-primary").pack(pady=5)

    def open_doc(self, doc_name):
        docs_path = os.path.join("docs", doc_name)
        try:
            with open(docs_path, "r", encoding="utf-8") as file:
                content = file.read()
            html_content = markdown2.markdown(content)
            doc_window = ttk.Toplevel(self.root)
            doc_window.title(doc_name)
            doc_window.geometry("600x300")
            html_label = HTMLLabel(doc_window, html=html_content)
            html_label.pack(expand=True, fill="both")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")

    def show_history(self):
        self.clear_main_frame()
        history = load_history()
        if not history:
            ttk.Label(self.main_frame, text="Nenhum upload encontrado.", font=("Helvetica", 14), bootstyle="secondary").pack(pady=20)
            return
        ttk.Label(self.main_frame, text="Histórico de Uploads", font=("Helvetica", 16), bootstyle="inverse-primary").pack(pady=10)
        for record in history:
            ttk.Label(self.main_frame, text=f"{record['timestamp']}: {record['link']}", bootstyle="info").pack(anchor="w", padx=10)
        ttk.Button(self.main_frame, text="Limpar Histórico", command=self.clear_history, bootstyle="danger").pack(pady=10)

    def clear_history(self):
        if messagebox.askyesno("Confirmação", "Tem certeza de que deseja limpar o histórico?"):
            clear_history()
            messagebox.showinfo("Sucesso", "Histórico limpo com sucesso!")
            self.show_history()

    def show_config(self):
        self.clear_main_frame()
        ttk.Label(self.main_frame, text="Configurações", font=("Helvetica", 16), bootstyle="inverse-primary").pack(pady=10)
        ttk.Label(self.main_frame, text="ID da Pasta do Google Drive:", bootstyle="secondary").pack(pady=5)
        folder_id = ttk.StringVar(value=load_config().get("folder_id", ""))
        ttk.Entry(self.main_frame, textvariable=folder_id, width=50).pack(pady=5)
        def save():
            config = {"folder_id": folder_id.get()}
            save_config(config)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        ttk.Button(self.main_frame, text="Salvar", command=save, bootstyle="success").pack(pady=10)
        ttk.Label(self.main_frame, text="Upload do arquivo credentials.json:", bootstyle="secondary").pack(pady=10)
        ttk.Button(self.main_frame, text="Selecionar Arquivo", command=self.upload_credentials, width=20, bootstyle="primary").pack(pady=5)

    def upload_credentials(self):
        # Verifica se o arquivo credentials.json já existe
        credentials_path = "credentials.json"
        if not os.path.exists(credentials_path):
            # Cria um arquivo vazio se não existir
            with open(credentials_path, "w") as f:
                json.dump({}, f)
            messagebox.showinfo("Aviso", "O arquivo 'credentials.json' não foi encontrado. Um arquivo vazio foi criado. Por favor, envie o arquivo correto.")
            return
    
        # Permite ao usuário selecionar um novo arquivo de credenciais
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("Todos os Arquivos", "*.*")])
        if file_path:
            try:
                shutil.copy(file_path, credentials_path)
                messagebox.showinfo("Sucesso", "Arquivo 'credentials.json' carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")

    def start_listener(self):
        try:
            run_listener_in_thread()
            self.listener_status.set("Serviço em execução")
            messagebox.showinfo("Listener", "Serviço iniciado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar o serviço: {e}")

    def stop_listener(self):
        try:
            stop_listener()
            self.listener_status.set("Serviço parado")
            messagebox.showinfo("Listener", "Serviço parado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao parar o serviço: {e}")

if __name__ == "__main__":
    root = ttk.Window(themename="pulse")
    app = App(root)
    root.mainloop()