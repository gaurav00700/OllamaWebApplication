FROM ollama/ollama

RUN pwd && ls -la

# Copy ollama setup script
COPY ../ollama_entrypoint.sh /ollama_entrypoint.sh

# Set environment variables for Ollama
ENV LLM_NAME=llama3.2:1b

# run the entrypoint script on container startup
ENTRYPOINT ["/usr/bin/bash", "/ollama_entrypoint.sh"]