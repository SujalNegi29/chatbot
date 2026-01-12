from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def to_english(text, src_lang):
    if src_lang == "en":
        return text
    return translator.translate(text, src=src_lang, dest="en").text

def from_english(text, target_lang):
    if target_lang == "en":
        return text
    return translator.translate(text, src="en", dest=target_lang).text
