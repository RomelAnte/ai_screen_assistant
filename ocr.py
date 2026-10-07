from pathlib import Path
from typing import Iterable

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from config import OCR_LANGUAGE, OCR_PSM_CANDIDATES, TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)


def _prepare_image(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    grayscale = ImageOps.grayscale(rgb)
    grayscale = ImageEnhance.Contrast(grayscale).enhance(2.0)
    grayscale = ImageOps.autocontrast(grayscale)
    grayscale = grayscale.resize((grayscale.width * 2, grayscale.height * 2))
    return grayscale.filter(ImageFilter.SHARPEN)


def _ocr_with_psm(processed: Image.Image, psm: int) -> tuple[str, float]:
    data = pytesseract.image_to_data(
        processed,
        lang=OCR_LANGUAGE,
        config=f"--psm {psm}",
        output_type=pytesseract.Output.DICT,
    )
    words = [
        word
        for word, text in zip(data["text"], data["conf"])
        if text.strip() and word.strip()
    ]
    confidences = [
        float(value)
        for value in data["conf"]
        if value != "-1" and value.strip()
    ]
    text = " ".join(word for word in words).strip()
    average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    return text, average_confidence


def _normalize_text(text: str) -> str:
    return "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    ).strip()


def extract_text(image: Image.Image) -> str:
    processed = _prepare_image(image)
    candidates: Iterable[tuple[str, float]] = (
        _ocr_with_psm(processed, psm) for psm in OCR_PSM_CANDIDATES
    )
    results = list(candidates)
    if not results:
        raise RuntimeError("Tesseract no devolvió resultados de OCR.")

    best_text, best_confidence = max(
        results,
        key=lambda result: (result[1], len(result[0])),
    )
    text = _normalize_text(best_text)
    if not text:
        raise RuntimeError("No se detectó texto en la región seleccionada.")
    return text


def get_ocr_confidence(image: Image.Image) -> float:
    processed = _prepare_image(image)
    _, confidence = max(
        (_ocr_with_psm(processed, psm) for psm in OCR_PSM_CANDIDATES),
        key=lambda result: result[1],
    )
    return confidence