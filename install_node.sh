#!/bin/bash

# Download Node.js 18 (Linux x64 prebuilt)
curl -o node.tar.xz https://nodejs.org/dist/v18.20.4/node-v18.20.4-linux-x64.tar.xz

# Extract Node.js
mkdir -p .node
tar -xf node.tar.xz -C .node --strip-components=1

# Export PATH so Python can find node
export PATH=$PWD/.node/bin:$PATH

# Optional: Show version
node -v
