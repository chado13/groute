#!/bin/bash

set -ex

# apt-get install --no-install-recommends -y git

# github_token=$(cat /run/secrets/github_token) 
# echo -e "machine github.com\nlogin github-actions\npassword $github_token" > ~/.netrc && \
poetry install --sync
# rm -rf ~/.netrc

# python manage.py migrate;
uvicorn app:app --reload --host 0.0.0.0 --port 8000