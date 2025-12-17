import riva.client
from riva.client import SpeechSynthesisService as TTSService
from app.core.consts import RIVA_URI

def build_riva_client() -> TTSService:
    auth = riva.client.Auth(uri=RIVA_URI)
    return TTSService(auth)
