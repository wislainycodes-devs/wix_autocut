import os
import subprocess

def cortar_clipe_vertical(caminho_video: str, tempo_inicio: float, tempo_fim: float, nome_saida: str = "clipe_cortado.mp4", pasta_saida: str = "output_clips") -> str:
    """
    Utiliza o FFmpeg para recortar um trecho específico do vídeo e redimensioná-lo
    para o formato vertical (9:16 - resolução 1080x1920), centralizando a imagem.
    """
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_final = os.path.join(pasta_saida, nome_saida)
    
    # Filtro do FFmpeg: 
    # 1. crop: recorta um quadrado ou a proporção central ideal para transformar em vertical
    # 2. scale: redimensiona para 1080x1920 (9:16)
    duracao = tempo_fim - tempo_inicio
    
    # Comando otimizado do FFmpeg para corte e conversão vertical (9:16)
    # Pegamos a altura original e ajustamos a largura proporcional para 9:16 centralizado
    filtro_video = "scale=w='ih*9/16':h=ih,crop=w='ih*9/16':h=ih,scale=1080:1920"
    
    comando = [
        'ffmpeg',
        '-y',                  # Sobrescreve o arquivo de saída se já existir
        '-ss', str(tempo_inicio), # Tempo de início do corte
        '-i', caminho_video,   # Arquivo de vídeo de entrada
        '-t', str(duracao),    # Duração do clipe
        '-vf', filtro_video,   # Aplica o filtro de proporção 9:16
        '-c:v', 'libx264',     # Codec de vídeo padrão
        '-c:a', 'aac',         # Codec de áudio padrão
        caminho_final
    ]
    
    print(f"[INFO] Renderizando clipe vertical de {tempo_inicio:.2f}s até {tempo_fim:.2f}s...")
    
    # Executa o comando do FFmpeg via terminal do sistema
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if resultado.returncode != 0:
        raise Exception(f"Erro ao processar o vídeo com FFmpeg: {resultado.stderr}")
        
    print(f"[SUCESSO] Clipes salvos em: {caminho_final}")
    return caminho_final
