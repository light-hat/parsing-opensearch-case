FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV SELENIUM_REMOTE_URL="http://selenium:4444/wd/hub"

CMD ["python3", "main.py"]
