FROM python:3.10-slim

ARG DEBIAN_FRONTEND="noninteractive"

# Pip install first to cache the environment layer
COPY requirements.txt /api/

RUN python3 -m pip install --no-cache-dir -r /api/requirements.txt

# Copy the code layer
COPY api.py /api/
WORKDIR /api

# Add default startup command
CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]
