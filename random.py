import discord

import requests

from discord.ext import tasks

import asyncio

from discord import Intents

from discord.ext import commands #for importing commands

intents = discord.Intents.all()

client = discord.Client(intents=Intents.all())


@client.event
async def on_ready():
    print('client is ready')


async def update_nickname():
    await client.wait_until_ready()
    api_ids = ["summer", "winter", "spring", "autumn"]
    guild_id = 902220302199689266  # Replace with the ID of your desired guild

    while not client.is_closed():
        guild = client.get_guild(guild_id)
        for api_id in api_ids:
            member = guild.get_member(client.user.id)
            capitalized_nickname = api_id.capitalize()
            await member.edit(nick=capitalized_nickname)
            await update_activity(api_id)
            await asyncio.sleep(60)  # Sleep for 1 minute

async def update_activity(api_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={api_id}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if api_id in result:
            price = result[api_id]["usd"]
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{api_id.capitalize()} Price: ${price:.7f}"
            )
            await client.change_presence(activity=activity)

@client.event
async def on_ready():
    print('Bot is ready')
    client.loop.create_task(update_nickname())

# Replace 'YOUR_DISCORD_TOKEN' with your actual Discord client token
client.run('MTExMjI1MTE4MDczOTk5NzcyNg.GsVnW1.5MbFRYf9E-zJorG0GgWZjIJ9tfjkDcUSHc6cqw')
