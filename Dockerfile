# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Django related env variables
ENV DJANGO_SETTINGS_MODULE=config.settings.base

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    # PostgreSQL client for pg_isready & psql
    postgresql-client \
    # PostgreSQL headers for psycopg2
    libpq-dev \
    # Pillow dependencies
    libjpeg-dev \
    # CairoSVG dependencies
    libcairo2 \
    # Compiler
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini VM's code directory
RUN mkdir -p /code

# Set the working directory
WORKDIR /code

# Copy requirements
COPY requirements.txt /tmp/requirements.txt

# Copy project source
COPY ./src /code

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Set default Django project name
ARG PROJ_NAME="config"

# Create a startup script to wait for DB & run the app
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n" >> ./paracord_runner.sh && \
    printf "python manage.py collectstatic --noinput\n" >> ./paracord_runner.sh && \
    printf "echo 'Running migrations...'\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate\n\n" >> ./paracord_runner.sh && \
    printf "echo 'Starting Gunicorn...'\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh


# Make script executable
RUN chmod +x paracord_runner.sh

# Run the Django project via the runtime script
CMD ["/code/paracord_runner.sh"]