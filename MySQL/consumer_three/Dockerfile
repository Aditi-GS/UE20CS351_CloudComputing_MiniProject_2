# parent image of consumer two = python version on local system
FROM python:3.11.0

# working directory = instance of flask app
WORKDIR /app

# copy contents of current dir into the container at /app which will be set as the working dir
COPY . /app

# install the required packages mentioned in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port used by the application
EXPOSE 8081

# Define environment variables
ENV RABBITMQ_HOST="rabbitmq"
ENV RABBITMQ_PORT=15672
ENV RABBITMQ_USER="guest"
ENV RABBITMQ_PASSWORD="guest"

# Run insert.py when the container launches
CMD ["python", "deletion.py"]
