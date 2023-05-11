# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
# WORKDIR /APP
COPY . .

RUN pip3 install -r requirements
CMD ["python3", "main.py", "0.0.0.0", "5000"]

EXPOSE 5000