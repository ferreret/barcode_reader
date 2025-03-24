# Imagen base de Python
FROM python:3.12-slim

# Directorio de trabajo del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Actualiza los repositorios e instala la librería del sistema zbar
RUN apt-get update && apt-get install -y libzbar0

# COPIAMOS el archivo principal
COPY main.py .

# Definimos el puerto
EXPOSE 8000

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


