import os
import yt_dlp

def baixar_video(url: str, pasta_saida: str = "downloads") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(pasta_saida, 'video_original.mp4'),
        'quiet': False,
        'no_warnings': True,
        # Linha essencial para autenticar o bot com os seus cookies:
        'cookiefile': 'cookies.txt',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    print("[INFO] Iniciando o download do conteúdo...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    caminho_arquivo = os.path.join(pasta_saida, 'video_original.mp4')
    print(f"[SUCESSO] Vídeo baixado em: {caminho_arquivo}")
    return caminho_arquivo
