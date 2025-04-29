### 🖥️ **AutoUploader - Funcionalidades Planejadas**

#### 🎯 Objetivo
Automatizar o processo de captura de tela e envio para o Google Drive com link copiado para a área de transferência, com uma interface gráfica feita em **Streamlit**.

---

### ✅ **Funcionalidades**

#### 🖱️ Automatização
- Monitorar tecla `PrintScreen`
- Perguntar ao usuário se deseja fazer upload
- Enviar para o Google Drive e obter link público
- Copiar link automaticamente para área de transferência

#### 📋 Histórico
- Exibir lista com:
  - Data/hora da captura
  - Link do arquivo no Drive
  - Possibilidade de copiar o link novamente

#### ⚙️ Configurações
- Interface para upload do `credentials.json`
- Campo para definir pasta destino no Google Drive
- Armazenamento local das configurações

#### 📚 Tutorial
- Sessão com instruções passo a passo:
  - Primeira configuração (Google API)
  - Como usar o programa
  - Onde encontrar as capturas

---

### 🛠️ **Tecnologias**

- **Python**
- **Streamlit** (interface)
- **Google Drive API** (upload + compartilhamento)
- **Pynput** (listener de teclado)
- **Pillow** (captura de imagem)
- **Pyperclip** (copiar link para área de transferência)
- **PyInstaller** (gerar executável Windows)

---

### 🧱 Estrutura do Projeto

```
AutoUploader/
│
├── background_listener.py   # Listener para capturar a tecla PrintScreen
├── main.py                  # Interface principal com Streamlit
├── requeriments.txt         # Lista de dependências do projeto
├── config.json              # Configurações do usuário (vazio no momento)
├── credentials.json         # Credenciais da API do Google Drive
├── history.json             # Histórico de uploads (vazio no momento)
├── LICENSE                  # Licença do projeto (vazio no momento)
│
├── docs/                    # Documentação do projeto
│   ├── configuracao.md      # Guia de configuração do AutoUploader
│   ├── compilacao.md        # Guia de compilação do projeto
│   └── uso.md               # Guia de uso (vazio no momento)
│
├── utils/                   # Funções utilitárias
│   ├── clipboard.py         # (vazio no momento)
│   ├── config.py            # Gerenciamento de configurações
│   ├── drive.py             # Integração com o Google Drive
│   ├── history.py           # Gerenciamento do histórico de uploads
│   └── image.py             # (vazio no momento)
```

---

### 🔜 Próximo Passo

1. **Atualizar arquitetura com base nessa nova estrutura**
2. **Implementar a interface com Streamlit** com abas para:
   - Dashboard / Histórico
   - Configurações
   - Tutorial
3. **Integrar o background listener ao sistema principal**
4. **Gerar o executável com PyInstaller**
5. **Criar um instalador para Windows (opcional: Inno Setup)**