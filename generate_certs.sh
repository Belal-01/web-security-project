#!/bin/bash

# Create ssl directory if it doesn't exist
mkdir -p apache/ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout apache/ssl/server.key \
    -out apache/ssl/server.crt \
    -subj "/CN=localhost"

echo "SSL certificates generated successfully in apache/ssl/"
