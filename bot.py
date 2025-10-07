import discord
from discord.ext import commands
import os
from datetime import datetime
import re

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration - Set these via environment variables
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '0'))
KEYWORDS = [
    'urgent', 'dev', 'developer', 'scripter', 'script', 'pay', 'paying',
    'hiring', 'recruit', 'recruiting', 'bounty', 'reward', 'bug bounty',
    'vulnerability', 'pentest', 'penetration test', 'security researcher',
    'ctf', 'forensics', 'malware analysis', 'reverse engineering',
    'exploit', 'looking for', 'need help', 'freelance', 'contract',
    'project', 'opportunity', 'position', 'job', 'work', 'gig'
]

# Track processed messages to avoid duplicates
processed_messages = set()

def contains_keyword(message_content):
    """Check if message contains any keyword (case-insensitive)"""
    content_lower = message_content.lower()
    for keyword in KEYWORDS:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', content_lower):
            return keyword
    return None

def create_embed(message, matched_keyword):
    """Create a rich embed for the forwarded message"""
    embed = discord.Embed(
        description=message.content[:4000],  # Discord limit
        color=discord.Color.blue(),
        timestamp=message.created_at
    )
    
    embed.set_author(
        name=f"{message.author.name} ({message.author.id})",
        icon_url=message.author.display_avatar.url
    )
    
    embed.add_field(
        name="Server",
        value=message.guild.name,
        inline=True
    )
    
    embed.add_field(
        name="Channel",
        value=f"#{message.channel.name}",
        inline=True
    )
    
    embed.add_field(
        name="Matched Keyword",
        value=f"**{matched_keyword}**",
        inline=True
    )
    
    embed.add_field(
        name="Jump to Message",
        value=f"[Click here]({message.jump_url})",
        inline=False
    )
    
    # Add attachments info if any
    if message.attachments:
        attachment_list = '\n'.join([f"[{att.filename}]({att.url})" for att in message.attachments[:5]])
        embed.add_field(
            name="Attachments",
            value=attachment_list,
            inline=False
        )
    
    embed.set_footer(text=f"Message ID: {message.id}")
    
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')
    print(f'Monitoring for keywords: {", ".join(KEYWORDS)}')
    print(f'Forwarding to channel ID: {TARGET_CHANNEL_ID}')
    
    # Verify target channel exists
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        print(f'Target channel found: #{target_channel.name} in {target_channel.guild.name}')
    else:
        print('WARNING: Target channel not found! Please check TARGET_CHANNEL_ID')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Ignore DMs
    if not message.guild:
        return
    
    # Avoid duplicate processing
    if message.id in processed_messages:
        return
    
    # Check for keywords
    matched_keyword = contains_keyword(message.content)
    
    if matched_keyword:
        processed_messages.add(message.id)
        
        # Keep set size manageable
        if len(processed_messages) > 10000:
            processed_messages.clear()
        
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        
        if target_channel:
            try:
                embed = create_embed(message, matched_keyword)
                await target_channel.send(embed=embed)
                print(f'Forwarded message from {message.guild.name} - Keyword: {matched_keyword}')
            except discord.Forbidden:
                print(f'No permission to send to target channel')
            except Exception as e:
                print(f'Error forwarding message: {e}')
        else:
            print(f'Target channel not found (ID: {TARGET_CHANNEL_ID})')
    
    await bot.process_commands(message)

@bot.command(name='stats')
@commands.has_permissions(administrator=True)
async def stats(ctx):
    """Show bot statistics"""
    embed = discord.Embed(
        title="Bot Statistics",
        color=discord.Color.green()
    )
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Monitored Keywords", value=len(KEYWORDS), inline=True)
    embed.add_field(name="Messages Processed", value=len(processed_messages), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='keywords')
@commands.has_permissions(administrator=True)
async def show_keywords(ctx):
    """Show current monitored keywords"""
    keywords_str = ', '.join(KEYWORDS)
    embed = discord.Embed(
        title="Monitored Keywords",
        description=keywords_str,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Run the bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        exit(1)
    
    if TARGET_CHANNEL_ID == 0:
        print("ERROR: TARGET_CHANNEL_ID environment variable not set!")
        exit(1)
    
    bot.run(TOKEN)
