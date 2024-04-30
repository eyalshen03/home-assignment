# Use Python base image
FROM python:3.9

# Set working directory within the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files into the container
COPY app.py .

# Expose the Flask port
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "app.py"]

