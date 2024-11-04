# Copyright 2024 Nils Knieling
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use python:3.13-slim image for a minimal Python 3.13 environment
FROM python:3.13-slim

# Environment variables
# Configure Python to log messages immediately instead of buffering
ENV PYTHONUNBUFFERED="True"
# Reduce runtime by disabling pip version check
ENV PIP_DISABLE_ PIP_VERSION_CHECK=1
# Reduce image size by disabling pip cache
ENV PIP_NO_CACHE_DIR=1
# Define application port (default: 8080)
ENV PORT=8080
# Configure Gunicorn server arguments
# Bind to all interfaces (0.0.0.0), use 1 worker, 8 threads, no timeout
# Source: https://cloud.google.com/run/docs/tips/python#optimize_gunicorn
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0"

# Expose port for container access
EXPOSE $PORT

# Disable health check (implement a custom health check if needed)
HEALTHCHECK NONE

# Working directory
# Set the working directory inside the container to /app
WORKDIR /app

# Copy application files
# Copy requirements.txt file for dependency installation
COPY main.py ./
COPY requirements.txt ./

# Install dependencies listed in requirements.txt using pip
RUN pip install -r requirements.txt

# Start application
# Run Gunicorn server using the defined arguments, entrypoint is "main:app"
CMD ["gunicorn", "main:app"]
