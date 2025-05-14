# filepath: c:\Users\hp\OneDrive\Documentos\DistribuidosParcial\recervas_citas\consumer\Dockerfile
FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

CMD ["python", "consumer/consumer.py"]