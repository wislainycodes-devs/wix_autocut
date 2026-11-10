FROM python:3.10-slim

# Instala o FFmpeg e dependências essenciais do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta que o Gradio vai usar na nuvem
EXPOSE 7860

# Comando para iniciar a aplicação web
CMD ["python", "src/app.py"]
