import customtkinter as ctk
import requests
import unicodedata
import random

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Bibble - Pokédex")
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
        self.text_area.insert(ctk.END, "Oi! Eu sou o Bibble. Digite o nome do Pokémon e eu te conto tudo sobre ele!\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite o nome do Pokémon...")
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
        self.text_area.insert(ctk.END, "\nVocê: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        # Processar a entrada do usuário
        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nBibble: " + response + "\n")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def normalize_string(self, s):
        # Remover acentos e converter para minúsculas
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()

    def get_response(self, user_input):
        user_input_normalized = self.normalize_string(user_input)
        
        prepositions = ["de", "do", "da"]
        tokens = [word for word in user_input_normalized.split() if word not in prepositions]

        if "olá" in tokens or "oi" in tokens:
            return "Olá! Em que posso ajudar?"
        elif "tchau" in tokens or "até logo" in tokens:
            return "Até mais! Se precisar de algo, estou aqui."
        elif "como" in tokens and ("você" in tokens or "está" in tokens):
            return "Estou ótima, obrigada por perguntar!"
        elif "qual" in tokens and "nome" in tokens:
            return "Eu sou o Bibble, sua assistente virtual."
        elif "ajuda" in tokens or "socorro" in tokens:
            return "Claro! Estou aqui para ajudar. O que você precisa?"

        greetings = ["Que legal", "Eba", "Que massa", "Uhul", "Oba", "Show"]
        frases = [
            "Aqui está!", "Encontrei!", "Acho que tenho aqui!",
            "Hum...acho que temos algo aqui!", "Encontrei algo aqui!",
            "Confira o que encontrei!", "Achei algo interessante!",
            "Veja só o que eu encontrei!", "Aqui está o que eu achei!",
            "Parece que encontrei a informação!", "Achei o que você precisa!",
            "Parece que tenho a resposta para você!", "Olha só o que encontrei!",
            "Tenho algo que pode te ajudar!", "Veja o que eu achei para você!",
            "Aqui está o que consegui encontrar!"
        ]

        synonyms = {
            "types": ["tipo", "tipos", "categoria", "classe"],
            "weight": ["peso", "massa", "peso em kg"],
            "height": ["altura", "tamanho", "estatura"]
        }

        attribute_requested = None
        pokemon_name = None

        for token in tokens:
            for key, syns in synonyms.items():
                if token in syns:
                    attribute_requested = key
                    break

        if not attribute_requested:
            pokemon_name = ' '.join(tokens)
        else:
            pokemon_name = ' '.join([token for token in tokens if token not in synonyms[attribute_requested]])

        if pokemon_name:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.strip()}")
                if response.status_code == 200:
                    data = response.json()
                    nome = data['name'].capitalize()
                    tipo = ', '.join([t['type']['name'].capitalize() for t in data['types']])
                    peso = data['weight'] / 10
                    altura = data['height'] / 10 

                    if attribute_requested:
                        if attribute_requested == "types":
                            return f"{random.choice(greetings)}! {random.choice(frases)} 🎉 \nNome: {nome} \nTipo: {tipo}"
                        elif attribute_requested == "weight":
                            return f"{random.choice(greetings)}! {random.choice(frases)} 🎉 \nNome: {nome} \nPeso: {peso} kg"
                        elif attribute_requested == "height":
                            return f"{random.choice(greetings)}! {random.choice(frases)} 🎉 \nNome: {nome} \nAltura: {altura} m"

                    return (
                        f"{random.choice(greetings)}! {random.choice(frases)} 🎉 \n"
                        f"Nome: {nome} \nTipo: {tipo} \nPeso: {peso} kg \nAltura: {altura} m"
                    )
                elif response.status_code == 404:
                    return "Hmm, não achei esse Pokémon... Tem certeza que digitou o nome certo? 🧐"
                else:
                    return "Oh, desculpe! Não consegui acessar a API agora. Tenta de novo mais tarde, tá bom? 😢"
            except requests.exceptions.RequestException as e:
                return f"Ops, deu problema na conexão com a API: {e}. 😖"

        return "Desculpe, não entendi. Poderia reformular a pergunta?"


if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
