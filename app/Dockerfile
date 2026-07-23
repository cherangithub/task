# buildstage 1
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#build stage 2 
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN useradd  appuser

USER appuser

EXPOSE 5000

CMD ["python3", "app.py"]