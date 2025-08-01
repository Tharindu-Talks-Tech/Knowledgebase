#!/bin/bash

set -e  # Exit on any error

echo "Updating system packages..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing required dependencies..."
sudo apt install -y \
    curl \
    unzip \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common

### --- Install Docker ---
echo "Installing Docker..."

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the Docker stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Add current user to the docker group
sudo usermod -aG docker ubuntu

### --- Install AWS CLI v2 ---
echo "Installing AWS CLI v2..."

cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installations
echo "Verifying Docker installation..."
docker --version

echo "Verifying AWS CLI installation..."
aws --version

echo "Installation complete! You may need to log out and log back in for Docker group permissions to apply."
