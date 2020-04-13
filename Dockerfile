# Use an official Python runtime as a parent image
FROM python:3.8
LABEL maintainer="hello@wagtail.io"

ARG SECRET_KEY
ENV SECRET_KEY $SECRET_KEY

ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV prod

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN python manage.py migrate --settings=general.settings.prod
RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000
CMD exec gunicorn idea2point0.wsgi:application --bind 0.0.0.0:8000 --workers 3
