# -*- coding: utf-8 -*-
"""
Created on Tue May  2 16:01:29 2023

@author: DrPupper_RG
kick.com/DrPupper
"""

import json
import discord
import aiofiles
from discord.ext import commands
from discord.utils import get

TOKEN = 'YOUR_BOT_TOKEN'
#Change waiting room name
WAITING_ROOM_CHANNEL = 'waiting_room'
#Team Numbering
CHANNEL_PREFIX = 'Team_'
USERS_TO_MOVE = 20
#This implies a points file is separately created and upgraded
POINTS_FILE = 'points.json'

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_points():
    async with aiofiles.open(POINTS_FILE, mode='r') as f:
        return json.loads(await f.read())

async def save_points(points):
    async with aiofiles.open(POINTS_FILE, mode='w') as f:
        await f.write(json.dumps(points))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        guild = after.channel.guild
        waiting_room = get(guild.voice_channels, name=WAITING_ROOM_CHANNEL)

        if waiting_room and len(waiting_room.members) >= USERS_TO_MOVE:
            points_data = await load_points()
            sorted_members = sorted(waiting_room.members, key=lambda m: points_data.get(str(m.id), 0), reverse=True)
            selected_members = sorted_members[:USERS_TO_MOVE]

            for selected_member in selected_members:
                new_channel_name = f'{CHANNEL_PREFIX}{selected_member.name}'
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    selected_member: discord.PermissionOverwrite(view_channel=True, move_members=True),
                    guild.me: discord.PermissionOverwrite(view_channel=True),
                }
                new_channel = await guild.create_voice_channel(name=new_channel_name, overwrites=overwrites)
                await selected_member.move_to(new_channel)

bot.run(TOKEN)
