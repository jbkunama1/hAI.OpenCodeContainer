FROM node:20-alpine

# Install dependencies
RUN apk add --no-cache git curl bash

# Install opencode globally
RUN npm install -g opencode-ai

# Create directories
RUN mkdir -p /root/.local/share/opencode /workspace

# Set working directory
WORKDIR /workspace

# Expose port
EXPOSE 4096

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:4096/health || exit 1

# Start command
CMD ["sh", "-c", "opencode web"]
