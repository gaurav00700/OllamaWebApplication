#!/bin/bash

echo "Starting Ollama..."
/bin/ollama serve &

pid=$!

echo "Waiting for Ollama to start..."
until ollama list > /dev/null 2>&1; do
  sleep 2
done

LLM_NAME=${LLM_NAME}

if ollama list | grep -q "$LLM_NAME"; then
  echo "Model $LLM_NAME already available."
else
  echo "Retrieving model: $LLM_NAME"
  ollama pull "$LLM_NAME"
  echo "Model $LLM_NAME is ready!"
fi

wait $pid