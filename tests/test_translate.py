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
