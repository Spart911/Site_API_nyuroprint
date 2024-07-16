FROM python:3.10 AS builder

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]