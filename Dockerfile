# syntax=docker/dockerfile:1.3-labs

# Build a docker image for serving the API

FROM python:3.10-slim

ARG DEBIAN_FRONTEND="noninteractive"

# Pip install first to cache the environment layer
COPY requirements.txt /api/

RUN <<EOF
set -e
python3 -m pip install --no-cache-dir -r /api/requirements.txt
EOF

# Copy the code layer
ADD __api.tar.gz /api
WORKDIR /api

# Add default startup command
CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]
