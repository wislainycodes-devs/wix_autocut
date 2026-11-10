import os
import yt_dlp

def baixar_video(url: str, pasta_saida: str = "downloads") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(pasta_saida, 'video_original.mp4'),
        'quiet': False,
        'no_warnings': True
    }

    print("[INFO] Iniciando o download do conteúdo...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    caminho_arquivo = os.path.join(pasta_saida, 'video_original.mp4')
    print(f"[SUCESSO] Vídeo baixado em: {caminho_arquivo}")
    return caminho_arquivo
