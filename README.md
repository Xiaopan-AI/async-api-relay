# Async API Relay

## Why build this

We have a Zapier zap that calls a webhook but it times out after 1 second (free account limitation, I know...) so the zap doesn't run properly.

I needed a way for the call to return immediately to Zapier, and process the request asynchronously in the background, because I don't really need the return value.

This universal API relay will work with any http POST request.

## Setup

```shell
pip install -r requirements.txt
```

## Usage

```shell
bash run.sh
```

Or you can build a Docker image and run it on some server

```shell
bash build_docker.sh [image-name]
```
