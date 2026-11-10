import os
import sys
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from downloader import baixar_video
from transcriber import transcrever_audio
from cutter import cortar_clipe_vertical

def processar_pipeline_web(url_alvo: str):
    if not url_alvo.strip():
        return "Por favor, insira uma URL válida do YouTube.", None

    try:
        # Etapa 1: Download
        print(f"[INFO] Baixando: {url_alvo}")
        arquivo_video = baixar_video(url_alvo, pasta_saida="downloads")
        
        # Etapa 2: Transcrição
        print("[INFO] Transcrevendo com Whisper...")
        dados_transcricao = transcrever_audio(arquivo_video, nome_modelo="base")
        segmentos = dados_transcricao.get("segments", [])
        
        if not segmentos:
            return "Nenhum segmento de áudio detectado no vídeo.", None
            
        # Pega o primeiro trecho para teste de corte
        primeiro_trecho = segmentos[0]
        t_inicio = primeiro_trecho["start"]
        t_fim = primeiro_trecho["end"]
        
        if (t_fim - t_inicio) < 3.0:
            t_fim = t_inicio + 5.0
            
        # Etapa 3: Corte 9:16
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

# Interface Gráfica com Gradio (tema moderno e limpo)
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 Wix Autocut Engine")
    gr.Markdown("Transforme vídeos longos do YouTube em clipes verticais (9:16) automaticamente com Inteligência Artificial e FFmpeg.")
    
    with gr.Row():
        with gr.Column():
            url_input = gr.Textbox(label="URL do Vídeo do YouTube", placeholder="https://www.youtube.com/watch?v=...")
            botao_executar = gr.Button("Gerar Clipe 9:16", variant="primary")
            
        with gr.Column():
            output_texto = gr.Markdown(label="Status / Transcrição do Trecho")
            output_video = gr.Video(label="Clipe Vertical Gerado")
            
    botao_executar.click(
        fn=processar_pipeline_web,
        inputs=url_input,
        outputs=[output_texto, output_video]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
