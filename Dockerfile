FROM python:3.8-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN python -m pip install --no-cache-dir -U pip pip-tools

WORKDIR /application

# Install backend deps
COPY requirements.txt /application/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /application
RUN python manage.py create_db
# TODO Remove debug level in production
CMD ["gunicorn", "--bind", "0.0.0.0:6009",  "--workers", "4", "--log-level", "debug", "wsgi:application"]
