import os
from peewee import SqliteDatabase

# ============================================================
# Base de datos
# ============================================================
DATABASE_PATH = os.getenv("DATABASE_PATH", "database.db")
db = SqliteDatabase(DATABASE_PATH)

# ============================================================
# Riva
# ============================================================
RIVA_URI = os.getenv("RIVA_URI", "localhost:50051")

# ============================================================
# Audio por defecto / validaciones actuales
# ============================================================
TTS_SAMPLE_RATE_HZ = 16000
TTS_AUDIO_CHANNEL_COUNT = 1
TTS_OUTPUT_FORMAT = "wav"

SUPPORTED_SAMPLE_RATES = {16000}
SUPPORTED_CHANNEL_COUNTS = {1}

# Extensiones internas soportadas (minúsculas)
SUPPORTED_OUTPUT_FORMATS = {"wav", "mp3"}

# ============================================================
# Constantes de dominio (catálogo TTS)
# ============================================================
LANG_ES = "es-ES"
LANG_EN = "en-US"

VOICE_MALE = "MALE"
VOICE_FEMALE = "FEMALE"

FORMAT_WAV = "WAV"
FORMAT_MP3 = "MP3"

# ============================================================
# Catálogo cerrado soportado por tu API
# ============================================================
TTS_VOICE_CATALOG = [
    {"language_code": LANG_ES, "voice_name": VOICE_MALE, "output_format": FORMAT_WAV},
    {"language_code": LANG_ES, "voice_name": VOICE_MALE, "output_format": FORMAT_MP3},
    {"language_code": LANG_ES, "voice_name": VOICE_FEMALE, "output_format": FORMAT_WAV},
    {"language_code": LANG_ES, "voice_name": VOICE_FEMALE, "output_format": FORMAT_MP3},

    {"language_code": LANG_EN, "voice_name": VOICE_MALE, "output_format": FORMAT_WAV},
    {"language_code": LANG_EN, "voice_name": VOICE_MALE, "output_format": FORMAT_MP3},
    {"language_code": LANG_EN, "voice_name": VOICE_FEMALE, "output_format": FORMAT_WAV},
    {"language_code": LANG_EN, "voice_name": VOICE_FEMALE, "output_format": FORMAT_MP3},
]

# Set rápido para validar combinaciones permitidas
TTS_ALLOWED_COMBOS = {
    (item["language_code"], item["voice_name"], item["output_format"])
    for item in TTS_VOICE_CATALOG
}

# ============================================================
# Mapeo de (idioma, género) -> nombre REAL de voz en Riva
# (esto es lo que se le pasa a Riva por debajo)
# ============================================================
RIVA_VOICE_MAP = {
    (LANG_ES, VOICE_MALE): "Spanish-ES-Male-1.0",
    (LANG_ES, VOICE_FEMALE): "Spanish-ES-Female-1.0",
    (LANG_EN, VOICE_MALE): "English-US.Male-1",
    (LANG_EN, VOICE_FEMALE): "English-US.Female-1",
}
