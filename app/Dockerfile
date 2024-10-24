# app/Dockerfile

# Usar o Ubuntu 22.04 como imagem base
FROM ubuntu:22.04

# Definir o diretório de trabalho
WORKDIR /app

# Definir variáveis de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar as dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    netcat \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos de requisitos
COPY requirements.txt .

# Instalar as dependências Python
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar o restante do código, incluindo run.py agora dentro de app/
COPY . .

# Dar permissão de execução ao script de entrada
RUN chmod +x /app/entrypoint.sh

# Expor a porta que a aplicação irá rodar
EXPOSE 5000

# Definir o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
