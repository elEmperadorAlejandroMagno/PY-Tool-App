from googletrans import Translator
from typing import Optional
import asyncio

translator = Translator()

async def detect_language(text):
  detected_lang = await translator.detect(text)
  return detected_lang.lang

async def translate_text(text: str, input_lang: str, output_lang: str) -> str:
  translated = await translator.translate(text, src=input_lang, dest=output_lang)
  return str(translated.text)

# Synchronous wrapper functions for external use
def detect_language_sync(text: str) -> str:
  """Synchronous wrapper for detect_language"""
  return asyncio.run(detect_language(text))

def translate_text_sync(text: str, input_lang: str, output_lang: str) -> str:
  """Synchronous wrapper for translate_text"""
  return asyncio.run(translate_text(text, input_lang, output_lang))

def translate_text_with_detection(text: str, output_lang: str) -> str:
  """Translate text with automatic language detection"""
  detected_lang = detect_language_sync(text)
  return translate_text_sync(text, detected_lang, output_lang)

def translate_text_delegate(src_input: object) -> str:
  """Delegate translation to the Translator object"""
  if src_input.input_lang == "detect":
    return translate_text_with_detection(src_input.text, src_input.output_lang)
  return translate_text_sync(src_input.text, src_input.input_lang, src_input.output_lang)

async def main():
  text = "Hello, how are you?"
  entry_lang: str = await detect_language(text)
  output_lang: str = "es"
  translated_text: str = await translate_text(text, entry_lang, output_lang)
  print(f"Translated text: {translated_text}")

if __name__ == "__main__":
  asyncio.run(main())
