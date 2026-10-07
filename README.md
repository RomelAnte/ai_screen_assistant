# AI Screen Assistant

Asistente de escritorio para Windows que analiza la pantalla con un modelo de visión local y presenta una respuesta explicada.

## Problema

Al estudiar o trabajar frente a la computadora, explicar una pregunta que aparece en pantalla suele requerir copiarla manualmente a otra herramienta. Esto interrumpe el flujo y puede ser incómodo cuando el contenido incluye imágenes, fórmulas o código.

## Objetivo

Crear una aplicación de escritorio que permita pedir ayuda sobre el contenido visible, enviando la captura a un modelo local de Ollama y mostrando una respuesta, una explicación y, cuando corresponda, código.

## Stack

- **Python 3.10+** — lógica de la aplicación.
- **PySide6** — interfaz de escritorio.
- **MSS y Pillow** — captura y preparación de imágenes.
- **Ollama** — ejecución local del modelo multimodal.
- **Requests** — comunicación con la API local de Ollama.
- **Keyboard** — atajos globales.
- **Tesseract OCR / pytesseract** — utilidades OCR disponibles en el proyecto.

## Arquitectura

```text
Atajo global (F8)
       │
       ▼
Controlador y worker en segundo plano (main.py)
       │
       ├── Captura de pantalla (screen_capture.py)
       ├── Cliente de Ollama y codificación de imagen (ollama_client.py)
       ├── Configuración y prompt (config.py)
       └── Parseo de respuesta (response_parser.py)
                    │
                    ▼
             Ventana PySide6 (ui/)
```

La captura se procesa localmente y se envía a la instancia local de Ollama configurada en `config.py`. El modelo y sus requisitos de hardware dependen de Ollama.

## Funcionalidades

- Captura la pantalla principal mediante el atajo global `F8`.
- Consulta una instancia local de Ollama con una imagen y un prompt de tutor en español.
- Presenta la respuesta, explicación y código en una ventana de escritorio.
- Permite copiar la respuesta y el código.
- Incluye una interfaz de selección de región disponible desde el controlador interno.

## Estado actual

Prototipo funcional para Windows. Requiere instalar Python, Ollama, un modelo de visión compatible y Tesseract OCR. El atajo `F8` captura la pantalla principal; la selección manual aún no está conectada al flujo principal del atajo. La configuración del modelo está en `config.py`.

## Capturas

Aún no hay capturas de la interfaz preparadas para publicación. Para añadirlas, guarda imágenes sin datos personales en `docs/images/` y enlázalas aquí. Por ejemplo:

```markdown
![Ventana de respuesta](docs/images/response-window.png)
```

## Cómo ejecutarlo

### Requisitos

- Windows 10/11 de 64 bits.
- Python 3.10 o superior.
- [Ollama](https://ollama.com/) instalado y en ejecución.
- Un modelo multimodal compatible con Ollama. La configuración inicial usa `qwen2.5vl:7b`.
- Tesseract OCR instalado y accesible desde PATH o en una ruta habitual.

### Instalación en PowerShell

```powershell
git clone https://github.com/USUARIO/ai-screen-assistant.git
cd ai-screen-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ollama pull qwen2.5vl:7b
```

Si PowerShell impide activar el entorno, permite la ejecución solo en la sesión actual y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instala Tesseract OCR por separado si todavía no está disponible. Luego, con Ollama en ejecución:

```powershell
python main.py
```

Pulsa `F8` para analizar la pantalla principal. Cambia `OLLAMA_MODEL` en `config.py` si quieres usar otro modelo de visión compatible. La pantalla puede contener información privada: revisa lo que está visible antes de activar la captura.

## Roadmap

- [ ] Conectar la selección de región al flujo de captura principal.
- [ ] Permitir configurar modelo y dirección de Ollama desde la interfaz o variables de entorno.
- [ ] Añadir instrucciones para otros sistemas operativos.
- [ ] Mejorar la gestión de errores y el estado de las consultas en la interfaz.
- [ ] Publicar capturas de pantalla preparadas para compartir.
- [ ] Automatizar comprobaciones básicas del proyecto en GitHub Actions.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta [LICENSE](LICENSE).
