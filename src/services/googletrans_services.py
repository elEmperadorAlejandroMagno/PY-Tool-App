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
async def detect_language_sync(text: str) -> str:
  """Synchronous wrapper for detect_language"""
  return await detect_language(text)

async def translate_text_sync(text: str, input_lang: str, output_lang: str) -> str:
  """Synchronous wrapper for translate_text"""
  return await translate_text(text, input_lang, output_lang)

async def translate_text_with_detection(text: str, output_lang: str) -> str:
  """Translate text with automatic language detection"""
  detected_lang = await detect_language_sync(text)
  return await translate_text_sync(text, detected_lang, output_lang)

async def translate_text_delegate(src_input: object) -> str:
  """Delegate translation to the Translator object"""
  text, input_lang, output_lang = src_input
  if input_lang == "detect":
    return await translate_text_with_detection(text, output_lang)
  return await translate_text_sync(text, input_lang, output_lang)

async def main():
  text, input_lang, output_lang = ("Hello, how are you?", "en", "es")
  translated_text: str = await translate_text_delegate(("Hello, how are you?", "detect", "es"))
  print(f"Translated text: {translated_text}")

if __name__ == "__main__":
  asyncio.run(main())
