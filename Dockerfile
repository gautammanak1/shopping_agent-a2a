# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI application will run on
# Render will use this port to route external traffic
EXPOSE 8000

# Run main.py when the container launches
# This will start the FastAPI server on port 8000 and the agent system in a separate thread.
CMD ["python", "main.py"]
