import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from downloader import baixar_video
from transcriber import transcrever_audio

def executar_pipeline():
    print("==========================================")
    print("      WIX AUTOCUT ENGINE - PIPELINE       ")
    print("  Desenvolvedora: Wislainy & Tawany       ")
    print("==========================================")

    url_alvo = input("Cole a URL do vídeo do YouTube: ").strip()

    if not url_alvo:
        print("[ERRO] Nenhuma URL informada. Encerrando o processo.")
        return

    try:
        arquivo_video = baixar_video(url_alvo, pasta_saida="downloads")
        dados_transcricao = transcrever_audio(arquivo_video, nome_modelo="base")

        print("\n--- AMOSTRA DE TRECHOS DETECTADOS ---")
        segmentos = dados_transcricao.get("segments", [])

        for i, segmento in enumerate(segmentos[:5]):
            inicio = segmento["start"]
            fim = segmento["end"]
            texto = segmento["text"]
            print(f"[{inicio:.2f}s - {fim:.2f}s]: {texto}")

        print(f"\n[INFO] Total de segmentos processados: {len(segmentos)}")
        print("[INFO] Próxima etapa do pipeline: Curadoria e Renderização FFmpeg (9:16).")

    except Exception as e:
        print(f"[ERRO CRÍTICO NO PIPELINE]: {str(e)}")

if __name__ == "__main__":
    executar_pipeline()
