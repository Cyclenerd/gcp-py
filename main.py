#!/usr/bin/env python3

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

#
# Sample Flask application to demonstrate authentication with GCP APIs
# using the Google Cloud Client Libraries
#

# Import necessary libraries
import os
from flask import Flask, jsonify
from google.cloud import storage

# Define the port number to listen on (default 8080)
http_port = int(os.environ.get('PORT', 8080))

# Create a Flask application instance
app = Flask(__name__)

# Configure Google Cloud Storage client
# (Credentials are automatically retrieved from environment)
storage_client = storage.Client()


@app.route('/', methods=['GET'])
def hello():
    """
    This function defines a simple route for the root path ('/')
    of the application. It returns a basic 'Hello, World!' message.
    """
    return 'Hello, World!'


@app.route('/buckets', methods=['GET'])
def buckets():
    """
    This function defines a route for '/buckets' that retrieves a list
    of bucket names from Google Cloud Storage using the storage client.
    It returns a JSON response containing the list of bucket names.
    """
    # Get a list of buckets from the storage client
    buckets = list(storage_client.list_buckets())

    # Extract bucket names from the list of buckets
    bucket_names = []
    for bucket in buckets:
        bucket_names.append(str(bucket.name))

    # Return the list of bucket names as a JSON response
    return jsonify(bucket_names)


if __name__ == '__main__':
    # Run the Flask application on port http_port (0.0.0.0 for all interfaces)
    app.run(host='0.0.0.0', port=http_port)
