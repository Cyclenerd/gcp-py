# Getting Started with Google Cloud Python Development

[![Badge: Google Cloud](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?logo=google-cloud&logoColor=white)](#readme)
[![Badge: Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?logo=docker&logoColor=white)](#readme)
[![Badge: Podman](https://img.shields.io/badge/Podman-%23892CA0.svg?logo=podman&logoColor=white)](#readme)
[![Badge: Python](https://img.shields.io/badge/Python-3670A0?logo=python&logoColor=ffdd54)](#readme)

This guide walks you through setting up a development environment for working with Google Cloud Platform (GCP) using Python.

This guide will help you:

* Set up a local development environment for GCP projects using Python.
* Develop a Python [Flask](https://flask.palletsprojects.com/en/stable/) application locally.
* Containerize your application for efficient deployment.
* Test your application locally.
* Deploy your application to [Google Cloud Run](https://cloud.google.com/run/).

## Prerequisites

* A Bash shell (`bash`)
* Git (`git`)
* curl (`curl`)
* Google Cloud CLI (`gcloud`)
* Python 3 (`python3`)
* Docker (`docker`) or Podman (`podman`) (for containerized development)

### Clone

Clone this Git repository:

```bash
git clone "https://github.com/Cyclenerd/gcp-py.git"
cd "gcp-py"
```

### Google Cloud CLI

The Google Cloud CLI lets you manage and interact with GCP services from your terminal.

To install, use the packet manager (recommended) of your operating system or follow the [official guide](https://cloud.google.com/sdk/docs/install).

macOS:

```bash
brew install --cask google-cloud-sdk
```

Debian/Ubuntu:

```shell
sudo apt install apt-transport-https ca-certificates gnupg curl
curl -fsSL "https://packages.cloud.google.com/apt/doc/apt-key.gpg" | sudo gpg --dearmor -o "/usr/share/keyrings/cloud.google.gpg"
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a "/etc/apt/sources.list.d/google-cloud-sdk.list"
sudo apt update
sudo apt install google-cloud-cli
```

To initialize the gcloud CLI, run `gcloud init`:

```bash
gcloud init
```

### Podman

Podman is an open-source, OCI-compliant container management tool that offers a Docker-like experience without the need for a daemon.
This makes it a secure and lightweight alternative for managing containers.

> If you prefer to use Docker instead of Podman, simply replace `podman` with `docker`.

To install, use the packet manager (recommended) of your operating system or follow the [official guide](https://podman.io/).

macOS:

```bash
brew install podman
brew install --cask podman-desktop
```

Debian/Ubuntu:

```bash
sudo apt install podman
```

After installing, you need to create and start your first Podman machine:

```bash
podman machine init
podman machine start
```

You can then verify the installation information using:

```bash
podman info
```

### Python

This section shows you how to bring up an environment with the correct dependencies installed.

First, follow the [official guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) so that you have a working virtual environment and `pip3` installed.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Once you have created and activated a virtual environment, install the dependencies listed in `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### Application Default Credentials (ADC)

Application Default Credentials (ADC) provide credentials to call Google APIs.
Use the `gcloud auth application-default login` command to manage them on your machine.

> Avoid working with service accounts and account account keys.
> Service account keys could pose a security risk if compromised.

To use your own user credentials:

```bash
gcloud auth application-default login
```

For manual authentication (no web flow):

```bash
gcloud auth application-default login --no-launch-browser
```

Learn More: [User credentials provided by using the gcloud CLI](https://cloud.google.com/docs/authentication/application-default-credentials#personal)


## Develop Your App

With the tools installed, you can start developing.
Here's ([`main.py`](./main.py)) a simple Python Flask application that lists Google Cloud Storage buckets in your project:

```bash
export "GOOGLE_CLOUD_PROJECT=[YOUR-GOOGLE-CLOUD-PROJECT-ID]"
python3 main.py
```

Make sure to replace `[YOUR-GOOGLE-CLOUD-PROJECT-ID]` with your actual project ID.

Test command:

```bash
curl "http://localhosy:8080/buckets"
```

## Build a Container

This section demonstrates building a container with your Python application.

Build:

```bash
podman build --tag "gcp-py:test" .
```

Note to Mac users with Apple Silicon (M1, M2, ...) CPUs:
Cloud Run is Intel-based. Therefore, create and test the container with X86 (linux/amd64).

```bash
podman build --platform "linux/amd64" --tag "gcp-py:test" .
```

## Run the Container

Running the container directly will result in an authentication error:

```text
[...]
  File "/usr/local/lib/python3.13/site-packages/google/auth/_default.py", line 693, in default
    raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS)
google.auth.exceptions.DefaultCredentialsError: Your default credentials were not found. To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc for more information.
```

To fix this:

* Export your `GOOGLE_APPLICATION_CREDENTIALS` environment variable. This variable points to your credential file location on your machine (usually `~/.config/gcloud/application_default_credentials.json`).
* Set the `GOOGLE_APPLICATION_CREDENTIALS` variable inside the container.
* Set the `GOOGLE_CLOUD_QUOTA_PROJECT` and `GOOGLE_CLOUD_PROJECT` variable inside the container.

Here's the command with explanations:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
export "GOOGLE_CLOUD_PROJECT=[YOUR-GOOGLE-CLOUD-PROJECT-ID]"
podman run \
  -v "$GOOGLE_APPLICATION_CREDENTIALS:/tmp/adc.json:ro" \
  -e "GOOGLE_APPLICATION_CREDENTIALS=/tmp/adc.json" \
  -e "GOOGLE_CLOUD_QUOTA_PROJECT=$GOOGLE_CLOUD_PROJECT" \
  -e "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT" \
  -e "PORT=8080" \
  -p "8080:8080" \
  gcp-py:test
```

The `--volume` (`-v`) flag injects the credential file into the container (assumes you have already set your `GOOGLE_APPLICATION_CREDENTIALS` environment variable on your machine).

The `--environment` (`-e`) flag sets the `GOOGLE_APPLICATION_CREDENTIALS` variable inside the container.

Learn More: [Set the quota project using an environment variable](https://cloud.google.com/docs/quotas/set-quota-project#set-project-variable) and [Test locally](https://cloud.google.com/run/docs/testing/local#docker-with-google-cloud-access).

## Deploy the Container

Now lets deploy this Python Flask application to Google Cloud Run:

```bash
gcloud run deploy "gcp-py" \
  --source="." \
  --project="$GOOGLE_CLOUD_PROJECT" \
  --region="europe-west1" \
  --quiet
```

Test command:

```bash
curl "https://[YOUR-CLOUD-RUN].run.app/buckets" \
  -H "Authorization: bearer $(gcloud auth print-identity-token)"
```

Make sure to replace `[YOUR-CLOUD-RUN]` with your actual Google Cloud Run URL.

## Further Documents

Once you have familiarized yourself with the basics, you can expand your knowledge with the following helpful documents:

* [Cloud Run identities](https://cloud.google.com/run/docs/securing/service-identity)
* [Build and push a Docker image with Cloud Build](https://cloud.google.com/build/docs/build-push-docker-image)
* [Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview)
* [Google Cloud Platform Python Samples](https://github.com/GoogleCloudPlatform/python-docs-samples)
* [Avocano - dropship sample website (Lit, Django, SQL)](https://github.com/GoogleCloudPlatform/avocano)
* [Mesop - Build web apps quickly in Python](https://github.com/google/mesop)
