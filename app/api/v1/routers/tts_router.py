from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime

from app.api.v1.dtos.synthesizer_request import SynthesizerRequest
from app.utils.path_utils import build_audio_output_path
from app.utils.file_utils import file_ready
from app.domain.services.tts_service import synthesize_to_file

router = APIRouter(
    prefix="/api/v1/tts",
    tags=["TTS"]
)


# ============================================================
# Catálogo de voces
# ============================================================
VOICE_CATALOG = {
    "en-US": {
        "voices": [
            "English-US.Female-1",
            "English-US.Male-1",
            "English-US.Female-Neutral",
            "English-US.Male-Neutral",
            "English-US.Female-Angry",
            "English-US.Male-Angry",
            "English-US.Female-Calm",
            "English-US.Male-Calm",
            "English-US.Female-Fearful",
            "English-US.Female-Happy",
            "English-US.Male-Happy",
            "English-US.Female-Sad"
        ]
    },
    "es-ES": {
        "voices": [
            "Spanish-ES-Female-1.0",
            "Spanish-ES-Male-1.0"
        ]
    }
}


# ============================================================
# Endpoint: Obtener lista plana de voces
# ============================================================
@router.get(
    "/voices",
    summary="Obtener todas las voces en formato de lista plana"
)
async def get_available_voices() -> list[dict]:
    """
    Devuelve una lista plana con:
    [
      { "language_code": "en-US", "voice_name": "English-US.Female-1" },
      ...
    ]
    """
    result = []

    for language_code, data in VOICE_CATALOG.items():
        voices = data.get("voices", [])
        for voice in voices:
            result.append({
                "language_code": language_code,
                "voice_name": voice
            })

    return result


# ============================================================
# Endpoint: Sintetizar texto TTS
# ============================================================
@router.post(
    "",
    summary="Sintetiza texto con Riva",
    response_class=FileResponse,
)
async def synthesize(req: SynthesizerRequest = Body()):
    try:
        audio_path = build_audio_output_path().replace(
            ".wav", f".{req.output_format}"
        )

        synthesize_to_file(
            text=req.text,
            voice=req.voice_name,
            lang=req.language_code,
            sample_rate=req.sample_rate_hz,
            channels=req.audio_channel_count,
            output_format=req.output_format,
            out_path=audio_path,
        )

        if not file_ready(audio_path):
            raise RuntimeError("Audio no generado")

        timestamp = datetime.now().strftime("%d-%m-%y_%H_%M_%S")
        filename = f"tts_{timestamp}.{req.output_format}"

        return FileResponse(
            path=audio_path,
            media_type=f"audio/{req.output_format}",
            filename=filename
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))