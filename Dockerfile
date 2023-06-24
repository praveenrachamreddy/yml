FROM registry.access.redhat.com/ubi8/ubi:latest

USER root

# Install required packages
RUN dnf install -y curl jq

# Set the working directory
WORKDIR /app

# Create a placeholder script
RUN echo '#!/bin/sh\necho "No vulnerability script provided"' > /app/vulnerability_scan.sh

# Make the script executable
RUN chmod +x /app/vulnerability_scan.sh

# Set the entrypoint
ENTRYPOINT ["/bin/sh"]
