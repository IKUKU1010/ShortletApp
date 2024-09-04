# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files to the working directory
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --retries 5 --timeout 100 -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Specify the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
