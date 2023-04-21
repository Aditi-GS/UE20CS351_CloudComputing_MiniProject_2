# parent image for producer = version of python on local system
FROM python:3.11.0

# working directory = instance of flask app
WORKDIR /app

# copy contents of current dir into the container at /app which will be set as the working dir
COPY . /app

# install the required packages mentioned in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the flask app is running on 
EXPOSE 5000

# run this command to start the producer
CMD ["python", "producer.py"]
