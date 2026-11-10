import os
import sys
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from downloader import baixar_video
from transcriber import transcrever_audio
from cutter import cortar_clipe_vertical

def processar_pipeline_web(arquivo_upload, url_alvo: str):
    try:
        if arquivo_upload:
            print(f"[INFO] Usando arquivo enviado: {arquivo_upload}")
            arquivo_video = arquivo_upload
        elif url_alvo and url_alvo.strip():
            print(f"[INFO] Baixando: {url_alvo}")
            arquivo_video = baixar_video(url_alvo, pasta_saida="downloads")
        else:
            return "Envie um arquivo de vídeo ou insira uma URL do YouTube.", None

        print("[INFO] Transcrevendo com Whisper...")
        dados_transcricao = transcrever_audio(arquivo_video, nome_modelo="base")
        segmentos = dados_transcricao.get("segments", [])

        if not segmentos:
            return "Nenhum segmento de áudio detectado no vídeo.", None

        primeiro_trecho = segmentos[0]
        t_inicio = primeiro_trecho["start"]
        t_fim = primeiro_trecho["end"]

        if (t_fim - t_inicio) < 3.0:
            t_fim = t_inicio + 5.0

        print("[INFO] Renderizando clipe vertical com FFmpeg...")
        caminho_clipe = cortar_clipe_vertical(
            caminho_video=arquivo_video,
            tempo_inicio=t_inicio,
            tempo_fim=t_fim,
            nome_saida="clipe_web_9_16.mp4",
            pasta_saida="output_clips"
        )

        texto_resumo = f"**Trecho Cortado:** [{t_inicio:.2f}s - {t_fim:.2f}s]\n\n> \"{primeiro_trecho['text']}\""
        return texto_resumo, caminho_clipe

    except Exception as e:
        return f"Erro crítico durante o processamento: {str(e)}", None

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 Wix Autocut Engine")
    gr.Markdown("Transforme vídeos longos em clipes verticais (9:16) automaticamente com Inteligência Artificial e FFmpeg.")

    with gr.Row():
        with gr.Column():
            arquivo_input = gr.File(label="Enviar vídeo (recomendado)", file_types=["video"])
            url_input = gr.Textbox(label="Ou URL do YouTube (pode falhar no servidor)", placeholder="https://www.youtube.com/watch?v=...")
            botao_executar = gr.Button("Gerar Clipe 9:16", variant="primary")

        with gr.Column():
            output_texto = gr.Markdown(label="Status / Transcrição do Trecho")
            output_video = gr.Video(label="Clipe Vertical Gerado")

    botao_executar.click(
        fn=processar_pipeline_web,
        inputs=[arquivo_input, url_input],
        outputs=[output_texto, output_video]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
