# app/Dockerfile

# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instale dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copie todo o conteúdo do diretório app para o contêiner
COPY . .

# Exponha a porta que a aplicação irá rodar
EXPOSE 8080

# Defina as variáveis de ambiente necessárias
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Comando para rodar a aplicação
CMD ["flask", "run"]
