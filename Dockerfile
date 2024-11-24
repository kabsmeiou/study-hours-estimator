FROM python:3.12-slim-bookworm

# set the working directory inside the container
WORKDIR /app

# copy the project files into the image
COPY . /app

# install dependencies using pip from the requirements.txt
RUN pip install -r requirements.txt

# expose the port
EXPOSE 9696

# run the script.py file in src/ with gunicorn
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "src.script:app"]