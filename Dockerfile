FROM registry.access.redhat.com/ubi8/ubi

USER root

# Install required packages
RUN yum update -y && \
    yum install -y curl jq && \
    yum clean all

# Copy the script to the container
COPY vulnerability_scan.sh /app/vulnerability_scan.sh

# Set execute permissions for the script
RUN chmod +x /app/vulnerability_scan.sh

# Set permissions for writing files
RUN chgrp -R 0 /app && \
    chmod -R g=u /app

# Set the user to a non-root user
USER 1001

# Set the working directory
WORKDIR /app

# Set the entrypoint to the script
ENTRYPOINT ["/app/vulnerability_scan.sh"]
