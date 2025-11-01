# Dockerfile
FROM python:3.11-slim

WORKDIR /code

# Instalar dependencias
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ .

# Exponer puerto
EXPOSE 8000

# Comando de inicio - El módulo main está en app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
