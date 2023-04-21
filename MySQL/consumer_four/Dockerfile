# parent image for consumer four = version of python on local system
FROM python:3.11.0

# working directory = instance of flask app
WORKDIR /app

COPY . /app

# install the required packages mentioned in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

# Define environment variables
ENV MYSQL_DATABASE=student_database
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root
ENV MYSQL_HOST=localhost

# run this command to start consumer four
CMD ["python", "read.py"]
