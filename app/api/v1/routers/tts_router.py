from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime

from app.api.v1.dtos.synthesizer_request import SynthesizerRequest
from app.utils.path_utils import build_audio_output_path
from app.utils.file_utils import file_ready
from app.domain.services.tts_service import synthesize_to_file
from app.core.consts import TTS_VOICE_CATALOG

router = APIRouter(
    prefix="/api/v1/tts",
    tags=["TTS"]
)

# ============================================================
# Endpoint: Catálogo cerrado (lo que me pediste)
# ============================================================
@router.get(
    "/voices",
    summary="Catálogo soportado de voces, idiomas y formatos"
)
async def get_tts_catalog() -> list[dict]:
    return TTS_VOICE_CATALOG


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
        # output_format llega como WAV/MP3; usamos extensión en minúsculas
        out_ext = (req.output_format or "").strip().lower()
        audio_path = build_audio_output_path().replace(".wav", f".{out_ext}")

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
        filename = f"tts_{timestamp}.{out_ext}"

        return FileResponse(
            path=audio_path,
            media_type=f"audio/{out_ext}",
            filename=filename
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
