FROM python:3.9-slim-buster as base
WORKDIR /fashion-campus
COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_SKIP_DOTENV=1
ENV FLASK_APP=app/main
COPY . .
CMD ["flask", "run"]
