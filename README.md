# Wix Autocut Engine
Software automatizado de extração, processamento e renderização de clipes verticais (Shorts, Reels e TikTok) a partir de transmissões longas e vídeos de reações. Desenvolvido para otimizar a criação de conteúdo em alta escala.
## Desenvolvedoras* **Wislainy Fontes dos Santos*** **Tawany Fontes dos Santos**
---
## Estrutura do Projeto
O repositório está organizado em uma arquitetura de *pipeline* modular:
```textwixtaw-autocut/├── src/ # Módulos de código-fonte em Python│ ├── downloader.py # Módulo de ingestão de vídeos via yt-dlp│ ├── transcriber.py # Módulo de processamento de áudio e transcrição (Whisper)│ ├── highlighter.py # Algoritmo de curadoria de trechos de alto impacto│ └── renderer.py # Renderização de legendas e enquadramento 9:16 (FFmpeg)├── downloads/ # Diretório temporário para armazenamento dos vídeos brutos├── output_clips/ # Diretório de destino para os clipes verticais prontos├── .gitignore # Arquivos ignorados pelo versionamento└── README.md # Documentação oficial do projeto
