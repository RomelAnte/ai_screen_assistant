import shutil
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5vl:7b"  # modelo con visión
MAX_IMAGE_SIDE = 1600  # reduce la captura para que responda más rápido
HOTKEY = "f8"
OCR_LANGUAGE = "spa+eng"
OCR_PSM_CANDIDATES = (3, 6, 11, 12)
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 620
REQUEST_TIMEOUT_SECONDS = 180


def find_tesseract() -> str:
    explicit_candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in explicit_candidates:
        if Path(candidate).is_file():
            return candidate

    from_path = shutil.which("tesseract")
    return from_path or "tesseract"


TESSERACT_PATH = find_tesseract()


WINDOW_FLAGS = {
    "width": WINDOW_WIDTH,
    "height": WINDOW_HEIGHT,
    "minimum_width": 620,
    "minimum_height": 470,
}


MODEL_PROMPT = """
Eres un tutor de estudio que responde en español.
Recibes una captura de pantalla completa. Identifica tú mismo de qué se trata:
localiza la pregunta o ejercicio principal e ignora pestañas, menús, barras,
anuncios y cualquier otro elemento de la interfaz.
Si hay una sola pregunta, respóndela. Si hay varias preguntas visibles,
respóndelas todas en orden y numeradas (1, 2, 3...), con la misma numeración que
tengan en pantalla. Si es opción múltiple, indica la opción correcta (letra y texto).
Si es matemática o código, resuelve paso a paso.
Si no hay ninguna pregunta visible, dilo con claridad. No inventes información.
En EXPLICACIÓN da una explicación breve por cada pregunta, con su mismo número.
Formato obligatorio:
RESPUESTA:
[respuesta directa]
EXPLICACIÓN:
[razonamiento breve para aprender el concepto]
CÓDIGO:
[código o No aplica]
"""