FROM python:3.9.5-alpine3.12

COPY . .
RUN apk add build-base libffi-dev --no-cache && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    mkdir {target,conf}

ENTRYPOINT ["python3", "app/main.py"]