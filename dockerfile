FROM python:3.9-slim-buster
WORKDIR /fashion-campus
COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
COPY . .
CMD ["flask", "run"]