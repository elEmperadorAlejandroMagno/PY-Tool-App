from googletrans import Translator
import asyncio

async def translate_text(lang, text):
    translator = Translator()
    if not lang:
        detected_lang = await translator.detect(text)
        lang = detected_lang.lang
    translated = await translator.translate(text, src=lang, dest='es')
    return translated.text.lower()

if __name__ == '__main__':
    translate_text(input())
