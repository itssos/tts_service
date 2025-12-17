from pydantic import BaseModel, Field

class SynthesizerRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=2,
        description="Texto a sintetizar (puede contener SSML)",
        example="Bien, gracias por venir. Para empezar, ¿podrías contarme brevemente sobre ti y tu experiencia con Java?"
    )
    voice_name: str = Field(
        ...,
        description="Voz de dominio: MALE o FEMALE",
        example="MALE"
    )
    language_code: str = Field(
        ...,
        description="Idioma: es-ES / en-US (también se acepta ES-ES/EN-US)",
        example="es-ES"
    )

    sample_rate_hz: int = Field(
        16000,
        description="Frecuencia de muestreo"
    )
    audio_channel_count: int = Field(
        1,
        description="Número de canales de audio"
    )
    output_format: str = Field(
        "WAV",
        description="Formato de salida: WAV o MP3",
        example="WAV"
    )
