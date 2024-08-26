# Use uma imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Gunicorn
RUN pip install gunicorn

# Copia todo o conteúdo do diretório atual para o diretório de trabalho dentro do container
COPY . .

# Exponha a porta 81
EXPOSE 81

# Define o comando para rodar a aplicação com Gunicorn na porta 81
CMD ["gunicorn", "-b", "0.0.0.0:81", "app:app"]
