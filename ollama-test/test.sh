#!/bin/bash

curl http://localhost:11434/api/generate \
  -d '{
    "model": "gemma3:1b",
    "prompt": "Explain dependency injection in simple terms.",
    "stream": false
  }'
