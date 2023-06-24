FROM registry.access.redhat.com/ubi8/ubi:latest

USER root

# Install required packages
RUN dnf install -y curl jq

# Set the working directory
WORKDIR /app

# Set the entrypoint
ENTRYPOINT ["/bin/sh"]
