# FROM python:3.12-slim

# WORKDIR /app

# # Copy current directory's contents
# COPY  . .

# RUN pip install --no-cache-dir -r requirements.txt

# # Use port 5000
# EXPOSE 8080 

# # Define environment variable
# ENV NAME World

# #installs curl to docker
# RUN apt-get update && apt-get install -y curl 

# ENV FLASK_APP=app
# ENV FLASK_ENV=development


# # Copy the wait-for-it script to the container
# COPY wait-for-it.sh /wait-for-it.sh

# # Make sure the script is executable
# RUN chmod +x /wait-for-it.sh

# CMD ["/wait-for-it.sh", "rabbitmq:5672", "--", "flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]


FROM python:3.12-slim

WORKDIR /app

# Copy current directory's contents to /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080, which is Heroku's default web port
EXPOSE 8080

# Install curl to help with wait-for-it
RUN apt-get update && apt-get install -y curl

# Set environment variables for Flask
ENV FLASK_APP=app
ENV FLASK_ENV=production  
#Set to production for Heroku

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /wait-for-it.sh

# Make sure the wait-for-it script is executable
RUN chmod +x /wait-for-it.sh

# CMD to wait for RabbitMQ to be ready, then run Flask
#CMD ["/wait-for-it.sh", "rabbitmq:5672", "--", "flask", "run", "--host=0.0.0.0", "--port=8080"]

CMD ["/wait-for-it.sh", "rabbitmq:5672", "--", "gunicorn", "app:create_app"]
