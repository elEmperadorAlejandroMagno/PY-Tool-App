import spacy 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc


def cargar_modelo(texto: str, language: str) -> "Doc":
    modelos: dict[str, str] = {
        'en': 'en_core_web_lg',
        'es': 'es_core_news_lg',
        'it': 'it_core_news_lg',
        'fr': 'fr_core_news_lg',
        'ru': 'ru_core_news_lg'
    }
    modelo = modelos.get(language)
    if modelo:
        nlp = spacy.load(modelo)
        return nlp(texto)
    else:
        raise ValueError("Idioma no soportado")

def preprocess_text(text_object: "Doc") -> str:
    # procesa el texto para eliminar datos sensibles
    # por ejemplo, eliminando nombres propios o información personal
    new_text = text_object.text
    for ent in text_object.ents:
        if ent.label_ == 'PERSON':
            new_text = new_text.replace(ent.text, 'NOMBRE_PROPIO')
        elif ent.label_ == 'ORG':
            new_text = new_text.replace(ent.text, 'ORGANIZACION')
        elif ent.label_ == 'GPE':
            new_text = new_text.replace(ent.text, 'GPE')
        elif ent.label_ == 'LOC':
            new_text = new_text.replace(ent.text, 'LUGAR')
    return new_text

def postprocess_text(original_text: "Doc", processed_text: str) -> str:
    # restaura los datos sensibles en el texto
    # por ejemplo, restaurando nombres propios o información personal
    for ent in original_text.ents:
        if ent.label_ == 'PER':
            processed_text = processed_text.replace('PERSON', ent.text, 1)
        elif ent.label_ == 'ORG':
            processed_text = processed_text.replace('ORG', ent.text, 1)
        elif ent.label_ == 'GPE':
            processed_text = processed_text.replace('GPE', ent.text, 1)
        elif ent.label_ == 'LOC':
            processed_text = processed_text.replace('LUGAR', ent.text, 1)
    return processed_text

if __name__ == "__main__":
    text = "Mi trabajo es programar en Microsoft y vivo en ONG con Ana."
    doc = cargar_modelo(text, "es")
    processed_text = preprocess_text(doc)
    new_text = postprocess_text(doc, processed_text)
    print(new_text)
