# Discord Keyword Monitor Bot

A Discord bot that monitors messages across all servers for specific keywords (like "urgent", "hiring", "bug bounty", etc.) and forwards matching messages to a designated channel.

## Project Structure

```
discord-monitor-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Features

- Monitors all servers the bot is in for specific keywords
- Forwards matching messages to your designated channel
- Rich embeds with server info, author, and direct message links
- Includes cybersecurity-related keywords (bounty, pentest, vulnerability, etc.)
- Duplicate message prevention
- Admin commands for stats and keyword viewing

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Privileged Gateway Intents" enable:
   - **MESSAGE CONTENT INTENT** (critical!)
   - SERVER MEMBERS INTENT
   - PRESENCE INTENT
6. Click "Reset Token" and copy your bot token (save it securely!)

### 2. Get Your Channel ID

1. Open Discord and enable Developer Mode:
   - User Settings → App Settings → Advanced → Developer Mode (toggle on)
2. Right-click on the channel where you want to receive alerts
3. Click "Copy Channel ID"

### 3. Invite Bot to Servers

1. In Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - `bot`
3. Select bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select each server you want to monitor and authorize

### 4. Local Testing (Optional)

```bash
# Clone or create the project directory
mkdir discord-monitor-bot
cd discord-monitor-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your values
# Add your bot token and channel ID

# Run the bot
python bot.py
```

## Deploying to Render

### Step 1: Prepare Your Code

1. Create a GitHub repository
2. Upload all project files:
   - `bot.py`
   - `requirements.txt`
   - `README.md`
   - `.env.example` (don't upload actual .env!)

### Step 2: Deploy on Render

1. Go to [Render.com](https://render.com/) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: discord-monitor-bot
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: Free (or paid for better uptime)

### Step 3: Add Environment Variables

In Render dashboard, go to "Environment" section and add:

```
DISCORD_BOT_TOKEN = your_actual_bot_token
TARGET_CHANNEL_ID = your_actual_channel_id
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your bot
3. Check the logs to confirm it's running

### Keeping the Bot Alive (Important!)

Render's free tier may spin down after inactivity. To keep it running:

**Option 1: Upgrade to Paid Plan** ($7/month for always-on service)

**Option 2: Use a Keep-Alive Service** (for free tier)
- Use [UptimeRobot](https://uptimerobot.com/) or [Cron-Job.org](https://cron-job.org/)
- Note: This won't work for Discord bots as they don't respond to HTTP requests
- **Recommended**: Just use Render's paid plan for reliability

**Option 3: Use Render Background Worker**
1. Change service type to "Background Worker" instead of "Web Service"
2. This is better suited for Discord bots
3. Still subject to free tier limitations

## Bot Commands

- `!stats` - Show bot statistics (admin only)
- `!keywords` - Display all monitored keywords (admin only)

## Monitored Keywords

The bot monitors for these keywords (case-insensitive):

**General Job/Opportunity Terms:**
- urgent, dev, developer, scripter, script
- pay, paying, hiring, recruit, recruiting
- bounty, reward, looking for, need help
- freelance, contract, project, opportunity
- position, job, work, gig

**Cybersecurity Specific:**
- bug bounty, vulnerability, pentest
- penetration test, security researcher
- ctf, forensics, malware analysis
- reverse engineering, exploit

## Customizing Keywords

Edit the `KEYWORDS` list in `bot.py`:

```python
KEYWORDS = [
    'urgent', 'hiring', 'bounty',
    # Add your own keywords here
    'your_keyword', 'another_keyword'
]
```

## Troubleshooting

### Bot is not receiving messages
- Ensure MESSAGE CONTENT INTENT is enabled in Discord Developer Portal
- Check that the bot has "Read Messages" permission in servers
- Verify the bot is actually in the servers you want to monitor

### Messages not forwarding
- Verify TARGET_CHANNEL_ID is correct
- Ensure bot has permission to send messages in target channel
- Check Render logs for error messages

### Bot keeps going offline
- Free Render instances spin down after inactivity
- Upgrade to paid plan ($7/month) for 24/7 uptime
- Or use a Background Worker service type

## Notes

- The bot only monitors messages sent AFTER it comes online
- Historical messages are not scanned
- Rate limits apply based on Discord's API limits
- Keep your bot token secure and never commit it to GitHub

## Legal & Ethical Considerations

- Only use this bot in servers where you have permission
- Respect Discord's Terms of Service
- Don't use for spam or harassment
- This is for monitoring public messages you already have access to

## Support

For issues with:
- **Discord API**: [Discord Developer Docs](https://discord.com/developers/docs)
- **Render Hosting**: [Render Docs](https://render.com/docs)
- **discord.py Library**: [discord.py Documentation](https://discordpy.readthedocs.io/)
