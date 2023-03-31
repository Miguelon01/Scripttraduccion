import requests
import csv
import json
from bs4 import BeautifulSoup

# Define la función para traducir el texto utilizando la API de Google
def translate_text(text, target_language='es'):
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q={}".format(text)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        if len(data) > 0 and len(data[0]) > 0 and len(data[0][0]) > 0:
            translation = data[0][0][0]
            return translation
        else:
            return "Translation not found"
    else:
        return "Error: {}".format(response.status_code)


text_to_translate = ""
translated_text = translate_text(text_to_translate)
print(translated_text)


# Define el archivo CSV que se va a leer y el archivo de salida
input_file = 'C:\\Users\\migue\\Documents\\Dialogues.csv'
output_file = 'C:\\Users\\migue\\Documents\\Dialogues-Traduction.csv'

# Abre el archivo de entrada
with open(input_file, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    # Crea el archivo de salida
    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        # Lee cada línea del archivo de entrada
        for row in reader:
            # Traduce cada frase en la fila
            translated_row = []
            for text in row:
                if not text.startswith(('http', 'https', '<?php')):
                    # Extrae el texto del elemento HTML si es necesario
                    soup = BeautifulSoup(text, 'html.parser')
                    text_to_translate = soup.get_text() if soup else text
                    # Traduce el texto
                    translated_text = translate_text(text_to_translate)
                    # Coloca el texto traducido en el contexto original
                    translated_row.append(text.replace(text_to_translate, translated_text))
                else:
                    translated_row.append(text)
            # Escribe la fila traducida en el archivo de salida
            writer.writerow(translated_row)

