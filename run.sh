#!/bin/bash

set -e

uvicorn api:app --host 0.0.0.0 --reload