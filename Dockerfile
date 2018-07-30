# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /FormicID
WORKDIR /FormicID

# Copy the current directory contents into the container at /FormicID
COPY . /FormicID

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
ENV NAME FormicID

# Run the program when the container launches
CMD ["python3", "formicID/get_dataset.py", "-c", "formicID/configs/config.json"]
