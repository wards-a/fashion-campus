FROM python:3.9-slim-buster
WORKDIR /fashion-campus
COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
ENV FLASK_HOST_RUN=0.0.0.0
ENV FLASK_DEBUG=1
ENV FLASK_APP=app/main
COPY . .
CMD ["flask", "run"]
