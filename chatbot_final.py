import spacy
import customtkinter as ctk
import requests
import random
import unicodedata

nlp = spacy.load("pt_core_news_sm")

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Bibble - Pokédex")
        master.geometry("600x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Oi! Eu sou o Bibble. Digite o nome do Pokémon e eu te conto tudo sobre ele!\n")
        self.text_area.configure(state="disabled")

        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite o nome do Pokémon...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="purple", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

    def normalize_string(self, s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()

    def extract_info(self, user_input):
        doc = nlp(self.normalize_string(user_input))

        pokemon_name = None
        attribute = None

        for token in doc:
            if token.pos_ in ["PROPN", "NOUN"]:
                if not pokemon_name and token.text.lower() not in ["peso", "altura", "tipo"]:
                    pokemon_name = token.text

            if token.text.lower() in ["peso", "altura", "tipo", "categorias", "tamanho", "estatura"]:
                if "peso" in token.text:
                    attribute = "weight"
                elif "altura" in token.text or "estatura" in token.text:
                    attribute = "height"
                elif "tipo" in token.text or "categorias" in token.text:
                    attribute = "types"

        return pokemon_name, attribute

    def get_response(self, user_input):
        pokemon_name, attribute_requested = self.extract_info(user_input)

        if not pokemon_name:
            return "Desculpe, não consegui identificar o Pokémon. Tente reformular a pergunta."

        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.strip()}")
            if response.status_code == 200:
                data = response.json()
                nome = data['name'].capitalize()
                tipo = ', '.join([t['type']['name'].capitalize() for t in data['types']])
                peso = data['weight'] / 10
                altura = data['height'] / 10

                greetings = ["Que legal", "Eba", "Que massa", "Uhul", "Oba", "Show"]
                frases = [
                    "Aqui está!", "Encontrei!", "Acho que tenho aqui!",
                    "Hum...acho que temos algo aqui!", "Encontrei algo aqui!",
                ]

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

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nVocê: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "\nBibble: " + response + "\n")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)


if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
