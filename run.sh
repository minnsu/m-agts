#!/bin/bash

# Start litellm in the background
litellm --model ollama/llama3.1:8b-instruct-q8_0 &

# Capture the PID of the background process
LITELLM_PID=$!

# Run the Python script
python3 ./src/main.py

# After the Python script finishes, kill the litellm process
kill $LITELLM_PID