# Local Russian voice QA report

## Goal

Validate that Open-LLM-VTuber can use local Russian speech recognition and
Windows speech synthesis without sending audio to a cloud API, and make the
selected Windows voice reproducible through configuration.

## Environment

- Windows with a local SAPI voice
- `sherpa-onnx` Russian ASR model on CPU
- `pyttsx3` TTS
- local microphone input at 16 kHz mono PCM

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Russian ASR smoke test | PASS | Expected phrase and unique number `7429` were recognized |
| Local TTS generation | PASS | Audio file generated and played without a cloud audio API |
| Explicit system-voice selection | PASS | Voice name is validated and passed to the engine |
| Feedback-loop observation | PASS with limitation | No repeated cycle was observed for 15 seconds |
| Automated regression tests | PASS | Config, factory forwarding, selection, and failure path |

## Important limitation

The feedback-loop observation did not include a successful browser microphone
event. It therefore shows that no loop appeared during the observation window,
but it is not presented as proof of a complete browser-to-ASR-to-TTS turn.

## Automated reproduction

```bash
python -m pip install pytest pyttsx3 loguru pydantic PyYAML
pytest -q tests/portfolio
```

## Configuration example

```yaml
tts_config:
  tts_model: pyttsx3_tts
  pyttsx3_tts:
    voice_name: Microsoft Irina Desktop - Russian
```

The name must match an installed system voice. Matching is case-insensitive; an
unknown name fails with a list of available voices instead of silently falling
back to an unintended voice.

## Manual evidence

- `local-voice-baseline-2026-07-30.txt` — sanitized Windows ASR/TTS results
- `upstream-baseline-localhost.jpg` — local application baseline
- `upstream-baseline-server.log` — raw diagnostic log retained for auditability

No tokens, passwords, registry identifiers, or private filesystem paths are
included in the published evidence.
