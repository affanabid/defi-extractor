const TelegramBot = require('node-telegram-bot-api');
const { spawn } = require('child_process');
const fs = require('fs');
require('dotenv').config();

// Create bot instance
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

// Track scraping status and projects
let isScrapingInProgress = false;
let processedProjects = new Set();

// Function to send project details
async function sendProjectDetails(project, chatId) {
    try {
        // Skip if we've already processed this project
        if (processedProjects.has(project.name)) {
            return;
        }
        processedProjects.add(project.name);

        // Format project details
        const tgeDate = project.start_date || 'N/A';
        const raise = project.total_raise || 'N/A';
        
        // Get project focus (first sentence of description)
        let projectFocus = 'N/A';
        if (project.description) {
            projectFocus = project.description.split('.')[0].trim();
        }

        // Look for investor information
        let investors = 'N/A';
        if (project.description) {
            const investorKeywords = ['backed by', 'invested by', 'investors include', 'investment from', 'partners include'];
            for (const keyword of investorKeywords) {
                if (project.description.toLowerCase().includes(keyword)) {
                    const startIdx = project.description.toLowerCase().indexOf(keyword);
                    const endIdx = project.description.indexOf('.', startIdx);
                    if (endIdx !== -1) {
                        investors = project.description.substring(startIdx, endIdx).trim();
                        break;
                    }
                }
            }
        }

        const message = `*Project:* ${project.name}\n` +
                       `*TGE:* ${tgeDate}\n` +
                       `*Raise:* ${raise}\n` +
                       `*Working On:* ${projectFocus}\n` +
                       `*Investors:* ${investors}`;

        await bot.sendMessage(chatId, message, {
            parse_mode: 'Markdown',
            disable_web_page_preview: true
        }).catch(err => {
            // Fallback to plain text if markdown fails
            bot.sendMessage(chatId, message.replace(/\*/g, ''));
        });
    } catch (error) {
        console.error('Error sending project details:', error);
    }
}

// Function to watch JSON file for changes
function watchProjectFile(chatId) {
    let lastContent = '';
    
    // Check file every second for changes
    const watcher = setInterval(() => {
        if (!isScrapingInProgress) {
            clearInterval(watcher);
            return;
        }

        try {
            if (fs.existsSync('project_list.json')) {
                const currentContent = fs.readFileSync('project_list.json', 'utf8');
                
                if (currentContent !== lastContent) {
                    const projects = JSON.parse(currentContent);
                    const lastProject = projects[projects.length - 1];
                    
                    if (lastProject && !processedProjects.has(lastProject.name)) {
                        sendProjectDetails(lastProject, chatId);
                    }
                    
                    lastContent = currentContent;
                }
            }
        } catch (error) {
            console.error('Error watching project file:', error);
        }
    }, 1000); // Check every second
}

// Handle all messages to identify group chat ID
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const chatType = msg.chat.type;
    
    console.log(`Message received from ${chatType}:`, {
        chatId: chatId,
        chatTitle: msg.chat.title,
        messageType: msg.text ? 'text' : 'other'
    });
});

// Add scrape command
bot.onText(/\/scrape/, async (msg) => {
    const chatId = msg.chat.id;
    
    if (isScrapingInProgress) {
        bot.sendMessage(chatId, '⚠️ Scraping is already in progress...');
        return;
    }

    try {
        isScrapingInProgress = true;
        processedProjects.clear();
        await bot.sendMessage(chatId, '🚀 Starting DeFi projects scraper...');

        // Start watching the project file
        watchProjectFile(chatId);
                        
        // Run the selenium scraper
        const pythonProcess = spawn('python', ['scrapers/selenium_scraper.py']);
            
        // Handle Python script output (for debugging)
        pythonProcess.stdout.on('data', (data) => {
            console.log('Python output:', data.toString());
        });

        // Handle errors (only log to terminal)
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Scraper Error: ${data}`);
        });

        // Handle completion
        pythonProcess.on('close', async (code) => {
            isScrapingInProgress = false;
            if (code === 0) {
                try {
                    const projects = JSON.parse(fs.readFileSync('project_list.json', 'utf8'));
                    await bot.sendMessage(chatId, 
                        `✅ Scraping completed!\n` +
                        `Total projects found: ${projects.length}`
                    );
                } catch (error) {
                    console.error('Error reading final results:', error);
                }
            }
        });

    } catch (error) {
        isScrapingInProgress = false;
        console.error('Scraper error:', error);
    }
});

// Basic /start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const chatType = msg.chat.type;

    let message = '';
    if (chatType === 'private') {
        message = '🤖 DeFi Scraper Bot is connected!\n' +
                 'Commands:\n' +
                 '/scrape - Start scraping projects';
    } else {
        message = '🤖 DeFi Scraper Bot is connected to group!\n' +
                 `Chat ID: ${chatId}\n` +
                 'Commands:\n' +
                 '/scrape - Start scraping projects';
    }

    bot.sendMessage(chatId, message);
});

// Error handling (only log to terminal)
bot.on('polling_error', (error) => {
    console.error('Polling error:', error);
});

console.log('Bot is running...');


