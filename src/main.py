import sys
import os

# Adiciona o diretório src ao path para importações relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from downloader import baixar_video
from transcriber import transcrever_audio
from cutter import cortar_clipe_vertical

def executar_pipeline():
    print("==========================================")
    print("      WIX AUTOCUT ENGINE - PIPELINE       ")
    print("  Desenvolvedoras: Wislainy & Tawany      ")
    print("==========================================")
    
    url_alvo = input("Cole a URL do vídeo do YouTube: ").strip()
    
    if not url_alvo:
        print("[ERRO] Nenhuma URL informada. Encerrando o processo.")
        return

    try:
        # Etapa 1: Ingestão / Download
        arquivo_video = baixar_video(url_alvo, pasta_saida="downloads")
        
        # Etapa 2: Transcrição e Mapeamento de Tempos (Whisper)
        dados_transcricao = transcrever_audio(arquivo_video, nome_modelo="base")
        
        print("\n--- AMOSTRA DE TRECHOS DETECTADOS ---")
        segmentos = dados_transcricao.get("segments", [])
        
        for i, segmento in enumerate(segmentos[:5]):
            inicio = segmento["start"]
            fim = segmento["end"]
            texto = segmento["text"]
            print(f"[{inicio:.2f}s - {fim:.2f}s]: {texto}")
            
        print(f"\n[INFO] Total de segmentos processados: {len(segmentos)}")
        
        # Etapa 3: Corte automático do primeiro clipe de destaque como teste
        if segmentos:
            print("\n[INFO] Iniciando corte do primeiro segmento detectado...")
            primeiro_trecho = segmentos[0]
            t_inicio = primeiro_trecho["start"]
            t_fim = primeiro_trecho["end"]
            
            # Garante um tempo mínimo de clipe se o primeiro for muito curto (ex: pelo menos 5 segundos)
            if (t_fim - t_inicio) < 3.0:
                t_fim = t_inicio + 5.0
                
            cortar_clipe_vertical(
                caminho_video=arquivo_video,
                tempo_inicio=t_inicio,
                tempo_fim=t_fim,
                nome_saida="primeiro_clipe_9_16.mp4",
                pasta_saida="output_clips"
            )
            print("[SUCESSO] Pipeline completo executado com sucesso!")
        else:
            print("[AVISO] Nenhum segmento válido encontrado para corte.")

    except Exception as e:
        print(f"[ERRO CRÍTICO NO PIPELINE]: {str(e)}")

if __name__ == "__main__":
    executar_pipeline()
