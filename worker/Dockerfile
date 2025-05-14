FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV PYTHONPATH=/code

CMD ["python", "worker/worker.py"]