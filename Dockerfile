FROM python:3.13.0-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python -m unittest tests/test_read_questionnaire.py

CMD ["python", "read_questionnaire.py"]
