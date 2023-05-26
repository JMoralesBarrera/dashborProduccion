FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV FLASK_APP app.py
ENV FLSK_RUN_HOST 0.0.0.0
EXPOSE 8000

# copiar el archivo de la plantilla al contenedor
COPY Plantilla.xlsx .

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY src/ .

CMD ["python3", "app.py", "runserver", "0.0.0.0:8000"]
