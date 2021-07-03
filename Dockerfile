FROM python:3.9.5-alpine3.12

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app/main.py"]