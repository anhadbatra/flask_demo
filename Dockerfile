# Use the official Python image from Docker Hub
FROM python:3.10

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    && apt-get clean

# Install Flask and pymongo
RUN pip install Flask pymongo

# Create and set the working directory
WORKDIR /app

# Copy the Flask application code into the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "run.py"]
