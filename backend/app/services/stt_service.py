"""Speech-to-Text service — OpenAI Whisper."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def transcribe_audio(audio_file_path: str, api_key: Optional[str] = None) -> dict:
    """
    Convert voice note to text using OpenAI Whisper.
    Supports Hindi, English, Tamil, Bengali, etc.
    Returns: {"text": "...", "language": "hi", "duration_seconds": 12.5}
    """
    try:
        import openai

        if api_key:
            client = openai.OpenAI(api_key=api_key)
        else:
            from app.config import settings
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )

        return {
            "text": transcript.text,
            "language": getattr(transcript, "language", "unknown"),
            "duration_seconds": getattr(transcript, "duration", 0),
        }
    except Exception as e:
        logger.error(f"STT transcription failed: {e}")
        return {
            "text": "",
            "language": "unknown",
            "duration_seconds": 0,
            "error": str(e),
        }


async def transcribe_audio_local(audio_file_path: str) -> dict:
    """
    Fallback: use local Whisper model (requires `openai-whisper` package).
    Useful when API key is not available.
    """
    try:
        import whisper

        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
        return {
            "text": result["text"],
            "language": result.get("language", "unknown"),
            "duration_seconds": 0,
        }
    except ImportError:
        logger.warning("Local whisper not installed. pip install openai-whisper")
        return {"text": "", "language": "unknown", "duration_seconds": 0, "error": "whisper not installed"}
    except Exception as e:
        logger.error(f"Local STT failed: {e}")
        return {"text": "", "language": "unknown", "duration_seconds": 0, "error": str(e)}
