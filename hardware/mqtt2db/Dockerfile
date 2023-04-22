FROM python:3.11.2-alpine
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-u", "mqtt2db.py"]