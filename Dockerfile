# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    liberasurecode-dev \
    && apt-get clean

# Install Poetry
RUN pip install poetry

# Install pyeclib directly using pip to bypass the Poetry issue
RUN pip install --no-cache-dir uvicorn

# Copy only the pyproject.toml and poetry.lock first (for caching)
COPY pyproject.toml poetry.lock* /app/


# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-interaction --no-ansi
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the project files
COPY . /app
