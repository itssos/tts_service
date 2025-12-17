import riva.client
import os

from app.infrastructure.riva.tts_client import build_riva_client
from app.utils.audio_utils import write_wav, convert_audio
from app.core.consts import (
    TTS_SAMPLE_RATE_HZ,
    TTS_AUDIO_CHANNEL_COUNT,
    TTS_OUTPUT_FORMAT,
    SUPPORTED_SAMPLE_RATES,
    SUPPORTED_CHANNEL_COUNTS,
    SUPPORTED_OUTPUT_FORMATS,
)

def validate_audio_params(sample_rate, channels, output_format):
    if sample_rate not in SUPPORTED_SAMPLE_RATES:
        raise ValueError("sample_rate_hz no soportado")

    if channels not in SUPPORTED_CHANNEL_COUNTS:
        raise ValueError("audio_channel_count no soportado")

    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        raise ValueError("output_format no soportado")

def build_tts_request(text: str, voice: str, lang: str) -> dict:
    return {
        "text": text,
        "language_code": lang,
        "voice_name": voice,
        "sample_rate_hz": TTS_SAMPLE_RATE_HZ,
        "encoding": riva.client.AudioEncoding.LINEAR_PCM,
    }

def synthesize_to_file(
    text: str,
    voice: str,
    lang: str,
    sample_rate: int,
    channels: int,
    output_format: str,
    out_path: str,
) -> None:

    validate_audio_params(sample_rate, channels, output_format)

    client = build_riva_client()
    request = build_tts_request(text, voice, lang)

    audio_chunks = []
    for chunk in client.synthesize_online(**request):
        if chunk.audio:
            audio_chunks.append(chunk.audio)

    raw_audio = b"".join(audio_chunks)

    wav_path = out_path.replace(f".{output_format}", ".wav")

    write_wav(
        raw_audio,
        wav_path,
        sample_rate,
        channels
    )

    # Si no es WAV → transformar
    if output_format != "wav":
        convert_audio(wav_path, out_path, output_format)
        os.remove(wav_path)
