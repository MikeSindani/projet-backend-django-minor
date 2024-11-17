FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
# Installation de Redis (si vous utilisez Redis comme broker)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app/

# Exposer les ports
EXPOSE 8000  # Pour Django
EXPOSE 6379  # Pour Redis
EXPOSE 5432  # Pour PostgreSQL (si utilisé)

# Lancer Redis en arrière-plan et démarrer Django
CMD redis-server --daemonize yes && python manage.py runserver 0.0.0.0:8000


