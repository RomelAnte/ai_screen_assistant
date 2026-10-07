import base64
import io

import requests
from PIL import Image

from config import (
    MAX_IMAGE_SIDE,
    MODEL_PROMPT,
    OLLAMA_MODEL,
    OLLAMA_URL,
    REQUEST_TIMEOUT_SECONDS,
)


class OllamaError(RuntimeError):
    pass


def _image_to_base64(image: Image.Image) -> str:
    image = image.convert("RGB")
    image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def ask_ollama(image: Image.Image) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": MODEL_PROMPT,
        "images": [_image_to_base64(image)],
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        if not result:
            raise OllamaError("Ollama devolvió una respuesta vacía.")
        return result
    except requests.Timeout as exc:
        raise OllamaError(f"Tiempo de espera agotado ({REQUEST_TIMEOUT_SECONDS}s).") from exc
    except requests.ConnectionError as exc:
        raise OllamaError("Ollama no está disponible en http://localhost:11434.") from exc
    except requests.HTTPError as exc:
        body = exc.response.text[:300] if exc.response is not None else ""
        raise OllamaError(
            f"Ollama devolvió un error. ¿Descargaste el modelo '{OLLAMA_MODEL}'? {body}"
        ) from exc
    except ValueError as exc:
        raise OllamaError("Ollama devolvió una respuesta JSON inválida.") from exc
    except requests.RequestException as exc:
        raise OllamaError(f"Error al comunicar con Ollama: {exc}") from exc