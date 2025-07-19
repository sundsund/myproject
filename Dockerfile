FROM python:3.13.0-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "read_fhir.py"]
