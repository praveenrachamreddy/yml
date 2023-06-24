FROM registry.access.redhat.com/ubi8/ubi:latest

USER root

# Install required packages
RUN dnf install -y curl jq

# Set the working directory
WORKDIR /app

# Copy the vulnerability script to the image
COPY vulnerability_scan.sh /app/vulnerability_scan.sh

# Make the script executable
RUN chmod +x /app/vulnerability_scan.sh

# Set the entrypoint to execute the vulnerability script
ENTRYPOINT ["/app/vulnerability_scan.sh"]
