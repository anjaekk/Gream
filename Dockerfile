FROM 3.8.12-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get install -y python3-dev

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

