# syntax=docker/dockerfile:1
FROM python:3.9.10-bullseye
WORKDIR /app
COPY . .
RUN pip3 install django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
