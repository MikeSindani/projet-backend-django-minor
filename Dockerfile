FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
# Installation de Redis (si vous utilisez Redis comme broker)


COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app/

# Exposer les ports
EXPOSE 8000 


# Lancer Redis en arrière-plan et démarrer Django
CMD python manage.py runserver 0.0.0.0:8000


