FROM python:3.12 AS builder

COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "10", "--proxy-headers", "--forwarded-allow-ips", "*", "--reload", "--ssl-keyfile", "ssl/certificate.key.pem", "--ssl-certfile", "ssl/certificate.crt.pem"]