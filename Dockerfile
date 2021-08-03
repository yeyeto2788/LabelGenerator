# Based image seleceted because of debian.
FROM python:3.8-buster

# Add all files from the repository.
COPY ./label_generator /code/label_generator
COPY ./requirements.txt /code/requirements.txt
COPY ./setup.py /code/setup.py

# Set working directory to the one we've just copied.
WORKDIR /code

RUN apt-get update && apt-get install wget unzip nano -y
# Get default fonts.
RUN wget --quiet https://assets.ubuntu.com/v1/0cef8205-ubuntu-font-family-0.83.zip &&\
    unzip ./0cef8205-ubuntu-font-family-0.83.zip &&\
    rm ./0cef8205-ubuntu-font-family-0.83.zip
# Update pip and install dependencies
RUN pip3 install --upgrade pip &&\ 
    pip3 install poetry &&\
    pip3 install -r requirements.txt &&\
    python3 ./setup.py install

# Define the entrypoint
ENTRYPOINT ["python3", "label_generator/cli.py", "--font", "./ubuntu-font-family-0.83/UbuntuMono-B.ttf"]