# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /FormicID
WORKDIR /FormicID

# Copy the current directory contents into the container at /FormicID
ADD . /FormicID

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
ENV NAME FormicID

# Run the program when the container launches
CMD ["python3", "main.py", "-c", "formicID/configs/config.json"]
