FROM python:3.11-slim

LABEL org.opencontainers.image.title="project-olly" \
      org.opencontainers.image.description="Django 2.2 esports platform" \
      org.opencontainers.image.licenses="UNLICENSED"

# Copy in your requirements file
COPY requirements.txt /requirements.txt

# Install requirements
RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /src/
WORKDIR /src/
COPY . /src/

# Create a non-root user to run the app and give it ownership of the app code,
# the socket directory and the static directory so named volumes inherit them
RUN useradd --create-home --shell /bin/bash olly \
    && mkdir -p /sock /static \
    && chown -R olly:olly /src /sock /static
USER olly

# Ensure the start script is executable
RUN chmod +x /src/start.sh

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz/', timeout=5)"

# Run the start script
CMD /src/start.sh