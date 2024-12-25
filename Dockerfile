FROM python:3.12-slim

WORKDIR /app

# Copy current directory's contents
COPY  . .

RUN pip install --no-cache-dir -r requirements.txt

# Use port 5000
EXPOSE 5000 

# Define environment variable
ENV NAME World

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]