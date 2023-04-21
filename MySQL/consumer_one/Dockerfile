# parent image for consumer one = version of python on local system
FROM python:3.11.0

# working directory = instance of flask app
WORKDIR /app

COPY requirements.txt .

# install the required packages mentioned in requirements.txt
RUN pip install -r requirements.txt

COPY healthcheck.py .

# run this command to start consumer one
CMD ["python", "healthcheck.py"]
