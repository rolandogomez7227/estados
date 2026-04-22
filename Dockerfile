FROM public.ecr.aws/docker/library/python:3.9-slim

WORKDIR /app

# Instalamos la librería de AWS
RUN pip install boto3

COPY app.py .
COPY Estados.txt .

CMD ["python", "app.py"]