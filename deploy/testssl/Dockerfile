# Dockerfile for running testssl.sh in parallel
FROM ubuntu:latest

# Create user
RUN groupadd -r testssl_user && useradd -r -g testssl_user testssl_user

# Update and install necessary packages
RUN apt-get update && apt-get install -y bash wget parallel bsdmainutils dnsutils
RUN wget -O testssl.tar.gz https://github.com/drwetter/testssl.sh/archive/master.tar.gz && \
    mkdir /opt/testssl && \
    tar xf testssl.tar.gz --strip-components=1 -C /opt/testssl && \
    ln -s /opt/testssl/testssl.sh /usr/local/bin/testssl.sh && \
    rm -rf testssl.tar.gz && \
    mkdir -p ~/.parallel && touch ~/.parallel/will-cite && \
    chown -R testssl_user:testssl_user /opt/testssl /usr/local/bin/testssl.sh

# Switch to the non-root user
USER testssl_user
WORKDIR /home/testssl_user

# Copy necessary files
COPY --chown=testssl_user:testssl_user ./scripts/get_cmd_lines.sh ./get_cmd_lines.sh
COPY --chown=testssl_user:testssl_user ./data/input.txt ./input.txt

# Generate parallel commands as the non-root user
RUN ./get_cmd_lines.sh ./input.txt ./commands.txt

RUN mkdir -p /home/testssl_user/results

ENTRYPOINT [ "tail", "-f", "/dev/null" ]
