FROM python:3.12-slim

#working directory in the container 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5003

CMD ["python", "notification_service.py"]
