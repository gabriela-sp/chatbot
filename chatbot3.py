import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import random

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Bibble - Inventário de Produtos")
        master.geometry("600x500")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Oi! Eu sou o Bibble. Digite o nome do produto e eu te conto tudo sobre ele!\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite o nome do produto...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="purple", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        # Processar a entrada do usuário
        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Bibble: " + response + "\n")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def normalize_string(self, s):
        # Remover acentos e converter para minúsculas
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()

    def get_response(self, user_input):
        user_input_normalized = self.normalize_string(user_input)
        greetings = ["Oi", "Eba", "Que bom te ver"]

        try:
            response = requests.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vRJsg28ooUOXs__BXP7hgXPl_uJ_bBqM6UOsj4Pd_bjWYvRgxXsI2QOZBu24TDVAzewrmvvDzQQcXJq/pubhtml")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr')

                suggestions = []
                for row in rows[1:]:  
                    cells = row.find_all('td')
                    produto = cells[0].get_text().strip()
                    produto_normalized = self.normalize_string(produto)

                    if re.search(r'\b' + re.escape(produto_normalized) + r'\b', user_input_normalized):
                        quantidade = cells[1].get_text().strip()
                        preco = cells[2].get_text().strip()
                        return f"{random.choice(greetings)}! Achei o produto! 🎉 Produto: {produto}, Quantidade: {quantidade}, Preço: R$ {preco} 😍"
                    elif user_input_normalized in produto_normalized:
                        suggestions.append(produto)

                if suggestions:
                    return f"Não achei exatamente o que você quer, mas será que algum desses serve? {', '.join(suggestions)}. 😅"
                return "Hmm, não achei o produto... pode tentar outro nome ou me dar mais detalhes? 🙏"

            else:
                return "Oh, desculpe! Não consegui acessar a tabela agora. Tenta de novo mais tarde, tá bom? 😢"
        except requests.exceptions.RequestException as e:
            return f"Ops, deu problema na conexão com a tabela: {e}. 😖"

if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
