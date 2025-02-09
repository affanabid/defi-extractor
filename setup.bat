@echo off
echo 🚀 Setting up DeFi Extractor...

:: Check for Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.x from https://www.python.org/downloads/
    exit /b 1
)

:: Check for Node.js installation
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js from https://nodejs.org/
    exit /b 1
)

:: Check for Chrome installation
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Chrome not found! Please install Chrome from https://www.google.com/chrome/
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🐍 Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

:: Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

:: Create .env if it doesn't exist
if not exist ".env" (
    echo 🔑 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your Telegram bot token
)

:: Create data directory
if not exist "data" mkdir data

echo ✅ Setup complete!
echo 📝 Next steps:
echo 1. Edit .env and add your Telegram bot token
echo 2. Run 'npm start' to start the bot

pause 