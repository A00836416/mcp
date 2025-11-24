FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip setuptools wheel

# Instala requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto completo
COPY . .

# Ejecuta FastAPI (NO agent.py)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
