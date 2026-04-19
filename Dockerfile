# Usamos una imagen base de Python ligera
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el archivo del mostrador
COPY mostrador.py .

EXPOSE 8080

# Usaremos un puerto distinto (8080) para que no choque con el emisor(8000) en el contenedor final
CMD ["uvicorn", "mostrador:app", "--host", "0.0.0.0", "--port", "8080"]
