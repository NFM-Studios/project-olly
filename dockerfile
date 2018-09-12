FROM python:slim

# Copy in your requirements file
ADD requirements.txt /requirements.txt

# Install requirements
RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /src/
WORKDIR /src/
ADD . /src/

# Ensure the start script is executable
RUN chmod +x /src/start.sh

# Run the start script
CMD /src/start.sh
