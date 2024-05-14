import os
import discord
from discord.ext import commands
import aiohttp
import random
from keep_alive import keep_alive
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Define intents for the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create an instance of the bot with a command prefix and specified intents
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


async def fetch_image_from_ipfs(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                print(f"Failed to fetch image: HTTP {response.status}")
                return None


@bot.command()
async def getape(ctx, token_id: str = None):
    if token_id is None:
        token_id = str(random.randint(
            1, 2222))  # Use a random token ID if not provided
    elif not token_id.isdigit() or not 1 <= int(token_id) <= 2222:
        await ctx.send("Please enter a Token ID from 1 to 2222.")
        return  # Exit the command if the token ID is invalid

    base_url = "https://bafybeiclwkjjtd4la5t3dpt7ldbsicwxg4yy6iylnikgvbw6r3eqhhs6ou.ipfs.w3s.link"
    image_url = f"{base_url}/{token_id}.png"

    description = (
        f"[**@BasedApeGang**](https://twitter.com/basedapegang) **#BasedApeGang**\n"
        f"Token ID: #{token_id}\n\n"
        f"*GetApe bot by [sickoconut](https://twitter.com/sickoconut)*")
    embed = discord.Embed(description=description, color=0x0F2AC6)
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Normalize the message to catch "getape", "!getape", and "! getape"
    normalized_message = message.content.lower().replace(" ", "")
    if 'getape' in normalized_message and not normalized_message.startswith(
            '!getape'):
        help_description = "**Commands Usage:**\n" \
                           "`!getape` - Fetches an NFT image using a random token ID from 1 to 2222.\n" \
                           "`!getape <Token ID>` - Fetches an NFT image for the specified Token ID."
        embed_help = discord.Embed(description=help_description,
                                   color=0x0F2AC6)
        await message.channel.send(embed=embed_help)

    await bot.process_commands(
        message)  # Important to allow other commands to be processed

keep_alive()
bot.run(BOT_TOKEN)  # Use the environment variable here
