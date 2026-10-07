# AI Screen Assistant

Asistente de escritorio local para estudiar y practicar con contenido visible en pantalla.

AI Screen Assistant permite capturar la pantalla mediante un atajo global y enviar la imagen a un modelo de visión ejecutado localmente con [Ollama](https://ollama.com/). El modelo identifica el ejercicio o pregunta principal y genera una respuesta acompañada de una explicación.

El procesamiento de la imagen se realiza localmente mediante Ollama. No necesitas enviar capturas a una API de IA en la nube.

> **Estado:** prototipo funcional para Windows.

## ¿Para qué sirve?

Está pensado para:

- estudiar con cuestionarios propios;
- practicar con bancos de preguntas;
- analizar ejercicios de programación;
- resolver problemas matemáticos;
- comprender preguntas mostradas en pantalla;
- recibir explicaciones sobre conceptos;
- trabajar con contenido que combine texto, imágenes, fórmulas o código.

El objetivo no es solamente obtener una respuesta, sino utilizar la IA como apoyo para comprender el problema.

## ¿Cómo funciona?

El flujo principal es:

```text
                Presionar F8
                     │
                     ▼
              Captura de pantalla
                     │
                     ▼
            Redimensionamiento
                     │
                     ▼
              Imagen en Base64
                     │
                     ▼
          API local de Ollama
                     │
                     ▼
       Modelo multimodal de visión
                     │
                     ▼
             Respuesta en español
                     │
                     ▼
             Parser de respuesta
                     │
                     ▼
              Ventana PySide6
```

El modelo recibe la captura y determina qué contenido es relevante. No es necesario copiar manualmente la pregunta ni utilizar OCR para el flujo principal.

## Características

- Atajo global `F8`.
- Captura de pantalla mediante MSS.
- Redimensionamiento de imágenes para reducir el tiempo de procesamiento.
- Análisis mediante modelo multimodal local.
- Integración con Ollama.
- Respuestas en español.
- Explicación del procedimiento.
- Soporte para preguntas de opción múltiple.
- Análisis de ejercicios matemáticos.
- Análisis de código.
- Ventana de respuesta siempre visible.
- Copia rápida de respuesta y código.
- Arquitectura preparada para incorporar selección de regiones.
- Sin dependencia de una API de IA en la nube.

## Modelo de IA

La configuración inicial utiliza:

```text
qwen2.5vl:7b
```

También se pueden probar modelos multimodales más pequeños si el hardware disponible requiere menor consumo de recursos.

La aplicación se comunica con la instancia local de Ollama mediante:

```text
http://localhost:11434/api/generate
```

El modelo puede cambiarse desde `config.py`.

```python
OLLAMA_MODEL = "qwen2.5vl:7b"
```

## Requisitos

### Actualmente soportado

- Windows 10/11
- Python 3.10+
- Ollama
- Un modelo multimodal compatible
- CPU/GPU suficiente para ejecutar el modelo seleccionado

### No requiere actualmente

- Cuenta de OpenAI
- API key
- API de terceros
- Conexión a un servicio de IA en la nube

La velocidad depende principalmente del hardware disponible y del modelo utilizado.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/RomelAnte/ai_screen_assistant.git
cd ai_screen_assistant
```

### 2. Crear el entorno virtual

En Windows:

```powershell
python -m venv .venv
```

Activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

y después:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Instalar Ollama

Instala Ollama desde su sitio oficial:

https://ollama.com/

Comprueba que esté funcionando:

```bash
ollama --version
```

### 5. Descargar el modelo

Por defecto:

```bash
ollama pull qwen2.5vl:7b
```

También puedes utilizar otro modelo multimodal compatible y modificar:

```python
OLLAMA_MODEL = "nombre-del-modelo"
```

en `config.py`.

### 6. Ejecutar

```bash
python main.py
```

La aplicación permanecerá ejecutándose en segundo plano.

Presiona:

```text
F8
```

para analizar la pantalla.

## Ejemplo de uso

1. Abre un cuestionario, ejercicio o problema.
2. Asegúrate de que el contenido que quieres analizar sea visible.
3. Presiona `F8`.
4. AI Screen Assistant captura la pantalla.
5. Ollama analiza la imagen.
6. La aplicación muestra:

```text
RESPUESTA:
...

EXPLICACIÓN:
...

CÓDIGO:
...
```

El formato puede variar dependiendo del contenido analizado.

## Arquitectura

El proyecto está dividido en componentes pequeños:

```text
ai_screen_assistant/
│
├── main.py
├── config.py
├── ollama_client.py
├── screen_capture.py
├── response_parser.py
├── requirements.txt
│
├── ui/
│   ├── response_window.py
│   ├── selection_window.py
│   └── __init__.py
│
├── tests/
│   ├── test_app_components.py
│   └── __init__.py
│
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

### `main.py`

Controla el ciclo principal de la aplicación, el hotkey global y el trabajo en segundo plano.

### `config.py`

Centraliza:

- modelo de Ollama;
- URL de la API;
- tamaño máximo de imagen;
- hotkey;
- dimensiones de la interfaz;
- timeout;
- prompt del modelo.

### `screen_capture.py`

Se encarga de obtener la captura de pantalla y prepararla para el procesamiento.

### `ollama_client.py`

Gestiona la comunicación con la API local de Ollama y el envío de la imagen al modelo.

### `response_parser.py`

Separa la respuesta generada por el modelo en:

- respuesta;
- explicación;
- código.

### `ui/`

Contiene las interfaces de PySide6.

### `tests/`

Contiene pruebas de componentes del proyecto.

## Privacidad

AI Screen Assistant utiliza un modelo ejecutado localmente mediante Ollama.

La aplicación captura la pantalla cuando se activa el análisis y envía esa imagen a la instancia local de Ollama.

Por defecto:

```text
Aplicación
    ↓
Captura
    ↓
Ollama local
    ↓
Modelo local
    ↓
Respuesta
```

No se necesita enviar la captura a un servidor externo de IA.

Aun así, debes tener cuidado con la información visible en pantalla. No captures información sensible que no quieras procesar.

## Uso responsable

AI Screen Assistant fue creado como herramienta de estudio y práctica.

Está pensado para:

- aprender;
- practicar;
- comprender errores;
- estudiar cuestionarios;
- experimentar con modelos multimodales locales.

No está diseñado específicamente para utilizarse durante evaluaciones calificadas, exámenes o actividades donde el uso de asistencia externa esté prohibido.

El usuario es responsable de utilizar la herramienta respetando las reglas de cada actividad.

## Rendimiento

El análisis mediante modelos de visión local puede ser considerablemente más lento que utilizar una API remota optimizada.

El tiempo de respuesta depende principalmente de:

- CPU;
- GPU;
- memoria disponible;
- tamaño del modelo;
- tamaño de la imagen;
- configuración de Ollama.

Actualmente el proyecto reduce el tamaño de la captura antes de enviarla al modelo:

```python
MAX_IMAGE_SIDE = 1600
```

La optimización del rendimiento es una de las prioridades del roadmap.

## Roadmap

### Próximamente

- [ ] Reducir el tiempo de respuesta.
- [ ] Probar modelos de visión más pequeños.
- [ ] Utilizar `keep_alive` para evitar recargas innecesarias del modelo.
- [ ] Conectar el selector de región al flujo principal.
- [ ] Permitir analizar únicamente una zona de la pantalla.
- [ ] Guardar historial de preguntas.
- [ ] Marcar preguntas incorrectas para repasarlas.
- [ ] Generar quizzes de práctica a partir de apuntes.
- [ ] Mejorar la gestión de errores.
- [ ] Configurar modelo y servidor desde la interfaz.
- [ ] Crear ejecutable para Windows.
- [ ] Automatizar pruebas mediante GitHub Actions.

### Soporte multiplataforma

El objetivo a medio plazo es llevar AI Screen Assistant a:

| Plataforma | Estado |
|---|---|
| Windows | Disponible |
| Linux | Planeado |
| macOS | Planeado |

La interfaz está construida con PySide6, por lo que puede reutilizarse entre sistemas operativos. Sin embargo, la captura de pantalla y los atajos globales requieren adaptación y pruebas específicas para cada plataforma.

El objetivo no es simplemente cambiar el sistema operativo declarado como compatible, sino conseguir un comportamiento equivalente en cada plataforma.

## Contribuir

Las contribuciones son bienvenidas.

Puedes:

- reportar errores;
- proponer funcionalidades;
- mejorar la documentación;
- optimizar el procesamiento;
- añadir soporte para nuevos sistemas operativos;
- añadir pruebas;
- mejorar la integración con modelos locales.

Consulta `CONTRIBUTING.md` antes de realizar cambios importantes.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

Consulta [`LICENSE`](LICENSE) para más información.

## Autor

**Romel Ante**

Ingeniero en Sistemas de Información.

GitHub: [@RomelAnte](https://github.com/RomelAnte)

---

### Nota

Este proyecto se encuentra en desarrollo. Algunas funcionalidades descritas en el roadmap todavía no están implementadas.