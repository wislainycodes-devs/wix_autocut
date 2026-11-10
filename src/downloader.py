import os
import yt_dlp

def baixar_video(url: str, pasta_saida: str = "downloads") -> str:
    os.makedirs(pasta_saida, exist_ok=True)

    # Define o caminho absoluto para o cookies.txt na raiz do projeto
    caminho_cookies = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')
    
    # Se estiver rodando um nível acima, tenta buscar na pasta atual de trabalho
    if not os.path.exists(caminho_cookies):
        caminho_cookies = 'cookies.txt'

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(pasta_saida, 'video_original.mp4'),
        'quiet': False,
        'no_warnings': True,
        'cookiefile': caminho_cookies,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    print(f"[INFO] Iniciando o download com o cookie: {caminho_cookies}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    caminho_arquivo = os.path.join(pasta_saida, 'video_original.mp4')
    print(f"[SUCESSO] Vídeo baixado em: {caminho_arquivo}")
    return caminho_arquivo
