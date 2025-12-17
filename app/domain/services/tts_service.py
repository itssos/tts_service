import os
import riva.client

from app.infrastructure.riva.tts_client import build_riva_client
from app.utils.audio_utils import write_wav, convert_audio
from app.core.consts import (
    TTS_SAMPLE_RATE_HZ,
    SUPPORTED_SAMPLE_RATES,
    SUPPORTED_CHANNEL_COUNTS,
    SUPPORTED_OUTPUT_FORMATS,
    TTS_ALLOWED_COMBOS,
    RIVA_VOICE_MAP,
)

def _normalize_language(lang: str) -> str:
    v = (lang or "").strip()
    up = v.upper()
    if up == "ES-ES":
        return "es-ES"
    if up == "EN-US":
        return "en-US"
    return v  # si viene ya normalizado, lo dejamos

def _normalize_voice(voice: str) -> str:
    return (voice or "").strip().upper()

def _normalize_format(fmt: str) -> str:
    return (fmt or "").strip().upper()

def validate_audio_params(sample_rate: int, channels: int, output_ext: str) -> None:
    if sample_rate not in SUPPORTED_SAMPLE_RATES:
        raise ValueError("sample_rate_hz no soportado")

    if channels not in SUPPORTED_CHANNEL_COUNTS:
        raise ValueError("audio_channel_count no soportado")

    if output_ext not in SUPPORTED_OUTPUT_FORMATS:
        raise ValueError("output_format no soportado (ext)")

def validate_catalog_selection(language_code: str, voice_name: str, output_format: str) -> None:
    combo = (language_code, voice_name, output_format)
    if combo not in TTS_ALLOWED_COMBOS:
        raise ValueError("Combinación no soportada: language_code/voice_name/output_format")

def build_tts_request(text: str, riva_voice_name: str, lang: str) -> dict:
    return {
        "text": text,
        "language_code": lang,
        "voice_name": riva_voice_name,
        "sample_rate_hz": TTS_SAMPLE_RATE_HZ,
        "encoding": riva.client.AudioEncoding.LINEAR_PCM,
    }

def synthesize_to_file(
    text: str,
    voice: str,          # MALE/FEMALE (dominio)
    lang: str,           # es-ES/en-US (normalizado)
    sample_rate: int,
    channels: int,
    output_format: str,  # WAV/MP3 (dominio)
    out_path: str,
) -> None:
    language_code = _normalize_language(lang)
    voice_name = _normalize_voice(voice)
    fmt = _normalize_format(output_format)

    # 1) Validación catálogo cerrado
    validate_catalog_selection(language_code, voice_name, fmt)

    # 2) Mapear a la voz REAL de Riva
    riva_voice = RIVA_VOICE_MAP.get((language_code, voice_name))
    if not riva_voice:
        raise ValueError("No existe mapeo a voz de Riva para language_code/voice_name")

    # 3) Extensión real del archivo
    output_ext = fmt.lower()  # "wav" o "mp3"

    # 4) Validación de audio actual (lo que ya estabas haciendo)
    validate_audio_params(sample_rate, channels, output_ext)

    client = build_riva_client()
    request = build_tts_request(text=text, riva_voice_name=riva_voice, lang=language_code)

    audio_chunks = []
    for chunk in client.synthesize_online(**request):
        if chunk.audio:
            audio_chunks.append(chunk.audio)

    raw_audio = b"".join(audio_chunks)

    # Riva devuelve PCM -> escribimos WAV intermedio seguro
    wav_path = out_path.replace(f".{output_ext}", ".wav")

    write_wav(
        raw_audio,
        wav_path,
        sample_rate,
        channels
    )

    # Si piden mp3 -> convertir y borrar wav intermedio
    if output_ext != "wav":
        convert_audio(wav_path, out_path, output_ext)
        os.remove(wav_path)
