# syntax=docker/dockerfile:1

FROM postgres:13.3
ENV POSTGRES_PASSWORD=pass
ENV POSTGRES_USER=cm_user
ENV POSTGRES_DB=cm
COPY dump.sql /docker-entrypoint-initdb.d/.