from types import SimpleNamespace

import pytest

from src.open_llm_vtuber.config_manager.tts import TTSConfig
from src.open_llm_vtuber.tts.pyttsx3_tts import TTSEngine
from src.open_llm_vtuber.tts.tts_factory import TTSFactory


class FakeVoice:
    def __init__(self, name: str, voice_id: str):
        self.name = name
        self.id = voice_id


class FakeEngine:
    def __init__(self):
        self.voices = [
            FakeVoice("Microsoft Irina Desktop - Russian", "voice-irina"),
            FakeVoice("Microsoft Zira Desktop", "voice-zira"),
        ]
        self.selected_voice = None

    def getProperty(self, name):
        assert name == "voices"
        return self.voices

    def setProperty(self, name, value):
        assert name == "voice"
        self.selected_voice = value


def test_config_accepts_local_voice_name():
    config = TTSConfig.model_validate(
        {
            "tts_model": "pyttsx3_tts",
            "pyttsx3_tts": {"voice_name": "Microsoft Irina Desktop - Russian"},
        }
    )

    assert config.pyttsx3_tts.voice_name == "Microsoft Irina Desktop - Russian"


def test_factory_forwards_voice_name(monkeypatch):
    calls = []

    class FakeTTSEngine:
        def __init__(self, voice_name=None):
            calls.append(voice_name)

    module = SimpleNamespace(TTSEngine=FakeTTSEngine)
    monkeypatch.setitem(
        __import__("sys").modules,
        "src.open_llm_vtuber.tts.pyttsx3_tts",
        module,
    )

    TTSFactory.get_tts_engine(
        "pyttsx3_tts", voice_name="Microsoft Irina Desktop - Russian"
    )

    assert calls == ["Microsoft Irina Desktop - Russian"]


def test_engine_selects_voice_case_insensitively(monkeypatch, tmp_path):
    fake_engine = FakeEngine()
    monkeypatch.setattr(
        "src.open_llm_vtuber.tts.pyttsx3_tts.pyttsx3.init", lambda: fake_engine
    )
    monkeypatch.chdir(tmp_path)

    TTSEngine("microsoft irina desktop - russian")

    assert fake_engine.selected_voice == "voice-irina"


def test_engine_lists_available_voices_when_requested_voice_is_missing(
    monkeypatch, tmp_path
):
    fake_engine = FakeEngine()
    monkeypatch.setattr(
        "src.open_llm_vtuber.tts.pyttsx3_tts.pyttsx3.init", lambda: fake_engine
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError, match="Microsoft Zira Desktop"):
        TTSEngine("Unknown voice")
