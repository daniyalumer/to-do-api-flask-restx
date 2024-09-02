FROM python:3.11-slim

WORKDIR /to-do-flask-restx

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_ENV=development

CMD ["python", "app.py"]
