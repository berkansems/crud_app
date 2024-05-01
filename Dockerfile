FROM python:3.9-alpine3.13
LABEL maintainer='berkansems@gmail.com'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

WORKDIR /app
EXPOSE 8000
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"
# This sets the user that the Docker container will run as to django-user. It's a security best practice to not run the application as the root user.
USER django-user