# Whisper Video Transcriber
Script simple en Python para descargar videos de internet, extraer audio y transcribir con Whisper AI en modo local.  
Testeado con CachyOS/Arch Linux. Funciona 100% offline después de descargar modelos.

## Características
- Descarga videos de YouTube/TikTok/etc con yt-dlp.
- Extrae audio optimizado (16kHz mono WAV para Whisper).
- Transcribe en español con modelo turbo/base.
- Instalación fácil con pipx (sin conflictos Python).
- 100% local, sin APIs externas. [github](https://github.com/yt-dlp/yt-dlp/wiki/Installation)

## Requisitos previos
- CachyOS/Arch Linux.
- Python 3.11+.
- FFmpeg instalado.
- ~2GB espacio para modelos. [archlinux](https://archlinux.org/packages/extra/any/python-openai-whisper/)

## Instalación paso a paso

### 01. Actualizar sistema
```bash
sudo pacman -Syu
```

### 02. Instalar dependencias
```bash
sudo pacman -S ffmpeg yt-dlp python-pipx
```

### 03. Instalar Whisper
```bash
pipx install openai-whisper
pipx ensurepath
source ~/.zshrc  # Si usas Zsh
```

### 04. Verificar instalación
```bash
whisper --help
yt-dlp --version
```

## Guía rápida de uso
```bash
mkdir whisper-video && cd whisper-video
# Copiar whisper_video.py aquí

python whisper_video.py "https://youtube.com/watch?v=VIDEO_ID"
```
**Salida esperada:**  
```
Descargando video...
Video: downloads/Título del Video.mp4
Extrayendo audio...
Audio: downloads/Título del Video.wav
Transcribiendo...

--- TRANSCRIPCIÓN ---
Hola, este es el texto transcrito del video...
```

## Personalización

### Modelos disponibles
```python
# Cambiar en transcribir(model_name=):
"tiny"     # 39MB, rápido
"base"     # 74MB, balanceado  
"small"    # 244MB, preciso
"medium"   # 769MB, muy preciso
"large"    # 1550MB, máximo
"turbo"    # Optimizado velocidad
```

### Idiomas
```python
model.transcribe(audio_path, language="es")  # Español
model.transcribe(audio_path)                 # Auto-detecta
```

## Estructura de archivos
```
whisper-video/
├── whisper_video.py
├── downloads/          # Auto-creada
│   ├── Título.mp4
│   └── Título.wav
└── README.md
```

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `command not found: whisper` | `source ~/.zshrc` o reiniciar terminal |
| `externally-managed-environment` | Usar `pipx` |
| Descarga falla | `sudo pacman -Syu yt-dlp` |
| Espacio insuficiente | Modelos en `~/.local/share/whisper/` [github](https://github.com/pypa/pipx) |

## Limitaciones
- Videos >2GB fallan en poca RAM.
- Modelos grandes tardan en CPU sin GPU.
- Solo texto plano (sin timestamps).

## Rendimiento Dell Inspiron 15 3000
| Modelo | RAM | Tiempo (1min video) |
|--------|-----|---------------------|
| tiny   | 1GB | 15s                |
| base   | 2GB | 45s                |
| turbo  | 1.5GB| 30s (recomendado)  |

## Contribuir
1. Fork el proyecto.
2. `git checkout -b feature/nueva-funcion`
3. `git commit -m 'Agregar X'`
4. `git push origin feature/nueva-funcion`
5. Pull Request. [github](https://github.com/pypa/pipx)

## Licencia
MIT License - ver LICENSE o [aquí](https://opensource.org/licenses/MIT). [github](https://github.com/pypa/pipx)

## Agradecimientos
- OpenAI Whisper por el modelo ASR.
- yt-dlp comunidad por descargas robustas.
- Foros CachyOS/ArchWiki por soluciones pipx/Zsh.
- Tutoriales YouTube para testing local.

**Creado por elpocitano** | Enero 2026
