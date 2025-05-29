from googletrans import Translator
import asyncio

async def translate_text(lang, text):
    translator = Translator()
    if not lang:
        detected_lang = await translator.detect(text)
        lang = detected_lang.lang
    translated = await translator.translate(text, src=lang, dest='es')
    return translated.text.lower()

def translate_file(file_path, lang='en'):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        output_path = file_path.replace('.txt', '_translated.txt')
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for line in lines:
                translated_line = asyncio.run(translate_text(lang, line.strip()))
                out_file.write(translated_line + '\n')
    file.close()
    out_file.close()
    return f"Archivo traducido guardado en: {output_path}"

if __name__ == '__main__':
    translate_text(input())
