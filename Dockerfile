FROM python:3.9.5-alpine3.12

RUN apk add build-base --no-cache
COPY . .
RUN pip install -r requirements.txt && \
    mkdir {target,conf}

ENTRYPOINT ["python3", "app/main.py"]