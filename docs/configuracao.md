
# Passo a Passo de Configuração do AutoUploader

Este guia detalha como configurar corretamente o projeto **AutoUploader** para que ele funcione de maneira eficiente em seu sistema. As etapas incluem a configuração das credenciais do Google Drive, variáveis de ambiente e ajustes no código.

## 1. Obtenção das Credenciais do Google Drive

### 1.1 Acesse o Console de Desenvolvedor do Google

1. Vá para o [Console de Desenvolvedor do Google](https://console.developers.google.com/).
2. Crie um **Novo Projeto** clicando em **Criar Projeto**.
3. Escolha um nome para o projeto e clique em **Criar**.

### 1.2 Habilite a API do Google Drive

1. No painel do projeto, no menu lateral esquerdo, selecione **Bibliotecas**.
2. Pesquise por "Google Drive API" e clique em **Habilitar**.
3. Isso permitirá que seu aplicativo interaja com o Google Drive.

### 1.3 Criação das Credenciais de OAuth 2.0

1. No painel de navegação, selecione **Credenciais**.
2. Clique em **Criar Credenciais** e escolha **ID do Cliente OAuth**.
3. Escolha **Aplicativo Desktop** como tipo de aplicação.
4. Salve e baixe o arquivo **`credentials.json`**.

O arquivo **`credentials.json`** contém as informações necessárias para autenticar a aplicação com a API do Google Drive.

## 2. Configuração do `config.json`

### 2.1 Criação do Arquivo `config.json`

Na raiz do seu projeto, crie um arquivo chamado **`config.json`** com a seguinte estrutura:

```json
{
  "drive_folder_id": "SEU_ID_DA_PASTA",
  "client_secrets_file": "credentials.json"
}
```

- **drive_folder_id**: O **ID da pasta** do Google Drive onde as imagens serão salvas. Para obter o ID da pasta, veja o passo abaixo.
- **client_secrets_file**: O nome do arquivo de credenciais baixado do Google.

### 2.2 Como Obter o ID da Pasta no Google Drive

1. Abra o **Google Drive** no seu navegador.
2. Crie uma nova pasta ou escolha uma pasta existente onde deseja salvar as imagens.
3. Abra a pasta e copie a **parte final da URL**. O ID da pasta é o valor presente após `folders/` na URL. Exemplo:

```
https://drive.google.com/drive/folders/ID_DA_PASTA
```

No exemplo acima, **`ID_DA_PASTA`** é o ID da pasta.

### 2.3 Salve o Arquivo

Coloque o arquivo **`config.json`** na raiz do seu projeto, ao lado do arquivo **`main.py`**.

## 3. Configuração das Variáveis de Ambiente

Para configurar as variáveis de ambiente (como o ID da pasta), edite o arquivo **`config.py`** (ou crie um novo, se não existir). No arquivo **`config.py`**, adicione a leitura do arquivo **`config.json`** para carregar as variáveis necessárias.

Exemplo de configuração em **`config.py`**:

```python
import json

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config
```

Com isso, seu código será capaz de acessar as configurações do **Google Drive** automaticamente.

## 4. Configuração do Histórico de Capturas

O histórico de capturas será armazenado em um arquivo JSON para rastrear os uploads feitos.

### 4.1 Criar o Arquivo de Histórico

Na raiz do projeto, crie um arquivo chamado **`history.json`**. Este arquivo será usado para armazenar o histórico de uploads.

Exemplo de estrutura do arquivo **`history.json`**:

```json
[
  {
    "timestamp": "2025-04-20 14:30",
    "link": "https://drive.google.com/file/d/ID_DO_ARQUIVO"
  }
]
```

### 4.2 Configuração do Histórico no Código

No arquivo **`history.py`**, crie funções para carregar e adicionar novas entradas ao histórico. Exemplo de código:

```python
import json

def load_history():
    try:
        with open('history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_to_history(link):
    history = load_history()
    history.append({"timestamp": "2025-04-20 14:30", "link": link})
    with open('history.json', 'w') as f:
        json.dump(history, f)
```

## 5. Teste de Configuração

Agora que as configurações foram feitas, é hora de testar se o programa está funcionando corretamente.

1. **Teste do Upload**: Execute o código e faça um print na tela. O arquivo será enviado para o Google Drive e o link será exibido.
2. **Verifique o Histórico**: Certifique-se de que o link gerado pelo upload aparece corretamente no arquivo **`history.json`**.

## 6. Ajustes Finais

Se o sistema está funcionando corretamente, você pode continuar com a integração do Streamlit, o que permitirá que os usuários interajam com a interface de forma mais amigável.

---

## Conclusão

Com este guia, você configurou corretamente a integração com o Google Drive e o armazenamento de histórico de capturas. Agora, o **AutoUploader** está pronto para capturar prints, fazer upload para o Google Drive e gerenciar os links gerados automaticamente!

Se precisar de mais ajuda ou ajustes, fique à vontade para entrar em contato!
```

---

### 🌟 Explicação do Passo a Passo:

1. **Configuração das Credenciais**: O primeiro passo envolve obter as credenciais do Google para permitir que o seu projeto interaja com o Google Drive, utilizando a API do Google.
2. **Configuração do Arquivo `config.json`**: Aqui, o ID da pasta do Google Drive é configurado junto com o caminho do arquivo `credentials.json`.
3. **Configuração do Histórico**: O histórico de links capturados é armazenado em um arquivo JSON, permitindo a persistência dos dados.
4. **Testes**: Após configurar, o passo final é testar o funcionamento do upload e o registro no histórico.

Com este guia, você terá configurado corretamente o seu projeto e estará pronto para utilizar o **AutoUploader**!