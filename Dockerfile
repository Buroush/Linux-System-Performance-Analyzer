# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY python/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose any ports if necessary (e.g., if you're running a web server)
EXPOSE 8000

# Command to run the system monitor script
CMD ["python", "python/system_monitor.py", "--interval", "5", "--duration", "60"]

