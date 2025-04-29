# AutoUploader - Passo a Passo de Compilação

Este guia fornece um passo a passo para compilar e rodar o projeto **AutoUploader**, uma ferramenta que permite capturar prints da tela, fazer upload para o Google Drive e gerenciar os links de forma simples. Abaixo estão as etapas para compilar o projeto e colocá-lo em funcionamento.

## Pré-requisitos

Antes de iniciar o processo de compilação, é necessário garantir que as seguintes ferramentas estejam instaladas:

1. **Python 3.x** (recomendado: versão 3.8 ou superior)
2. **Pip** (gerenciador de pacotes Python)
3. **Streamlit** (para a interface web)
4. **PyInstaller** (para compilar o projeto como executável)
5. **Google Cloud API** (para configurar a API do Google Drive)
6. **Bibliotecas do Python**: `pyautogui`, `Pillow`, `pyperclip`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, entre outras.

## Passo 1: Clone o repositório

Primeiro, clone o repositório para o seu computador:

```bash
git clone https://github.com/seu-usuario/AutoUploader.git
cd AutoUploader
```

## Passo 2: Crie um ambiente virtual

Crie e ative um ambiente virtual para evitar conflitos com outras dependências do sistema:

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows
```

## Passo 3: Instale as dependências

Instale as bibliotecas necessárias utilizando o `pip`:

```bash
pip install -r requirements.txt
```

## Passo 4: Criar executável
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --add-data "credentials.json;." --add-data "config.json;." main.py
```