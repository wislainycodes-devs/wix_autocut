import whisper

def transcrever_audio(caminho_video: str, nome_modelo: str = "base") -> dict:
    """
    Carrega o modelo Whisper localmente, executa a transcrição do arquivo de vídeo
    e retorna o dicionário estruturado com segmentos, textos e timestamps.
    """
    print(f"[INFO] Carregando modelo Whisper ('{nome_modelo}')...")
    modelo = whisper.load_model(nome_modelo)
    
    print("[INFO] Processando transcrição e mapeamento temporal do áudio...")
    resultado = modelo.transcribe(caminho_video, language="pt", verbose=False)
    
    print("[SUCESSO] Transcrição concluída com sucesso!")
    return resultado
