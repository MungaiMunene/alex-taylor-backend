# Use a base image with Python installed
FROM python:3.11-slim

# Install system dependencies for building Python packages, including gcc, libc-dev, and other build essentials
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    libffi-dev \
    libc-dev \
    libssl-dev \
    tzdata \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if needed)
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y build-essential python3-dev libffi-dev libssl-dev gcc