FROM vllm/vllm-openai:latest

# Install nginx
RUN apt-get update && apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for nginx
EXPOSE 80

# Start both nginx and vllm
ENTRYPOINT nginx && python3 -m vllm.entrypoints.openai.api_server --port 8000 --model google/gemma-2b