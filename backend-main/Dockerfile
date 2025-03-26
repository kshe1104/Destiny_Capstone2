FROM python:3.11-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
