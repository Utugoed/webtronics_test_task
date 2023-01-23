FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY docker-entrypoint-initdb.d /docker-entrypoint-initdb.d

COPY . /app
WORKDIR /app/
ENV PYTHONPATH=/app
EXPOSE 80