# Base image with Python + NodeJS preinstalled
FROM nikolaik/python-nodejs:python3.10-nodejs19

# Fix outdated Debian repo issue
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i '/security.debian.org/d' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files into container
COPY . /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Start the bot (replace with your main entrypoint if different)
CMD ["bash", "start"]
