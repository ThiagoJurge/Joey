# Use uma imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Gunicorn e o Supervisord
RUN pip install gunicorn supervisor

# Copia todo o conteúdo do diretório atual para o diretório de trabalho dentro do container
COPY . .

# Copia o arquivo de configuração do supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exponha a porta 81
EXPOSE 81

# Define o comando para rodar o supervisor que gerenciará os processos
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
