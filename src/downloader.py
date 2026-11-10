import os
import shutil
import yt_dlp

COOKIES_SECRET = "/etc/secrets/cookies.txt"
COOKIES_TMP = "/tmp/cookies.txt"

def _cookies():
    if os.path.exists(COOKIES_SECRET):
        shutil.copy(COOKIES_SECRET, COOKIES_TMP)
        return COOKIES_TMP
    return None

def baixar_video(url: str, pasta_saida: str = "downloads") -> str:
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_saida, 'video_original.mp4')

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': caminho_arquivo,
        'quiet': False,
        'no_warnings': True,
        'cookiefile': _cookies(),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        if "Sign in" in str(e) or "bot" in str(e):
            raise RuntimeError("O YouTube bloqueou o servidor. Envie o arquivo de vídeo em vez do link.")
        raise

    return caminho_arquivo
