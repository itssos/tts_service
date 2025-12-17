import wave
import subprocess
from app.core.consts import TTS_SAMPLE_RATE_HZ, TTS_AUDIO_CHANNEL_COUNT

def write_wav(
    audio_bytes: bytes,
    file_path: str,
    sample_rate: int,
    channels: int
) -> None:
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16 bits PCM
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

def convert_audio(
    input_path: str,
    output_path: str,
    output_format: str
) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", input_path,
            output_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
