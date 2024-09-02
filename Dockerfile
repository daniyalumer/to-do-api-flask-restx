FROM python:3.11-slim

WORKDIR /to-do-flask-restx

COPY requirements.txt /to-do-flask-restx/

RUN pip install -r requirements.txt

COPY . /to-do-flask-restx/

EXPOSE 5000

CMD ["python", "app.py"]
