FROM python:3.9-slim-buster
WORKDIR /fashion-campus
ENV FLASK_HOST_RUN=0.0.0.0
ENV FLASK_APP=app/main
COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
COPY . .
CMD ["flask", "run"]
