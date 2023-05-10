# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /AI
COPY .. .

RUN pip3 install -r requirements
CMD ["python3", "main_AI_service.py", "0.0.0.0", "5002"]

EXPOSE 5002