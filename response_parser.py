import re


def _section(text: str, label: str) -> str:
    match = re.search(
        rf"(?im)^\s*{re.escape(label)}\s*:\s*(.*?)(?=^\s*(?:RESPUESTA|EXPLICACIÓN|CÓDIGO)\s*:|\Z)",
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def parse_response(text: str) -> dict[str, str]:
    raw = text.strip()
    if not raw:
        return {"answer": "", "explanation": "", "code": ""}

    answer = _section(raw, "RESPUESTA")
    explanation = _section(raw, "EXPLICACIÓN")
    code = _section(raw, "CÓDIGO")

    if not answer:
        answer = raw

    if code.lower() == "no aplica":
        code = "No aplica"

    return {
        "answer": answer.strip(),
        "explanation": explanation.strip(),
        "code": code.strip(),
    }