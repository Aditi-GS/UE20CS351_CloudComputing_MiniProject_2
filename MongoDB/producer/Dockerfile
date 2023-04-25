# basic python image
FROM python:3.10.9

COPY requirements.txt .

# install pika to access rabbitmq
RUN pip install -r requirements.txt

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# declare the source directory
WORKDIR /app

# copy the file
COPY . .

ENTRYPOINT [ "python3" ]

# start command
CMD [  "producer.py" ]


EXPOSE 5100
