FROM python:3.9.6-slim-buster

COPY . .
RUN pip install -r requirements.txt && \
    mkdir {target,conf}

ENTRYPOINT ["python3", "app/main.py"]