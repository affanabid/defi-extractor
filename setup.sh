#!/bin/bash

# Make script exit on error
set -e

echo "🚀 Setting up DeFi Extractor..."

# Check if running in WSL
if grep -q Microsoft /proc/version; then
    echo "📌 WSL detected"
    echo "ℹ️  Make sure Chrome is installed in Windows"
else
    echo "📌 Native Linux detected"
    echo "ℹ️  Installing Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Telegram bot token"
fi

# Create data directory
mkdir -p data

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "1. Edit .env and add your Telegram bot token"
echo "2. Run 'npm start' to start the bot" 