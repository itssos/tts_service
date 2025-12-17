from pathlib import Path
import uuid

def build_audio_output_path() -> str:
    tmp_dir = Path("/tmp/riva_tts")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return str(tmp_dir / f"{uuid.uuid4().hex}.wav")
