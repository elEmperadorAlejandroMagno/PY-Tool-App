from googletrans import Translator
from typing import Optional

translator = Translator()

def detect_language(text):
    detected_lang = translator.detect(text)
    return detected_lang.lang

def translate_text(text: str, input_lang: str, output_lang: str) -> str:
    translated = translator.translate(text, src=input_lang, dest=output_lang)
    return translated.text

def translate_text_with_detection(text: str, output_lang: str) -> str:
    detected_lang =  detect_language(text)
    return translate_text(text, detected_lang, output_lang)

def translate_text_delegate(src_input: object) -> str:
    text, input_lang, output_lang = src_input
    if input_lang == "detect":
        return translate_text_with_detection(text, output_lang)
    return translate_text(text, input_lang, output_lang)

def main():
    text, input_lang, output_lang = ("Hello, how are you?", "en", "es")
    translated_text = translate_text_delegate((text, input_lang, output_lang))
    print(f"Translated text: {translated_text}")

if __name__ == "__main__":
    main()
