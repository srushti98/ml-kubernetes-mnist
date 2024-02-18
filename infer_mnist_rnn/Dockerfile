FROM python:3.8-slim
LABEL authors="srushtipawar"

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py /app

EXPOSE 7860
CMD ["python3", "main.py"]