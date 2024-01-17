# Use an official Python runtime as a parent image
FROM python:3.9-slim
# install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /app

# copy /src to /app
COPY src/ /app
# now /src/proxy.py is in /app/proxy.py
RUN chmod +x proxy.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic

# Make port 8000 available to the world outside this container
EXPOSE 8000

# change directory to /app and run the command
CMD ["uvicorn", "proxy:app", "--host", "0.0.0.0" , "--port", "8000"]
