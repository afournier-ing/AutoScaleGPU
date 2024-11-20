# Use an official Python base image to include common dependencies
FROM docker.io/library/python:3.9-slim


# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh
ENV PATH="/root/.pulumi/bin:$PATH"

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Set working directory
WORKDIR /app

# Add entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint
COPY .secret   /app/.secret
RUN chmod +x /usr/local/bin/entrypoint

# Default entrypoint
ENTRYPOINT ["entrypoint"]

