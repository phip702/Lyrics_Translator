FROM python:3.12-slim

WORKDIR /usr/src/app

# Copy current directory's contents
COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

# Use port 5000
EXPOSE 5000 

# Define environment variable
ENV NAME World

ENV FLASK_APP=run.py

CMD [ "python", "./run.py" ]