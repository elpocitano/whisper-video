#!/usr/bin/env python3

"""
WHISPER VIDEO - Transcripción automática de videos de YouTube/TikTok/etc.

Pipeline completo para descargar videos, extraer audio y transcribir con Whisper.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 REQUISITOS:
    • yt-dlp        $ pip install yt-dlp
    • ffmpeg        $ sudo apt install ffmpeg (Linux)
    • openai-whisper $ pip install openai-whisper

💻 USO:
    python whisper_video.py "https://youtube.com/watch?v=..."

✍️  AUTORES:
    Desarrollador - UNSJ (Universidad Nacional de San Juan)
    Fecha: Enero 2026

📄 LICENCIA: MIT License
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# IMPORTS
import subprocess
import os
from pathlib import Path
import whisper
import sys
from typing import Optional, Union # str | None


# CONSTANTES
MODELOS_DISPONIBLES = ["turbo", "base", "small", "medium", "large"]
FPS_AUDIO = 16000
MAX_RESOLUCION = 720

# FUNCIONES
def descargar_video(
    url: str, 
    output_dir: str = 'descargas'
) -> Optional[str]:
    """
    Descarga video de YouTube/TikTok/etc usando yt-dlp.
    
    Args:
        url (str): URL del video a descargar
        output_dir (str): Carpeta destino (crea si no existe)
    
    Returns:
        str | None: Ruta del archivo descargado o None si falla
    
    Raises:
        subprocess.CalledProcessError: Si yt-dlp falla
    """
    Path(output_dir).mkdir(exist_ok=True)
    cmd = [
        "yt-dlp", 
        "-f", "18",  # ← 360p MP4 SIEMPRE funciona
        "-o", f"{output_dir}/%(title)s.%(ext)s", 
        url
    ]

    subprocess.run(cmd, check=True)
    
    files = list(Path(output_dir).glob("*"))
    if not files:
        return None
    return str(max(files, key=os.path.getctime))



def extraer_audio(
    video_path: str, 
    output_path: Optional[str] = None
) -> str:
    """
    Extrae audio mono 16kHz del video usando FFmpeg.
    
    Args:
        video_path (str): Ruta al archivo de video
        output_path (str, optional): Ruta de salida WAV. 
            Defaults to <nombre_video>.wav
    
    Returns:
        str: Ruta del archivo WAV generado
    
    Raises:
        subprocess.CalledProcessError: Si FFmpeg falla
    """
    if output_path is None:
        output_path = f"{Path(video_path).stem}.wav"
    
    cmd = [
        "ffmpeg", "-i", video_path, 
        "-vn", "-acodec", "pcm_s16le", 
        "-ar", "16000", "-ac", "1", 
        output_path, "-y"
    ]
    subprocess.run(cmd, check=True)
    return output_path


def transcribir(
    audio_path: str, 
    model_name: str = "turbo"
) -> str:
    """
    Transcribe audio usando Whisper (OpenAI).
    
    Args:
        audio_path (str): Ruta al archivo WAV
        model_name (str): Modelo Whisper ('turbo', 'base', 'small', etc.)
    
    Returns:
        str: Texto transcrito en español
    
    Raises:
        RuntimeError: Si falla la carga del modelo
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language="es")
    return result["text"]


def main(url: str) -> None:
    """
    Pipeline completo: descarga → audio → transcripción.
    """
    print("📥 Descargando video...")
    video = descargar_video(url)
    if not video:
        print("❌ Error: No se pudo descargar el video")
        sys.exit(1)
    
    print(f"✅ Video: {video}")
    print("🔊 Extrayendo audio...")
    audio = extraer_audio(video)
    print(f"✅ Audio: {audio}")
    print("🗣️  Transcribiendo...")
    texto = transcribir(audio)
    print("\n" + "="*50)
    print("📄 TRANSCRIPCIÓN COMPLETA")
    print("="*50)
    print(texto)

# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("💡 Uso: python whisper_video.py <URL_VIDEO>")
        print("Ejemplo: python whisper_video.py 'https://youtube.com/watch?v=...'")
        sys.exit(1)
    
    url = sys.argv[1]
    main(url)

