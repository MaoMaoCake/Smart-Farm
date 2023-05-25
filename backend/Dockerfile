FROM python:3.12.0b1-slim

WORKDIR /backend

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]