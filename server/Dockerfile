# Use an official Python runtime
FROM python:3.11.5

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies (Make sure you have a valid requirements.txt)
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ .  

# Set environment variables
EXPOSE 8080

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "8", "server.src.app:app"]