# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /usr/src/app
COPY . /src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "proxy.py"]
