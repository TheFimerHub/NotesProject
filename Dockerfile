FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80