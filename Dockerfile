FROM node:20-alpine

# Install dependencies
RUN apk add --no-cache git curl bash

# Fake xdg-open: opencode web tries to open a browser, which crashes in containers
RUN printf '#!/bin/sh\nexit 0\n' > /usr/local/bin/xdg-open && chmod +x /usr/local/bin/xdg-open

# Install opencode globally
RUN npm install -g opencode-ai

# Create directories
RUN mkdir -p /root/.local/share/opencode /workspace

# Set working directory
WORKDIR /workspace

# Expose port
EXPOSE 4096

# Health check: any HTTP response (incl. 401 auth-required) means the server is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -s -o /dev/null http://localhost:4096/ || exit 1

# Start command
CMD ["sh", "-c", "opencode web --port 4096 --hostname 0.0.0.0"]
