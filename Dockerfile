FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy the project into the image
COPY ["pyproject.toml", "uv.lock", "./"]
RUN uv sync --frozen
COPY . .

# Expose the port your application will run on
EXPOSE 9696

# Command to run the application
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]