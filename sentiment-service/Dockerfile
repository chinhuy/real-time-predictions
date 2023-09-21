# Use the official Python image as the base image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Expose the port that the app listens on
EXPOSE 5000

# Define the command to run the app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]