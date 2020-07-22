#!/usr/bin/env bash

# shellcheck disable=SC2164
cd "$(dirname "$0")"

echo Configuring Python virtual environment...
if [[ -d "./venv" ]]; then
  rm -rf ./venv
fi
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install --upgrade pip

echo Installing Python project dependencies...
pip3 install -r ./requirements.txt
