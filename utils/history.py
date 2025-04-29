import os
import json

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)  # Escreve uma lista vazia no arquivo
        else:
            print(f"Arquivo {HISTORY_FILE} não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao limpar o histórico: {e}")

def add_to_history(timestamp, link):
    try:
        history = load_history()
        history.append({"timestamp": timestamp, "link": link})

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        raise Exception(f"Erro ao adicionar ao histórico: {e}")