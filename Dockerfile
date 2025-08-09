FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema incluindo netcat para verificar conexão
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requirements
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Copia e torna executável o script de entrada
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Define o script como ponto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]