FROM python:3.12.5-slim

# Atualizando e instalando pacotes essenciais, incluindo libpangoft2-1.0-0
RUN apt-get update && apt-get install -y \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \  
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    build-essential \
    libpq-dev \
  && apt-get clean

# Copiar arquivos do projeto
COPY . /app/

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta 8000
EXPOSE 8000

# Comando para rodar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
