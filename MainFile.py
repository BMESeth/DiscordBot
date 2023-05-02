# -*- coding: utf-8 -*-
"""
Created on Tue May  2 16:01:29 2023

@author: DrPupper_RG
"""

import discord
from discord.ext import commands
#CHANGE THE BOT TOKEN
TOKEN = 'MTEwMzA0OTczNTc2MzQwNjg2OA.GTAKsw.PUc9aBXQjxSpzLBwcKsDtK8PJNjUCwrv0OJ0oM'
WAITING_ROOM_CHANNEL = 'waiting_room'
#Change the below options for new channels
CHANNEL_PREFIX = 'team_'
CHANNEL_SIZE = 60
NEW_CHANNEL_SIZE = 3
intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        guild = after.channel.guild
        waiting_room = discord.utils.get(guild.voice_channels, name=WAITING_ROOM_CHANNEL)

        if waiting_room and len(waiting_room.members) >= CHANNEL_SIZE:
            new_channel_name = f'{CHANNEL_PREFIX}{discord.utils.time_snowflake()}'
            new_channel = await guild.create_voice_channel(name=new_channel_name)

            for member in waiting_room.members:
                await member.move_to(new_channel)

bot.run(TOKEN)
