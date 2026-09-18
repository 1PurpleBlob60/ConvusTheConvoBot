# dont touch this side = this side can be edited remember to use "", "" if not, use only [""]
try:
    import argostranslate.translate as argos_translate
    import argostranslate.package as argos_package
except ImportError:
    argos_translate = None
    argos_package = None

INSTALLED_TRANSLATION_MODELS = set()

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

    if argos_translate is None:
        return "Translation is unavailable because Argos Translate is not installed."

    try:
        installed_targets = {
            translation.to_lang.code
            for language in argos_translate.get_installed_languages()
            for translation in language.translations_from
            if translation.from_lang.code == "en"
        }
        if language_code not in installed_targets:
            if argos_package is None:
                return "Translation models are unavailable because Argos Translate is not installed."
            if language_code not in INSTALLED_TRANSLATION_MODELS:
                argos_package.update_package_index()
                installed = argos_package.install_package_for_language_pair(
                    "en",
                    language_code,
                )
                if not installed:
                    return f"The {language_code} translation model could not be installed."
                INSTALLED_TRANSLATION_MODELS.add(language_code)
                installed_targets = {
                    translation.to_lang.code
                    for language in argos_translate.get_installed_languages()
                    for translation in language.translations_from
                    if translation.from_lang.code == "en"
                }
            if language_code not in installed_targets:
                return f"The {language_code} translation model is not available yet."

        translated = argos_translate.translate(text, "en", language_code)
        if translated and translated.strip():
            return translated
    except Exception:
        pass

    fallback_translations = {
        "fr": {
            "hello": "Bonjour",
            "hi": "Salut",
            "goodbye": "Au revoir",
            "thank you": "Merci",
            "cat": "chat",
            "dog": "chien",
            "house": "maison",
            "water": "eau",
            "food": "nourriture",
            "love": "amour",
        },
        "es": {
            "hello": "Hola",
            "hi": "Hola",
            "goodbye": "Adiós",
            "thank you": "Gracias",
            "cat": "gato",
            "dog": "perro",
            "house": "casa",
            "water": "agua",
            "food": "comida",
            "love": "amor",
        },
        "de": {
            "hello": "Hallo",
            "hi": "Hallo",
            "goodbye": "Auf Wiedersehen",
            "thank you": "Danke",
            "cat": "Katze",
            "dog": "Hund",
            "house": "Haus",
            "water": "Wasser",
            "food": "Essen",
            "love": "Liebe",
        },
    }

    lookup = text.strip().lower()
    if lookup in fallback_translations.get(language_code, {}):
        return fallback_translations[language_code][lookup]

    return f"Translation for '{text}' is unavailable right now. Try a simple word or phrase."


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
