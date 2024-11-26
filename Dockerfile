FROM python:3.12-slim-bookworm

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io && apt-get clean

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# expose the port
EXPOSE 9696

# run the script.py file in src/ with gunicorn using uv
ENTRYPOINT ["uv", "run", "gunicorn", "--bind=0.0.0.0:9696", "src.script:app"]