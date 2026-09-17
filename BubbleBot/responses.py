# dont touch this side = this side can be edited remember to use "", "" if not, use only [""]
import json
import urllib.parse
import urllib.request

followup1 = ["Great", "Good to hear that", "Awesome!", "Ok"]
question1 = ["Good, you?", "I'm good, you?"]
question2 = ["What do you like?", "What is you favourite food?"]
followup2 = ["That's great!", "Wow", "Awesome"]
joke = ["Why can't you tell a joke to an egg? It might crack up!", "What do you call a magic dog? A labracadabrador!"]
invalid = ["?", "What do you mean?", "What?", "I don't understand"]
special_word_resp = "Awesome!"
goodbye = ["Bye!", "See you later!", "👋", ":("]
name = ["I am BubbleBot, your friendly chatbot!", "My name is BubbleBot!"]
sensored = ["Please don't use offensive language.", "DON'T SAY THAT!", "Fuck you too (:", "NO!", "STOP!", "YOU SHOULD KILL YOURSELF!"]
gay = ["I'm sorry, but I can't engage in that conversation.🏳‍🌈", "That's not something I can help with.", "I'm here to have a good conversation, not a bad one."]

LANGUAGE_CODES = {
    "french": "fr",
    "france": "fr",
    "francais": "fr",
    "français": "fr",
    "f": "fr",
    "fr": "fr",
    "spanish": "es",
    "espanol": "es",
    "español": "es",
    "s": "es",
    "es": "es",
    "german": "de",
    "deutsch": "de",
    "deutschland": "de",
    "g": "de",
    "de": "de",
}


def get_language_code(language):
    if not language:
        return None
    normalized = language.strip().lower().replace(" ", "").replace("-", "")
    return LANGUAGE_CODES.get(normalized)


def translate_text(text, target_language):
    if not text or not text.strip():
        return "Please enter some text to translate."

    language_code = get_language_code(target_language)
    if language_code is None:
        return text

    lowered = text.strip().lower()
    fallback_translations = {
        "fr": {
            "hello": "Bonjour",
            "hi": "Salut",
            "goodbye": "Au revoir",
            "thank you": "Merci",
            "how are you": "Comment ça va ?",
        },
        "es": {
            "hello": "Hola",
            "hi": "Hola",
            "goodbye": "Adiós",
            "thank you": "Gracias",
            "how are you": "¿Cómo estás?",
        },
        "de": {
            "hello": "Hallo",
            "hi": "Hallo",
            "goodbye": "Auf Wiedersehen",
            "thank you": "Danke",
            "how are you": "Wie geht es dir?",
        },
    }

    if lowered in fallback_translations.get(language_code, {}):
        return fallback_translations[language_code][lowered]

    try:
        encoded_text = urllib.parse.quote(text)
        url = (
            "https://api.mymemory.translated.net/get?"
            f"q={encoded_text}&langpair=en|{language_code}"
        )
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        translated = data.get("responseData", {}).get("translatedText")
        if translated:
            return translated
    except Exception:
        pass

    return text


TRANSLATE_ALIASES = [
    "translate",
    "translate text",
    "translation",
    "translator",
    "trans",
    "tr",
    "tl",
]


def is_translate_command(command):
    if not command:
        return False
    normalized = command.strip().lower().replace("!", "").replace("?", "")
    return normalized in TRANSLATE_ALIASES


TRANSLATE_LANGUAGE_ALIASES = {
    "f": "fr",
    "fr": "fr",
    "french": "fr",
    "france": "fr",
    "francais": "fr",
    "français": "fr",
    "s": "es",
    "es": "es",
    "spanish": "es",
    "espanol": "es",
    "español": "es",
    "g": "de",
    "de": "de",
    "german": "de",
    "deutsch": "de",
    "deutschland": "de",
}


def get_translation_choice(language):
    if not language:
        return None
    normalized = language.strip().lower().replace(" ", "").replace("-", "")
    return TRANSLATE_LANGUAGE_ALIASES.get(normalized)


def get_translate_prompt():
    return "Choose a language: French (f), Spanish (s), or German (g)."
