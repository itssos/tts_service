import os

from peewee import SqliteDatabase

DATABASE_PATH = os.getenv("DATABASE_PATH", "database.db")
db = SqliteDatabase(DATABASE_PATH)
RIVA_URI = os.getenv("RIVA_URI", "localhost:50051")

TTS_SAMPLE_RATE_HZ = 16000
TTS_AUDIO_CHANNEL_COUNT = 1
TTS_OUTPUT_FORMAT = "wav"

SUPPORTED_SAMPLE_RATES = {16000}
SUPPORTED_CHANNEL_COUNTS = {1}
SUPPORTED_OUTPUT_FORMATS = {"wav", "mp3"}