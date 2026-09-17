import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "BubbleBot"))

import responses


def test_get_language_code_for_supported_languages():
    assert responses.get_language_code("french") == "fr"
    assert responses.get_language_code("spanish") == "es"
    assert responses.get_language_code("german") == "de"


def test_translate_text_returns_string_for_supported_language():
    result = responses.translate_text("hello", "fr")
    assert isinstance(result, str)
    assert result.strip()
    assert result == "Bonjour"


def test_translate_text_accepts_full_language_names_and_iso_codes():
    assert responses.translate_text("hello", "french") == "Bonjour"
    assert responses.translate_text("hello", "fr") == "Bonjour"


def test_translate_shortcuts_and_command_aliases():
    assert responses.get_language_code("f") == "fr"
    assert responses.get_language_code("s") == "es"
    assert responses.get_language_code("g") == "de"
    assert responses.translate_text("hello", "f") == "Bonjour"
    assert responses.translate_text("hello", "s") == "Hola"
    assert responses.translate_text("hello", "g") == "Hallo"
