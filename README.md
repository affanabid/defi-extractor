# DeFi Project Scraper & Notifier

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node-%3E%3D%2014.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Selenium](https://img.shields.io/badge/selenium-4.17.2-green.svg)](https://www.selenium.dev/)

A powerful automation tool that scrapes DeFi project information from [CoinLaunch](https://coinlaunch.space/) and delivers real-time updates through Telegram. This project combines web scraping capabilities with instant messaging to keep you updated about new DeFi projects.

<p align="center">
  <img src="https://coinlaunch.space/images/logo.svg" alt="CoinLaunch Logo" width="200"/>
</p>

## 🌟 Features

- 🔍 **Advanced Web Scraping**
  - Utilizes Selenium with undetected-chromedriver for reliable scraping
  - Bypasses anti-bot measures effectively
  - Handles dynamic content loading

- 📊 **Comprehensive Project Information**
  - Project Name & Details
  - TGE (Token Generation Event) Date
  - Total Raise Amount
  - In-depth Project Description
  - Investor Information & Backing

- 🤖 **Intelligent Telegram Integration**
  - Real-time notifications
  - Formatted message delivery
  - Support for both private chats and groups
  - Command-based interaction

- ⚡ **Performance & Reliability**
  - Live updates with minimal delay
  - Continuous monitoring system
  - Robust error handling
  - Automatic recovery mechanisms

## 🏗 Project Structure

```
defi-extractor/
├── bot/                    # Telegram bot implementation
│   ├── index.js           # Main bot logic
│   └── .env              # Bot configuration
├── scrapers/              # Web scraping scripts
│   └── selenium_scraper.py # Main scraping logic
├── data/                  # Data storage directory
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies
└── project_list.json      # Scraped project data
```

## 🔧 Prerequisites

- **Python**: Version 3.x
  - Required for web scraping functionality
  - Handles Selenium automation

- **Node.js**: Version 14.0.0 or higher
  - Powers the Telegram bot
  - Manages real-time updates

- **Chrome Browser**
  - Required for Selenium automation
  - Should be compatible with chromedriver

- **Telegram Account**
  - Needed for bot creation and testing
  - Access to BotFather for setup

## 🚀 Setup Instructions

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/affanabid/defi-extractor
   cd defi-extractor
   ```

2. **Install Dependencies**
   ```bash
   # Node.js dependencies
   npm install

   # Python dependencies
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create `.env` in root directory:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ```

4. **Telegram Bot Setup**
   1. Message [@BotFather](https://t.me/botfather) on Telegram
   2. Create new bot: `/newbot`
   3. Follow prompts and save token
   4. Add token to `.env` file

5. **Launch Application**
   ```bash
   node bot/index.js
   ```

## 💡 Usage Guide

### Basic Commands
- `/start` - Initialize bot and view commands
- `/scrape` - Begin scraping process
- `/help` - View available commands

### Workflow
1. **Bot Initialization**
   - Establishes Telegram connection
   - Validates configuration
   - Prepares scraping environment

2. **Data Collection**
   - Automated navigation through CoinLaunch
   - Intelligent data extraction
   - Real-time processing

3. **Update Delivery**
   - Instant notifications
   - Formatted project details
   - Continuous monitoring

## ⚙️ Technical Details

### Scraping Engine
- Uses undetected-chromedriver for stealth
- Implements dynamic waiting mechanisms
- Handles pagination and data extraction

### Bot Architecture
- Event-driven design
- Robust error handling
- Automatic conflict resolution
- Webhook management

### Data Management
- JSON-based storage
- Real-time file watching
- Duplicate detection
- Data validation

## 🔍 Troubleshooting

### Common Issues
- **Polling Conflicts**: Restart bot to clear existing sessions
- **WSL Network Issues**: Special handling implemented
- **Chrome/Chromedriver**: Ensure compatible versions
- **Bot Responsiveness**: Check network connectivity

### Debug Tips
- Monitor console output
- Check Chrome installation
- Verify environment variables
- Ensure proper permissions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Affan Abid - [@affanabid](https://github.com/affanabid)

Project Link: [https://github.com/affanabid/defi-extractor](https://github.com/affanabid/defi-extractor)

---
<p align="center">Made with ❤️ by Affan Abid</p> 