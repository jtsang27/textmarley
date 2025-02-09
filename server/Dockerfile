# Use an official Python runtime
FROM python:3.11

# Set the working directory inside the container
WORKDIR /server

# Copy and install dependencies (Make sure you have a valid requirements.txt)
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /server

# Set environment variables
EXPOSE 8080

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "8", "src.app:app"]