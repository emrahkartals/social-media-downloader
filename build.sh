#!/bin/bash
# Render build script for installing ffmpeg

set -e

echo "🔧 Installing system dependencies..."

# Update package list
apt-get update -qq

# Install ffmpeg (required for audio conversion)
apt-get install -y -qq ffmpeg

echo "✅ ffmpeg installed successfully"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully"

